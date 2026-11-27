#!/usr/bin/env python3
"""
LandShift — QGIS style (.qml) library and installer for the D3.5 notebooks (§4.1 – §4.4).

Two commands
------------
  python landshift_qml.py library  <target_dir>            write the style library (one .qml per style)
  python landshift_qml.py install  <outputs_dir> [--recursive] [--dry-run]
                                                           write '<raster>.qml' next to every recognised GeoTIFF
                                                           (QGIS applies a .qml with the same base name automatically)

* Fixed-range outputs (health index, MF indices, ratio classes, …) get exact styles.
* Data-dependent outputs (service maps, supply, demand, per-type means) get a 2–98 % stretch computed from
  the actual raster (the 'install' command reads the rasters with rasterio); the 'library' command writes the same
  styles with a provisional 0–1 range and cumulative-cut metadata — use 'install' for the real stretch.
* Multiband rasters: '<name>.qml' styles band 1; '<name>.band2.qml', '<name>.band3.qml', … style the other bands
  (QGIS: Layer Styling ▸ Style ▸ Load Style…).

Only the Python standard library and numpy are needed for 'library'; 'install' also needs rasterio.
Written for QGIS 3.x (renderer types 'singlebandpseudocolor' and 'paletted').
"""
import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

import numpy as np

QGIS_VERSION = "3.28.0-Firenze"

# ─────────────────────────────────────────────────────────────────────────────
# Colour ramps (ColorBrewer / matplotlib stops)
# ─────────────────────────────────────────────────────────────────────────────
RAMPS = {
    "YlGn":   ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"],
    "PuBuGn": ["#f6eff7", "#bdc9e1", "#67a9cf", "#1c9099", "#016c59"],
    "Blues":  ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"],
    "Reds":   ["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"],
    "OrRd":   ["#fef0d9", "#fdcc8a", "#fc8d59", "#e34a33", "#b30000"],
    "YlOrBr": ["#ffffd4", "#fed98e", "#fe9929", "#d95f0e", "#993404"],
    "YlOrRd": ["#ffffb2", "#fecc5c", "#fd8d3c", "#f03b20", "#bd0026"],
    "RdPu":   ["#feebe2", "#fbb4b9", "#f768a1", "#c51b8a", "#7a0177"],
    "PuRd":   ["#f1eef6", "#d7b5d8", "#df65b0", "#dd1c77", "#980043"],
    "YlGnBu": ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"],
    "Greens": ["#edf8e9", "#bae4b3", "#74c476", "#31a354", "#006d2c"],
    "magma_r": ["#fcfdbf", "#fc8961", "#b73779", "#51127c", "#000004"],
    "viridis": ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
}
YLGN9 = ["#ffffe5", "#f7fcb9", "#d9f0a3", "#addd8e", "#78c679", "#41ab5d", "#238443", "#006837", "#004529"]
REDS9 = ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"]

# colour ramp per service key (supply / service maps)
SERVICE_RAMP = {
    "carbon_storage": "YlGn", "carbon_sequestration": "YlGn", "sediment_avoided_export": "Blues",
    "n_total_export": "YlOrBr", "n_retention": "YlGnBu", "habitat_quality": "RdPu",
    "pollinator_supply": "PuBuGn", "water_yield": "Blues",
}

# ─────────────────────────────────────────────────────────────────────────────
# QML writers
# ─────────────────────────────────────────────────────────────────────────────
def _head(opacity_note=""):
    return ("<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"
            f'<qgis version="{QGIS_VERSION}" styleCategories="Symbology" hasScaleBasedVisibilityFlag="0" '
            'maxScale="0" minScale="1e+08">\n')

_TAIL = ('    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>\n'
         '    <huesaturation colorizeBlue="128" colorizeGreen="128" colorizeOn="0" colorizeRed="255" '
         'colorizeStrength="100" grayscaleMode="0" invertColors="0" saturation="0"/>\n'
         '    <rasterresampler maxOversampling="2"/>\n'
         '  </pipe>\n'
         '  <blendMode>0</blendMode>\n'
         '</qgis>\n')


