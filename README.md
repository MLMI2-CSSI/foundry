
<picture>
  <source srcset="./assets/foundry-light.png" height=175" media="(prefers-color-scheme: dark)">
  <img src="./assets/foundry-dark.png" height="175">
</picture>

[![PyPI](https://img.shields.io/pypi/v/foundry_ml.svg)](https://pypi.python.org/pypi/foundry_ml)
[![tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/testing-work.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/testing-work.yml)

Foundry simplifies the discovery and usage of ML-ready datasets in materials science and chemistry providing a simple API to access even complex datasets. 
* Load ML-ready data with just a few lines of code
* Work with datasets in local or cloud environments. 
* Publish your own datasets with Foundry to promote community usage
* (in progress) Run published ML models without no hassle



# Documentation
Information on how to install and use foundry can be found in our documentation [here](https://ai-materials-and-chemistry.gitbook.io/foundry/v/docs/).

DLHub documentation for model publication and running information can be found [here](https://dlhub-sdk.readthedocs.io/en/latest/servable-publication.html).

# Quick Start
`pip install foundry_ml`

```python
from foundry import Foundry
f = Foundry(index="mdf")


f = f.load("10.18126/e73h-3w6n", globus=True)
res = f.load_dataset()
```

[See full examples](./examples)

# Primary Support
This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure".

# Other Support
Foundry brings together many components in the materials data ecosystem. Including [MAST-ML](https://mastmldocs.readthedocs.io/en/latest/), the [Data and Learning Hub for Science](https://www.dlhub.org) (DLHub), and the [Materials Data Facility](https://materialsdatafacility.org) (MDF).

## MAST-ML
This work was supported by the National Science Foundation (NSF) SI2 award No. 1148011 and DMREF award number DMR-1332851

## The Data and Learning Hub for Science (DLHub)
This material is based upon work supported by Laboratory Directed Research and Development (LDRD) funding from Argonne National Laboratory, provided by the Director, Office of Science, of the U.S. Department of Energy under Contract No. DE-AC02-06CH11357.
https://www.dlhub.org

## The Materials Data Facility
This work was performed under financial assistance award 70NANB14H012 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the [Center for Hierarchical Material Design (CHiMaD)](http://chimad.northwestern.edu). This work was performed under the following financial assistance award 70NANB19H005 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Materials Design (CHiMaD). This work was also supported by the National Science Foundation as part of the [Midwest Big Data Hub](http://midwestbigdatahub.org) under NSF Award Number: 1636950 "BD Spokes: SPOKE: MIDWEST: Collaborative: Integrative Materials Design (IMaD): Leverage, Innovate, and Disseminate".
https://www.materialsdatafacility.org
