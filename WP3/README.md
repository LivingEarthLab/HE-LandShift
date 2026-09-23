# WP3 — Ecosystem extent, condition, services, and landscape metrics

**Task 3.3 — Mapping the ecosystem services linked with past, current, and projected LULUCF**

Part of the [LandShift](https://landshift.eu) Horizon-Europe project · [University of Geneva — Living Earth Lab](https://www.unige.ch/envirospace/livingearth)

---

## Table of contents

- [Overview](#overview)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [1. Ecosystem extent](#1-ecosystem-extent)
- [2. Ecosystem condition](#2-ecosystem-condition)
- [3. Ecosystem services](#3-ecosystem-services)
- [4. Landscape](#4-landscape)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

---

## Overview

Using multiple datasets — Earth Observation (EO) data, ecosystem service (ES) initiatives, and land/climate monitoring products (Copernicus) — this task quantifies ecosystem services following the [SEEA-EA (System of Environmental Economic Accounting — Ecosystem Accounting Framework)](https://seea.un.org/ecosystem-accounting) reference list: biomass provision, climate regulation, air filtration, water supply, soil erosion prevention, pollination potential, etc.

Individual services are combined into a multi-tiered **ecosystem multifunctionality index** (areas where multiple services are jointly supplied), and a **supply–demand ratio** is estimated from socio-economic data (T2.1) to identify mismatches between the services provided and society's demand for natural resources.

The approach follows a three-tier model:

1. **Input data** — current and projected LULUCF patterns from Tasks 2.3 (mapping of current LULUCF) and 2.4 (AI-based future scenario modelling).
2. **Model layer** — ecosystem **extent**, **condition**, **services**, and **landscape structure** are each assessed through a dedicated set of notebooks (this folder).
3. **Synthesis layer** — outputs are combined into Ecosystem Services by ecosystem type, Ecosystem Health, Supply/Demand ratio, Ecosystem Multifunctionality, and Landscape metrics (see [Roadmap](#roadmap)).

More detail on the methodology is available in Deliverable D3.5.

## Repository structure

```
WP3/
├── ecosystem_extent/
│   └── ecosystem_extent.ipynb                 # MAES Level 1/2 classification from a LCCS map
├── ecosystem_condition/
│   ├── ecosystem_condition_prep.ipynb          # GEE data prep (NDVI reference/current, tree cover)
│   ├── clip_rasters_with_vector.ipynb          # Clip prepared rasters to the LC extent maps
│   └── ecosystem_condition.ipynb               # SEEA-EA condition score computation
├── ecosystem_services/
│   ├── ecosystem_services.ipynb                # Runs the 5 InVEST models (see below)
│   ├── carbon/                                 # Carbon pool tables (MAES L2 / L3)
│   ├── crop-pollination/                       # Guild and biophysical tables for Pollination
│   ├── habitat-quality/
│   │   ├── habitat_sensitivity.csv
│   │   ├── habitat_threats.csv
│   │   └── habitat_threats_extraction.ipynb    # Derives binary habitat masks from MAES L2
│   ├── sediment-retention/
│   │   ├── SDR_biophysical_table_*.csv
│   │   ├── sdr_biophysical.csv
│   │   └── clip_natcap_layers_to_basilicata.ipynb  # Clips global K-factor & erosivity layers
│   ├── water-purification/
│   │   ├── nutrient_biophysical.csv
│   │   └── nutrient_extract.ipynb              # Pulls NASADEM, HydroSHEDS & ERA5-Land precip.
│   └── misc/
│       └── forest_edge_biophysical.csv
├── landscape/
│   └── landscape.ipynb                         # PyLM landscape mosaic metrics
└── legends/                                    # QGIS .qml style files for the output rasters
    └── landscape/
```

## Requirements

- Python ≥ 3.10, with [JupyterLab](https://jupyter.org/) or a compatible notebook runtime
- [`geemap`](https://geemap.org/) and an authenticated [Google Earth Engine](https://earthengine.google.com/) account (used by `ecosystem_condition_prep.ipynb` and `nutrient_extract.ipynb`)
- [`natcap.invest`](https://naturalcapitalproject.stanford.edu/software/invest) (InVEST Python API, `pip install natcap.invest`) — used by `ecosystem_services.ipynb`
- [PyLM](https://github.com/ggiuliani/PyLM) — used by `landscape.ipynb`
- Standard geospatial stack: `rasterio`/`gdal`, `numpy`, `pandas`, `geopandas`

> Each notebook exposes a short **Parameters** cell near the top (workspace directory, input LULC/LCCS path, CRS, etc.) — edit only those cells before running; the processing cells below should not need changes.

---

## 1. Ecosystem extent

The [MAES](https://ec.europa.eu/environment/nature/knowledge/ecosystem_assessment/) (Mapping and Assessment of Ecosystems and their Services) framework classifies ecosystems into 12 broad types across three eco-regions, standardizing environmental reporting and biodiversity monitoring across the EU:

- **Terrestrial (7 types):** Urban, Cropland, Grassland, Forest and woodland, Heathland and shrub, Sparsely vegetated land, Wetland
- **Freshwater (1 type):** Rivers and lakes
- **Marine (4 types):** Marine inlets and transitional waters, Coastal, Shelf, Open ocean

**Notebook:** [`ecosystem_extent/ecosystem_extent.ipynb`](ecosystem_extent/ecosystem_extent.ipynb)

Variables to edit: `lccsFile = 'PATH_L4_landcover'`, `outputFld = 'PATH_output'`

| Output file | Description |
|---|---|
| `<name>_maesL2.tif` | MAES-compliant Level 2 classification map |
| `<name>_maesL1.tif` | MAES-compliant Level 1 classification map |
| `<name>_maesL2_area_ha.csv` | Area (ha) per MAES Level 2 category |
| `<name>_maesL1_area_ha.csv` | Area (ha) per MAES Level 1 category |

## 2. Ecosystem condition

Reference period: **2000–2015** (consistent with the UNCCD SDG 15.3.1 reference period).

Three notebooks, run in sequence:

1. [`ecosystem_condition/ecosystem_condition_prep.ipynb`](ecosystem_condition/ecosystem_condition_prep.ipynb) — prepares NDVI (reference and current period) and tree-cover layers in GEE
2. [`ecosystem_condition/clip_rasters_with_vector.ipynb`](ecosystem_condition/clip_rasters_with_vector.ipynb) — clips all prepared rasters to the land-cover extent maps
3. [`ecosystem_condition/ecosystem_condition.ipynb`](ecosystem_condition/ecosystem_condition.ipynb) — computes the SEEA-EA condition score

Edit the configuration cell and target CRS at the top of each notebook before running.

| Output file | Type | Description |
|---|---|---|
| `ecosystem_condition_map.tif` | GeoTIFF | SEEA-EA condition raster (1–5 score) |
| `condition_statistics.csv` | CSV | Per-ecosystem condition breakdown |
| `rle_assessment.csv` | CSV | IUCN Red List of Ecosystems (RLE) Criterion D assessment |
| `01_input_layers.png` | Figure | LCCS map + NDVI input layers |
| `02_condition_indicators.png` | Figure | The 4 biophysical indicators used |
| `03_ecosystem_condition_map.png` | Figure | Main condition map |
| `04_condition_by_ecosystem_group.png` | Figure | Stacked bar chart of condition by ecosystem group |
| `05_summary_dashboard.png` | Figure | Full summary dashboard |

## 3. Ecosystem services

Ecosystem services are quantified with five [InVEST](https://naturalcapitalproject.stanford.edu/software/invest) (Integrated Valuation of Ecosystem Services and Tradeoffs) models, all run from a single land-cover raster (LCCS/MAES map) plus model-specific biophysical tables shipped in the sub-folders below.

**Notebook:** [`ecosystem_services/ecosystem_services.ipynb`](ecosystem_services/ecosystem_services.ipynb)

Shared configuration (first code cell):

```python
workspace_dir = 'PATH_TO_YOUR_WORKSPACE_DIRECTORY'   # root output folder, shared by all models
luc           = 'PATH_TO_YOUR_LUC_FILE'               # land cover / LULC raster, shared by all models
```

Each model is run in its own section of the notebook via the InVEST Python API (`natcap.invest.<model>.execute(args)`); the required biophysical/guild tables are stored alongside this README, and the corresponding auxiliary notebooks (habitat threat extraction, nutrient layer extraction, layer clipping) are also linked below.

> Exact InVEST output filenames can change slightly between InVEST versions — see the linked user guide page for each model for the authoritative, versioned list. The tables below reflect the main outputs produced by the model configuration used in `ecosystem_services.ipynb`. All models also write an `intermediate_outputs/` sub-folder with the per-step rasters used to build the final layers, plus a `taskgraph_data.db` cache file used by InVEST for incremental re-runs — these are not reproduced in detail below.

### 3.1 Carbon storage and sequestration

[Model documentation](https://naturalcapitalproject.stanford.edu/invest/carbon) · Data: [`carbon/`](ecosystem_services/carbon/) (`carbon_pools_MAES_L2.csv`, `carbon_pools_MAES_L3.csv`)

Estimates carbon stored in the landscape as the sum of four carbon pools (aboveground biomass, belowground biomass, soil, dead matter) mapped from the biophysical (carbon pools) table onto the land-cover raster. The notebook runs a single-scenario configuration (`calc_sequestration = False`, no valuation), so only the baseline outputs below are produced.

| Output file | Description |
|---|---|
| `c_storage_bas.tif` | Total carbon stored per pixel (Mg C/ha) — sum of all four carbon pools for the baseline land cover |
| `raster_values_summary.csv` | Table summarizing total values, units, and filenames of the output rasters |
| `intermediate_outputs/c_above_bas.tif` | Aboveground carbon, mapped from the carbon pools table to the LULC |
| `intermediate_outputs/c_below_bas.tif` | Belowground carbon, mapped from the carbon pools table to the LULC |
| `intermediate_outputs/c_soil_bas.tif` | Soil carbon, mapped from the carbon pools table to the LULC |
| `intermediate_outputs/c_dead_bas.tif` | Dead organic matter carbon, mapped from the carbon pools table to the LULC |

### 3.2 Crop pollination

[Model documentation](https://naturalcapitalproject.stanford.edu/invest/crop-pollination) · Data: [`crop-pollination/`](ecosystem_services/crop-pollination/) (`crop_poll_guild_table.csv`, `crop_poll_biophysical_table.csv`)

Models wild pollinator abundance and pollination-dependent crop yield from nesting-habitat suitability and floral resource availability, by pollinator guild and season. The notebook runs without a farm vector (`farm_vector_path = ''`), so it produces the landscape-wide abundance/supply indices below rather than the farm-level yield outputs (which require a farm polygon input).

| Output file | Description |
|---|---|
| `pollinator_abundance_[SPECIES]_[SEASON].tif` | Abundance of pollinator guild `SPECIES` in season `SEASON`, one raster per guild/season combination in the guild table |
| `pollinator_supply_[SPECIES].tif` | Pollinator supply index for guild `SPECIES` — habitat suitability × reachable floral resources |
| `intermediate_outputs/habitat_nesting_index_[SPECIES].tif` | Nesting-habitat suitability index per guild |
| `intermediate_outputs/floral_resources_[SPECIES].tif` | Floral resources available to each guild |
| `intermediate_outputs/relative_floral_abundance_index_[SEASON].tif` | Relative floral abundance per season |

*(If a farm vector is supplied, the model additionally produces `farm_results.shp`, `farm_pollinators.tif`, `total_pollinator_yield.tif`, and `wild_pollinator_yield.tif`.)*

### 3.3 Habitat quality

[Model documentation](https://naturalcapitalproject.stanford.edu/invest/habitat-quality) · Data: [`habitat-quality/`](ecosystem_services/habitat-quality/) (`habitat_sensitivity.csv`, `habitat_threats.csv`) · Habitat masks derived with [`habitat_threats_extraction.ipynb`](ecosystem_services/habitat-quality/habitat_threats_extraction.ipynb)

Combines habitat suitability with the distance-decayed influence of mapped threats (e.g. cropland, urban land) and each land-cover class's sensitivity to those threats, producing a relative degradation and habitat-quality score. The notebook runs on a single scenario (`lulc_cur_path` only), so only the "current" outputs below are produced.

| Output file | Description |
|---|---|
| `quality_c.tif` | Relative habitat quality on the current landscape (0–1) |
| `deg_sum_c.tif` | Relative level of habitat degradation on the current landscape |
| `intermediate/habitat_c.tif` | Current habitat raster |
| `intermediate/[THREAT]_distance_transform_c.tif` | Distance to each mapped threat, current scenario |
| `intermediate/degradation_[THREAT]_c.tif` | Per-threat degradation contribution, current scenario |

*(If a baseline and/or future LULC are also supplied, the model additionally produces `quality_f.tif`, `deg_sum_f.tif`, and the habitat-rarity outputs `rarity_c.tif` / `rarity_c.csv` and `rarity_f.tif` / `rarity_f.csv`.)*

### 3.4 Nutrient delivery ratio (water purification)

[Model documentation](https://naturalcapitalproject.stanford.edu/invest/water-purification) · Data: [`water-purification/`](ecosystem_services/water-purification/) (`nutrient_biophysical.csv`) · DEM, watersheds and runoff proxy prepared with [`nutrient_extract.ipynb`](ecosystem_services/water-purification/nutrient_extract.ipynb)

Routes nitrogen and phosphorus loads generated on each pixel of the land-cover raster downslope to the stream network, using the DEM-derived flow network and watershed boundaries, and estimates how much load is retained versus exported. The notebook runs with both `calc_n` and `calc_p` enabled.

| Output file | Description |
|---|---|
| `watershed_results_ndr.gpkg` | Aggregated nutrient loads/exports (N and P) per watershed |
| `n_total_export.tif` | Total nitrogen export per pixel, surface + subsurface flow (kg/ha) |
| `n_surface_export.tif` | Nitrogen export per pixel by surface flow (kg/ha) |
| `n_subsurface_export.tif` | Nitrogen export per pixel by subsurface flow (kg/ha) |
| `p_surface_export.tif` | Phosphorus export per pixel by surface flow (kg/ha) |
| `stream.tif` | Stream network derived from the DEM and flow-accumulation threshold |
| `intermediate_outputs/d_up.tif`, `d_dn.tif` | Upslope/downslope factors of the index of hydrological connectivity |

### 3.5 Sediment delivery ratio (sediment retention)

[Model documentation](https://naturalcapitalproject.stanford.edu/invest/sediment-retention) · Data: [`sediment-retention/`](ecosystem_services/sediment-retention/) (`sdr_biophysical.csv`, plus global-value alternates for ESA CCI / ESA WorldCover LULC) · DEM, erodibility and erosivity layers clipped with [`clip_natcap_layers_to_basilicata.ipynb`](ecosystem_services/sediment-retention/clip_natcap_layers_to_basilicata.ipynb)

Combines the RUSLE (Revised Universal Soil Loss Equation) with a downslope sediment-retention/connectivity index to estimate how much eroded soil actually reaches the stream network, versus how much is trapped by vegetation on the way.

| Output file | Description |
|---|---|
| `usle.tif` | Total potential soil loss per pixel from the USLE equation (t/ha) |
| `rkls.tif` | Potential soil loss per pixel for bare soil (RKLS equation, no cover factor) |
| `sed_export.tif` | Sediment exported from each pixel that reaches the stream (t/ha) |
| `sed_deposition.tif` | Sediment deposited on the pixel from upslope sources (i.e. trapped, t/ha) |
| `avoided_export.tif` | Contribution of vegetation to keeping erosion out of the stream (on-pixel retention + upslope trapping) |
| `avoided_erosion.tif` | Contribution of vegetation to keeping soil from eroding off the pixel |
| `watershed_results_sdr.shp` | Aggregated sediment export, USLE total, avoided export/erosion, and deposition per watershed |
| `stream.tif` | Stream network derived from the DEM and flow-accumulation threshold |
| `stream_and_drainage.tif` | Union of the calculated stream layer with a supplied drainage layer (only if `drainage_path` is set) |

## 4. Landscape

[PyLM](https://github.com/ggiuliani/PyLM) is a Python implementation of the Landscape Mosaic model, processing land-cover maps into stratification layers and landscape metrics/visualizations (e.g. ternary-diagram heatmaps). It is designed to be used standalone, in notebooks, or embedded in larger workflows for research, conservation, and planning.

**Notebook:** [`landscape/landscape.ipynb`](landscape/landscape.ipynb)

Variables to edit: `lccsFile = 'PATH_L4_landcover'`, `outputFolder = 'PATH_output'`

| Output file | Description |
|---|---|
| `lm19class.tif` | Proportion of Agriculture-Natural-Developed (A-N-D) classes per pixel, aggregated into 19 classes |
| `lmBackground.tif` | LM summarized into 4 classes — Natural, Agriculture, Developed, Mixed — showing the dominant land-use/cover class |
| `lmAgriculture.tif` | LM summarized into 3 classes — dominant (≥60%), subdominant, or minor (<10%) agricultural LUC — for anthropogenic impact from agriculture |
| `lmDeveloped.tif` | LM summarized into 3 classes — dominant (≥60%), subdominant, or minor (<10%) developed LUC — for anthropogenic impact from urbanization |
| `lmNatural.tif` | LM summarized into 3 classes — dominant (≥60%), subdominant, or minor (<10%) natural LUC — for classes not impacted by anthropogenic activity |
| `lmDiversity.tif` | LM summarized into 4 classes of increasing LUC diversity — Uniform, Dual, Triple, Intermixed — reporting spatial heterogeneity |
| `lmAnthropicIntensity.tif` | Anthropic intensity summarized into 6 classes — Very Low, Low, Medium, High, Very High, Extreme |
| `heatmap.csv` | Frequency distribution of the 103 classes within the ternary diagram |
| `stats.csv` | Summary statistics of the ternary-diagram class distribution |

> Files with an `_rgb` suffix are colour-mapped copies of the above, intended for rendering only.

QGIS style files (`.qml`) for all landscape output rasters are provided in [`legends/landscape/`](legends/landscape/); styles for the extent and condition rasters are in [`legends/`](legends/).

---

## Roadmap

The following syntheses, combining the outputs above, are planned but not yet implemented in this folder:

- **ES provided by ecosystem types** — cross-tabulation of ecosystem services by MAES ecosystem type
- **Ecosystem health** — combined extent + condition + services indicator
- **Supply/demand ratio** — mismatch between ecosystem service supply and socio-economic demand (T2.1 data)
- **Multifunctionality index** — multi-tiered index of areas supplying multiple ecosystem services

## License

This work is released under the [European Union Public Licence (EUPL) v1.2](../LICENSE.txt), consistent with the rest of the [HE-LandShift repository](https://github.com/LivingEarthLab/HE-LandShift).

## Contact

Maintainer: [Gregory Giuliani](https://www.unige.ch/envirospace/people/giuliani), University of Geneva — Living Earth Lab.
Please use the [issue tracker](https://github.com/ggiuliani/LivingEarthLab/issues) to report problems or suggest improvements.