def _fmt(v):
    if abs(v) >= 1000 or (v != 0 and abs(v) < 0.01):
        return f"{v:.3g}"
    return f"{v:.4g}"


def qml_pseudocolor(items, band=1, cumulative_cut=False):
    """Interpolated single-band pseudocolor.  items = [(value, '#rrggbb', label), …] sorted by value."""
    items = sorted(items, key=lambda t: t[0])
    vmin, vmax = items[0][0], items[-1][0]
    limits = "CumulativeCut" if cumulative_cut else "None"
    out = [_head(), "  <pipe>\n",
           f'    <rasterrenderer type="singlebandpseudocolor" band="{band}" opacity="1" alphaBand="-1" nodataColor="" '
           f'classificationMin="{vmin!r}" classificationMax="{vmax!r}">\n',
           "      <rasterTransparency/>\n",
           f"      <minMaxOrigin>\n        <limits>{limits}</limits>\n        <extent>WholeRaster</extent>\n"
           "        <statAccuracy>Estimated</statAccuracy>\n        <cumulativeCutLower>0.02</cumulativeCutLower>\n"
           "        <cumulativeCutUpper>0.98</cumulativeCutUpper>\n        <stdDevFactor>2</stdDevFactor>\n"
           "      </minMaxOrigin>\n",
           "      <rastershader>\n",
           f'        <colorrampshader clip="0" colorRampType="INTERPOLATED" classificationMode="1" '
           f'minimumValue="{vmin!r}" maximumValue="{vmax!r}" labelPrecision="4">\n']
    for value, colour, label in items:
        out.append(f'          <item alpha="255" value="{value!r}" label={quoteattr(label)} color="{colour}"/>\n')
    out += ["        </colorrampshader>\n", "      </rastershader>\n", "    </rasterrenderer>\n", _TAIL]
    return "".join(out)


def qml_paletted(entries, band=1):
    """Unique-value (paletted) renderer.  entries = [(value, '#rrggbb', label), …]."""
    out = [_head(), "  <pipe>\n",
           f'    <rasterrenderer type="paletted" band="{band}" opacity="1" alphaBand="-1" nodataColor="">\n',
           "      <rasterTransparency/>\n", "      <colorPalette>\n"]
    for value, colour, label in entries:
        out.append(f'        <paletteEntry value="{int(value)}" label={quoteattr(label)} color="{colour}" alpha="255"/>\n')
    out += ["      </colorPalette>\n", "    </rasterrenderer>\n", _TAIL]
    return "".join(out)


def ramp_items(ramp, vmin, vmax, unit=""):
    cols = RAMPS[ramp] if isinstance(ramp, str) else ramp
    n = len(cols)
    items = []
    for i, c in enumerate(cols):
        v = vmin + (vmax - vmin) * i / (n - 1)
        lab = _fmt(v) + (f" {unit}" if unit and i in (0, n - 1) else "")
        items.append((float(v), c, lab))
    return items


# ─────────────────────────────────────────────────────────────────────────────
# Style definitions
# ─────────────────────────────────────────────────────────────────────────────
HEALTH_STOPS = [(0.0, "#c82020", "0 — Very poor"), (0.25, "#e87820", "0.25 — Poor"), (0.5, "#f0d040", "0.5 — Fair"),
                (0.75, "#78c850", "0.75 — Good"), (1.0, "#1a7a1a", "1 — Very good")]

def ratio_stops(cap=10.0):
    """Diverging ratio style centred on 1; boundaries 0.5 / 1 / 1.5 are the D3.5 Table 7 class limits."""
    cap = max(float(cap), 3.0)
    return [(0.0, "#a50026", "0"), (0.5, "#f46d43", "0.5 — deficit limit"), (1.0, "#ffffbf", "1 — balance"),
            (1.5, "#a6d96a", "1.5 — surplus limit"), (3.0, "#1a9850", "3"), (cap, "#006837", f"{_fmt(cap)} (cap)")]

RATIO_CLASSES = [(0, "#d73027", "High deficit (< 0.5)"), (1, "#fc8d59", "Moderate deficit (0.5 – 1.0)"),
                 (2, "#fee090", "Balanced (1.0 – 1.5)"), (3, "#91bfdb", "Surplus (> 1.5)")]
