# Task 3.3 Mapping the ecosystem services linked with past, current, and projected LULUCF 
Using multiple datasets, such as EO data, ES initiatives and land/climate monitoring products (Copernicus), different ecosystem services will be quantified based on [SEEA-EA’s (System of Environmental Economic Accounting – Ecosystem Accounting Framework)](https://seea.un.org/ecosystem-accounting) reference list, including biomass provision, climate regulation, air filtration, water supply, soil erosion prevention, pollination potential, etc. The ecosystem services measured will then be combined to create a multi-tiered index of ecosystem multifunctionality, i.e., areas where multiple ecosystem services are supplied. To define the actual flow/use of services, a supply-demand ratio index will be estimated to identify the level of mismatches between provided services and society’s demand for natural resources. The latter will be quantified based on socio-economic data (demography, employment, etc. in T2.1). The output data products will in- clude individual ecosystem services, multifunctionality index, and supply-demand mismatches on superregional (250- 500m) and regional (10-30m) level. The provision of ecosystem services will be assessed, examining the links and changes over time based on historical and current LULUCF. An integration of landscape ecological assessment will ensure the understanding of the interplay between ecosystems structure, function, and services within the context of LULUCF. 

## Ecosystem extent
The MAES (Mapping and Assessment of Ecosystems and their Services) framework classifies ecosystems into 12 broad types to standardize environmental reporting and biodiversity monitoring across the European Union.

These 12 types are categorized into three major eco-regions:
- Terrestrial (7 types): Urban, Cropland, Grassland, Forest and woodland, Heathland and shrub, Sparsely vegetated land, and Wetland.
- Freshwater (1 type): Rivers and lakes.
- Marine (4 types): Marine inlets and transitional waters, Coastal, Shelf, and Open ocean.

[Link to the notebook](ecosystem_extent/ecosystem_extent.ipynb)

The only variables you should adapt are:<br>
`lccsFile = 'PATH_L4_landcover'`<br>
`outputFld = 'PATH_output'`


Output files:<br>
> filename__maesL2.tif: MAES-compliant Level 2 map<br>
> filename_maesL1.tif: MAES-compliant Level 1 map<br>
> filename_maesL2_area_ha.csv: Area of MAES Level 2 categories<br>
> filename_maesL1_area_ha.csv: Area of MAES Level 1 categories<br>

## Ecosystem condition

Reference period: 2000-2015 (similar to UNCCD SDG15.3.1 reference)

Two notebooks:
- data preparation: extract NDVI refrence and current periods + Tree cover
- compute ecosystem conditions

## Ecosystem services

## Landscape
PyLM is a Python implementation of the Landscape Mosaic model for processing land cover maps, generating stratification layers, and producing key landscape metrics and visualizations (e.g., heatmaps). It is designed for accessibility, flexibility, and integration with open-source tools, supporting use as a standalone script, in Jupyter Notebooks, or within larger workflows for research, conservation, and planning.

Main repository and documentation: https://github.com/ggiuliani/PyLM 

[Link to the notebook](landscape/landscape.ipynb)

Variables to edit:<br>
`lccsFile = 'PATH_L4_landcover'`<br>
`outputFolder = 'PATH_output'`

Output files:<br>
> lm19class.tif:  proportion of A-N-D classes on a per pixel basis aggregated  into 19 classes.<br>
> lmBackground.tif: summarizes the LM into 4 classes Natural - Agriculture - Developed - Mixed, showing the dominant presence of each LUC classes.<br>
> lmAgriculture.tif: summarizes the LM into 3 classes showing where agricultural LUC is dominant (>=60%), subdominant, or minor (<10%), thereby enabling the determination of the anthropogenic impact from agriculture.<br>
> lmDeveloped.tif: summarizes the LM into 3 classes showing where developed LUC is dominant (>=60%), subdominant, or minor (<10%), allowing to determine the anthropogenic impact from urbanization.<br>
> lmNatural.tif: summarizes the LM into 3 classes showing where natural LUC is dominant (>=60%), subdominant, or minor (<10%), allowing to determine the dominant natural classes not impacted by anthropogenic activies.<br>
> lmDiversity.tif: summarizes the LM into 4 classes to account the increasing degree of LUC diversity from Uniform, Dual, Triple, or Intermixed LUC, reporting on the degree of spatial heterogeneity.<br>
> lmAnthropicIntensity.tif: summarizes the anthopic intensity into 6 classes from Very Low - Low - Medium - High - Very High - Extreme, to account for the anthropogenic impacts.<br>
> heatmap.csv & stats.csv: provide summary statistics of the frequency distribution of the 103-classes within the ternary diagram.<br>

Files with _rgb are just for rendering purposes

## ES provided by ecosystem types

## Ecosystem health

## Suppy/Demand ratio

## Multifunctionality index
