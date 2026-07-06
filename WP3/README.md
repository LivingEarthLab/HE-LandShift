# Task 3.3 Mapping the ecosystem services linked with past, current, and projected LULUCF 
Using multiple datasets, such as EO data, ES initiatives and land/climate monitoring products (Copernicus), different ecosystem services will be quantified based on [SEEA-EA’s (System of Environmental Economic Accounting – Ecosystem Accounting Framework)](https://seea.un.org/ecosystem-accounting) reference list, including biomass provision, climate regulation, air filtration, water supply, soil erosion prevention, pollination potential, etc. The ecosystem services measured will then be combined to create a multi-tiered index of ecosystem multifunctionality, i.e., areas where multiple ecosystem services are supplied. To define the actual flow/use of services, a supply-demand ratio index will be estimated to identify the level of mismatches between provided services and society’s demand for natural resources. The latter will be quantified based on socio-economic data (demography, employment, etc. in T2.1). The output data products will in- clude individual ecosystem services, multifunctionality index, and supply-demand mismatches on superregional (250- 500m) and regional (10-30m) level. The provision of ecosystem services will be assessed, examining the links and changes over time based on historical and current LULUCF. An integration of landscape ecological assessment will ensure the understanding of the interplay between ecosystems structure, function, and services within the context of LULUCF. 

## Ecosystem extent
The MAES (Mapping and Assessment of Ecosystems and their Services) framework classifies ecosystems into 12 broad types to standardize environmental reporting and biodiversity monitoring across the European Union.

These 12 types are categorized into three major eco-regions:
- Terrestrial (7 types): Urban, Cropland, Grassland, Forest and woodland, Heathland and shrub, Sparsely vegetated land, and Wetland.
- Freshwater (1 type): Rivers and lakes.
- Marine (4 types): Marine inlets and transitional waters, Coastal, Shelf, and Open ocean.

[Link to the notebook](1.ecosystem_extent/ecosystem_extent.ipynb)

The only variables you should adapt are:<br>
`lccsFile = 'PATH_L4_landcover'`<br>
`outputFld = 'PATH_output'`


Output files:

> filename__maesL2.tif: MAES-compliant Level 2 map<br>
> filename_maesL1.tif: MAES-compliant Level 1 map<br>
> filename_maesL2_area_ha.csv: Area of MAES Level 2 categories<br>
> filename_maesL1_area_ha.csv: Area of MAES Level 1 categories<br>

## Ecosystem condition

## Ecosystem services

## Landscape

## ES provided by ecosystem types

## Ecosystem health

## Suppy/Demand ratio

## Multifunctionality index