CONDITION_CLASSES = [(0, "#d9d9d9", "Not assessed"), (1, "#d73027", "Degraded (score 1–2)"),
                     (2, "#fee08b", "Moderate (score 3)"), (3, "#2ca25f", "Good (score 4–5)")]
HOTSPOT_CLASSES = [(0, "#d73027", "Cold spot (≤ Q25)"), (1, "#ffffbf", "Intermediate"), (2, "#1a9850", "Hotspot (≥ Q75)")]


def count_entries(n, palette, noun):
    return [(k, palette[min(k, len(palette) - 1)], f"{k} {noun}" + ("" if k == 1 else "s")) for k in range(n + 1)]


def style_qml(key, band=1, n=8, vmin=0.0, vmax=1.0, ramp=None, unit="", cap=10.0, cumulative_cut=False):
    """Return the QML text of a named style."""
    if key == "health_index":
        return qml_pseudocolor(HEALTH_STOPS, band)
    if key == "condition_class":
        return qml_paletted(CONDITION_CLASSES, band)
    if key == "mf_avg":
        return qml_pseudocolor(ramp_items("YlGn", 0, 1), band)
    if key == "mf_w":
        return qml_pseudocolor(ramp_items("PuBuGn", 0, 1), band)
    if key == "mf_sd":
        return qml_pseudocolor(ramp_items("magma_r", 0, 0.4), band)
    if key == "mf_thr":
        return qml_paletted(count_entries(n, YLGN9, "service"), band)
    if key == "hotspot":
        return qml_paletted(HOTSPOT_CLASSES, band)
    if key == "ratio":
        return qml_pseudocolor(ratio_stops(cap), band)
    if key == "ratio_class":
        return qml_paletted(RATIO_CLASSES, band)
    if key == "ratio_norm":
        return qml_pseudocolor([(v / max(cap, 3.0), c, l.split(" ")[0] if i in (0, 5) else "")
                                for i, (v, c, l) in enumerate(ratio_stops(cap))], band)
    if key == "deficit_count":
        return qml_paletted(count_entries(n, REDS9, "service"), band)
    if key == "stretch":
        return qml_pseudocolor(ramp_items(ramp or "viridis", vmin, vmax, unit), band, cumulative_cut)
    raise KeyError(key)


# the style library written by the 'library' command: (file name, kwargs)
LIBRARY = [
    # §4.2 ecosystem health
    ("health_index.qml", dict(key="health_index")),
    # §4.1 ecosystem services by ecosystem type
    ("condition_class.qml", dict(key="condition_class")),
    ("service_carbon_storage.qml", dict(key="stretch", ramp="YlGn", cumulative_cut=True)),
    ("service_sediment.qml", dict(key="stretch", ramp="Blues", cumulative_cut=True)),
    ("service_nitrogen_export.qml", dict(key="stretch", ramp="YlOrBr", cumulative_cut=True)),
    ("service_habitat_quality.qml", dict(key="stretch", ramp="RdPu", cumulative_cut=True)),
    ("service_pollinator_supply.qml", dict(key="stretch", ramp="PuBuGn", cumulative_cut=True)),
    ("service_generic_stretch.qml", dict(key="stretch", ramp="viridis", cumulative_cut=True)),
    # §4.3 multifunctionality
    ("mf_avg.qml", dict(key="mf_avg")),
    ("mf_w.qml", dict(key="mf_w")),
    ("mf_thr_count.qml", dict(key="mf_thr", n=8)),
    ("mf_hotspot_map.qml", dict(key="hotspot")),
    ("mf_tradeoff_sd.qml", dict(key="mf_sd")),
    ("mf_normalised_service.qml", dict(key="mf_avg")),
    ("mf_by_zone_band3_thr_mean.qml", dict(key="stretch", ramp="YlGn", vmin=0, vmax=5, unit="services", cumulative_cut=False)),
    # §4.4 supply/demand ratio
    ("ratio_continuous.qml", dict(key="ratio", cap=10)),
    ("ratio_class.qml", dict(key="ratio_class")),
    ("ratio_normalised.qml", dict(key="ratio_norm", cap=10)),
    ("ratio_n_deficit_services.qml", dict(key="deficit_count", n=8)),
    ("supply_generic.qml", dict(key="stretch", ramp="YlGn", cumulative_cut=True)),
    ("demand_generic.qml", dict(key="stretch", ramp="Reds", cumulative_cut=True)),
    # demand helper
    ("demand_ghg_emissions.qml", dict(key="stretch", ramp="Reds", cumulative_cut=True)),
    ("demand_water.qml", dict(key="stretch", ramp="Blues", cumulative_cut=True)),
    ("demand_erosion_risk.qml", dict(key="stretch", ramp="OrRd", cumulative_cut=True)),
    ("demand_pollination.qml", dict(key="stretch", ramp="PuRd", cumulative_cut=True)),
    ("demand_nitrogen_input.qml", dict(key="stretch", ramp="YlGnBu", cumulative_cut=True)),
]


