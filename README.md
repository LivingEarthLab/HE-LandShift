# LandShift repository

This is the repository of the University of Geneva – [Living Earth Lab](https://www.unige.ch/envirospace/livingearth) for the Horizon Europe [LandShift](https://landshift.eu) project. It hosts the code and notebooks we develop as our contribution to the [Living Earth](https://livingearthhub.org) framework.

<p align="center">
	<img src="img/LANDSHIFT-logo-RGB_no-tagline-scaled.png" alt="MONALISA" width="200"/>
</p>

## About LandShift

**LandShift** (*Community-Led Creation of Living Spaces in Shifting Landscapes for Climate-Resilient Land Use Management and Supporting the New European Bauhaus*) is a Horizon Europe Research and Innovation Action running from 1 November 2024 to 31 October 2027 (call HORIZON-CL6-2024-CLIMATE-01, grant agreement No [101182007](https://cordis.europa.eu/project/id/101182007)).

It develops solutions to reduce biogenic emissions, enhance ecosystem resilience, and promote sustainable land use and land management. It does so by combining nature-based solutions, aligned with the New European Bauhaus, with monitoring, reporting and verification (MRV) systems that measure impacts on emissions, biodiversity, and ecosystem health.

**Our contribution.** The Living Earth Lab provides Earth Observation data science expertise: land cover mapping and projections, ecosystem services and condition assessments, and data cube infrastructure.

## Contents

You will find our main contributions and the relevant source code and notebooks for the following work:

| Work package | Topic | Location |
|--------------|-------|----------|
| WP2 | LCCS land cover maps production | *coming soon* |
| WP2 | Land cover projections | *coming soon* |
| WP3 | Ecosystem services, extent, condition and landscapes | [WP3](WP3) |
| WP5 | Data cubes creation | *coming soon* |

## Getting started

### Prerequisites

- Python 3.10+
- A [Google Earth Engine](https://earthengine.google.com/) account (for GEE-based notebooks)
- Jupyter (JupyterLab recommended)

### Installation

```bash
git clone https://github.com/LivingEarthLab/HE-LandShift.git
cd HE-LandShift

# Install the dependencies required by the notebooks you want to run
# (see the notebook headers or the module's README)
jupyter lab
```

> 🔧 *If you have an `environment.yml` or `requirements.txt`, reference it here.*

## Contributor guidelines

Contributions are welcome and greatly appreciated! To contribute, please follow these guidelines:

**Reporting issues**
* Check that the issue has not already been reported on the [issue tracker](https://github.com/LivingEarthLab/HE-LandShift/issues).
* Submit a new issue on the [issue tracker](https://github.com/LivingEarthLab/HE-LandShift/issues).

**Development process**
* Fork the repository, make changes in your fork, and submit a pull request.
* Follow the existing coding style and structure.
* Write tests for any new functionality.
* Document any changes in the package documentation.

**Where to get help**
* Maintainer: [Gregory Giuliani](https://www.unige.ch/envirospace/people/giuliani)

## Citation

If you use this repository in your work, please cite it:

```bibtex
@software{landshift_livingearthlab,
  author    = {{Living Earth Lab, University of Geneva}},
  title     = {LandShift repository},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/LivingEarthLab/HE-LandShift}
}
```

## License

Released under the [European Union Public Licence v1.2 (EUPL-1.2)](LICENSE.txt).

## Acknowledgements

This work has received funding from the European Union's Horizon Europe research and innovation programme under grant agreement No **101182007** (LandShift).

> 🔧 *Add the Swiss funding statement (e.g. SERI) if required for UNIGE's participation.*
