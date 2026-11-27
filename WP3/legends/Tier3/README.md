# LandShift — QGIS styles for the D3.5 notebook outputs (§4.1 – §4.4)

Contents
- `qgis_styles/*.qml` — the style library (26 files, one per kind of output).
- `landshift_qml.py` — installer: writes `<raster>.qml` next to every recognised GeoTIFF, so QGIS styles the layer automatically when you add it.

## Quick start

    python landshift_qml.py install path/to/outputs --recursive     # needs numpy + rasterio
    python landshift_qml.py library qgis_styles                      # rewrite the library (stdlib + numpy only)

Add the GeoTIFFs to QGIS — each one already carries its style (a `.qml` with the same base name is applied on load).
Re-run `install` whenever the rasters change (the stretch of continuous layers is recomputed).

**Multiband rasters.** `<name>.qml` styles band 1; `<name>.band2.qml`, `<name>.band3.qml`, … style the other bands
(Layer Styling ▸ Style ▸ Load Style…).  Band order follows the band descriptions stored in the GeoTIFF.

**Fixed vs data-driven styles.**
- *Fixed* (exact, identical for every study area): health index, condition classes, MF indices, hotspots, trade-off SD, ratio, ratio classes, deficit counts.
- *Data-driven* (service maps, supply, demand, per-type means, GHG / water / erosion / pollination / nitrogen demand): the installer sets the stretch to the 2nd–98th percentile of the raster (lower end 0 for non-negative data).
  The library versions of these styles carry a provisional 0–1 range and the cumulative-cut setting: use `install` for the real stretch, or in QGIS Layer Styling ▸ Min/Max ▸ *Cumulative count cut 2–98 %* ▸ Apply.

## Which style is used for which output

| Notebook | GeoTIFF | Style | Type |
|---|---|---|---|
| §4.2 health | `ecosystem_health_index_pixel_<y>.tif`, `…_by_type_<y>.tif` | `health_index.qml` (red → green, 0–1; SEEA-EA class colours) | fixed |
| §4.1 services | `condition_class_<y>.tif` | `condition_class.qml` (Good / Moderate / Degraded / Not assessed) | classes |
| | `service_<service>_<y>.tif` | `service_*.qml` (ramp per service) | stretch |
| | `ecosystem_services_by_type_<y>.tif`, `…_supply_per_pixel_<y>.tif` | one band per service, ramp from the band's `service` tag | stretch per band |
| §4.3 multifunctionality | `mf_avg_<y>.tif`, `norm_<service>_<y>.tif`, `mf_sensitivity_scenarios_<y>.tif` | `mf_avg.qml` (YlGn 0–1) | fixed |
| | `mf_w_<y>.tif` | `mf_w.qml` (PuBuGn 0–1) | fixed |
| | `mf_thr_T0xx_<y>.tif`, `mf_thr_sensitivity_<y>.tif` | `mf_thr_count.qml` (0…n services) | classes |
| | `hotspot_map_<y>.tif` | `mf_hotspot_map.qml` | classes |
| | `mf_tradeoff_sd_<y>.tif` | `mf_tradeoff_sd.qml` (0–0.4) | fixed |
| | `mf_by_ecosystem_type_<y>.tif`, `mf_by_zone_<y>.tif` | bands: MF_avg, MF_w, MF_thr mean (0…n), MF_sd | fixed |
| §4.4 supply/demand | `ratio_<service>_<y>.tif`, `ratio_by_*_<y>.tif` | `ratio_continuous.qml` (diverging, centred on 1; stops 0.5 / 1 / 1.5 = Table 7) | fixed |
| | `ratio_class_<service>_<y>.tif` | `ratio_class.qml` (Table 7 classes) | classes |
| | `ratio_norm_<service>_<y>.tif` | `ratio_normalised.qml` | fixed |
| | `ratio_n_deficit_services_<y>.tif` | `ratio_n_deficit_services.qml` | classes |
| | `supply_<service>_<y>.tif`, `demand_<service>_<y>.tif` | `supply_generic.qml`, `demand_generic.qml` | stretch |
| demand helper | `ghg_emissions.tif`, `water_demand.tif`, `erosion_risk.tif`, `pollination_demand.tif`, `n_input.tif` | `demand_*.qml` | stretch |

Not styled (diagnostic): `components_*.tif`, `_aligned/*.tif`, demo inputs.

## Validation
All 82 style files generated for the demo outputs of the five notebooks (and the 26 library files) were loaded and rendered in headless QGIS 3.34
(`QgsRasterLayer.loadNamedStyle`, renderer type checked, layer rendered): no failures.  The files use only the standard
`singlebandpseudocolor` and `paletted` renderers and should work in any QGIS 3.x.

## Notes
- Nodata (−9999 for float, 255 for classes) comes from the GeoTIFF itself; no transparency is stored in the style.
- If you change `RATIO_CAP` in the notebook, re-run `install`: the ratio style reads the `ratio_cap` tag and rescales its last stop.
- The number of classes in the count styles follows the `n_services` tag of the raster.