def write_library(target):
    target = Path(target); target.mkdir(parents=True, exist_ok=True)
    for name, kw in LIBRARY:
        (target / name).write_text(style_qml(**kw), encoding="utf-8")
    print(f"{len(LIBRARY)} style files written to {target}")


# ─────────────────────────────────────────────────────────────────────────────
# Installer: pick a style for every recognised GeoTIFF
# ─────────────────────────────────────────────────────────────────────────────
Y = r"(?:_\d{4})?"
# (regex, plan).  plan = list of per-band style specs, the last one is repeated for further bands.
#   spec = ('fixed', key) | ('count', key) | ('stretch', ramp_or_None, role)
RULES = [
    (r"^ecosystem_health_index_(pixel|by_type)" + Y + r"\.tif$",        [("fixed", "health_index")]),
    (r"^condition_class" + Y + r"\.tif$",                                [("fixed", "condition_class")]),
    (r"^ecosystem_services_(by_type|supply_per_pixel)" + Y + r"\.tif$",  [("stretch", None, "service")]),
    (r"^service_.+" + Y + r"\.tif$",                                     [("stretch", None, "service")]),
    (r"^mf_avg" + Y + r"\.tif$",                                         [("fixed", "mf_avg")]),
    (r"^mf_w" + Y + r"\.tif$",                                           [("fixed", "mf_w")]),
    (r"^mf_thr_sensitivity" + Y + r"\.tif$",                             [("count", "mf_thr")]),
    (r"^mf_thr_T\d+" + Y + r"\.tif$",                                    [("count", "mf_thr")]),
    (r"^mf_sensitivity_scenarios" + Y + r"\.tif$",                       [("fixed", "mf_avg"), ("fixed", "mf_w")]),
    (r"^mf_tradeoff_sd" + Y + r"\.tif$",                                 [("fixed", "mf_sd")]),
    (r"^hotspot_map" + Y + r"\.tif$",                                    [("fixed", "hotspot")]),
    (r"^norm_.+" + Y + r"\.tif$",                                        [("fixed", "mf_avg")]),
    (r"^mf_by_(ecosystem_type|zone)" + Y + r"\.tif$",                    [("fixed", "mf_avg"), ("fixed", "mf_w"),
                                                                          ("stretch", "YlGn", "thr_mean"), ("fixed", "mf_sd")]),
    (r"^ratio_class_.+" + Y + r"\.tif$",                                 [("fixed", "ratio_class")]),
    (r"^ratio_norm_.+" + Y + r"\.tif$",                                  [("fixed", "ratio_norm")]),
    (r"^ratio_n_deficit_services" + Y + r"\.tif$",                       [("count", "deficit_count")]),
    (r"^ratio_by_(ecosystem_type|zone)" + Y + r"\.tif$",                 [("fixed", "ratio")]),
    (r"^ratio_(?!class|norm|n_deficit|by_).+" + Y + r"\.tif$",           [("fixed", "ratio")]),
    (r"^supply_.+" + Y + r"\.tif$",                                      [("stretch", None, "supply")]),
    (r"^demand_.+" + Y + r"\.tif$",                                      [("stretch", "Reds", "demand")]),
    (r"^ghg_emissions\.tif$",                                            [("stretch", "Reds", "demand")]),
    (r"^water_demand\.tif$",                                             [("stretch", "Blues", "demand")]),
    (r"^erosion_risk\.tif$",                                             [("stretch", "OrRd", "demand")]),
    (r"^pollination_demand\.tif$",                                       [("stretch", "PuRd", "demand")]),
    (r"^n_input\.tif$",                                                  [("stretch", "YlGnBu", "demand")]),
]


def band_stretch(ds, band, lower_zero=True, pct=(2, 98), max_px=2_000_000):
    """(vmin, vmax) of a band from a decimated read; ignores nodata."""
    h, w = ds.height, ds.width
    f = max(1, int(np.ceil(np.sqrt(h * w / max_px))))
    arr = ds.read(band, out_shape=(max(h // f, 1), max(w // f, 1)), masked=True)
    v = arr.compressed().astype("float64")
    v = v[np.isfinite(v)]
    if v.size == 0:
        return 0.0, 1.0
    lo, hi = np.percentile(v, pct)
    if lo >= 0 or v.min() >= 0:
        lo = 0.0 if (lower_zero and v.min() >= 0) else lo
    if hi <= lo:
        hi = float(v.max()) if v.max() > lo else lo + 1e-6
    return float(lo), float(hi)


def _tag(ds, band, name, default=None):
    t = ds.tags(band).get(name)
    return t if t is not None else ds.tags().get(name, default)


def _n_services(ds, band):
    n = _tag(ds, band, "n_services")
    if n is None and _tag(ds, band, "services"):
        n = len(str(_tag(ds, band, "services")).split(","))
    try:
        return int(n)
    except (TypeError, ValueError):
        return 5


def resolve(ds, plan, band):
    """QML text for one band of an open rasterio dataset."""
    spec = plan[min(band - 1, len(plan) - 1)]
    kind = spec[0]
    if kind == "fixed":
        cap = _tag(ds, band, "ratio_cap", "10")
        try:
            cap = float(cap)
        except ValueError:
            cap = 10.0
        return style_qml(spec[1], band=band, cap=cap)
    if kind == "count":
        return style_qml(spec[1], band=band, n=_n_services(ds, band))
    # stretch
    _, ramp, role = spec
    service = _tag(ds, band, "service")
    if role in ("service", "supply"):
        ramp = SERVICE_RAMP.get(service, "viridis")
    if role == "thr_mean":
        return style_qml("stretch", band=band, ramp=ramp, vmin=0.0, vmax=float(_n_services(ds, band)), unit="services")
    unit = _tag(ds, band, "unit", "") or ""
    vmin, vmax = band_stretch(ds, band)
    return style_qml("stretch", band=band, ramp=ramp, vmin=vmin, vmax=vmax, unit=unit)


def install(folder, recursive=False, dry_run=False):
    import rasterio
    folder = Path(folder)
    files = sorted(folder.rglob("*.tif") if recursive else folder.glob("*.tif"))
    done, skipped = 0, []
    for f in files:
        plan = next((p for rx, p in RULES if re.match(rx, f.name)), None)
        if plan is None:
            skipped.append(f.name); continue
        with rasterio.open(f) as ds:
            names = []
            for b in range(1, ds.count + 1):
                qml = resolve(ds, plan, b)
                out = f.with_suffix(".qml") if b == 1 else f.with_name(f"{f.stem}.band{b}.qml")
                if not dry_run:
                    out.write_text(qml, encoding="utf-8")
                names.append(out.name)
        print(f"  {f.name:<58} → {', '.join(names)}")
        done += 1
    print(f"\n{done} raster(s) styled" + (f"; not recognised (no style): {skipped}" if skipped else "") + (" [dry run]" if dry_run else ""))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("library", help="write the style library"); a.add_argument("target")
    b = sub.add_parser("install", help="write <raster>.qml next to the rasters"); b.add_argument("folder")
    b.add_argument("--recursive", action="store_true"); b.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if args.cmd == "library":
        write_library(args.target)
    else:
        install(args.folder, args.recursive, args.dry_run)


if __name__ == "__main__":
    main()
