
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
<picture>
  <source srcset="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-white.png" height=175" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-black.png" height="175">
</picture>

[![PyPI](https://img.shields.io/pypi/v/foundry_ml.svg)](https://pypi.python.org/pypi/foundry_ml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/python-publish.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/python-publish.yml)
[![NSF-1931306](https://img.shields.io/badge/NSF-1931306-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1931306&HistoricalAwards=false)
[![DOI](https://zenodo.org/badge/236077574.svg)](https://zenodo.org/doi/10.5281/zenodo.10480757)
[<img src="https://img.shields.io/badge/view-documentation-blue">](https://ai-materials-and-chemistry.gitbook.io/foundry/)


Foundry-ML simplifies the discovery and usage of ML-ready datasets in materials science and chemistry providing a simple API to access even complex datasets. 
* Load ML-ready data with just a few lines of code
* Work with datasets in local or cloud environments. 
* Publish your own datasets with Foundry to promote community usage
* (in progress) Run published ML models without hassle

Learn more and see our available datasets on [Foundry-ML.org](https://foundry-ml.org/)



# Documentation
Information on how to install and use Foundry is available in our documentation [here](https://ai-materials-and-chemistry.gitbook.io/foundry/v/docs/).

DLHub documentation for model publication and running information can be found [here](https://dlhub-sdk.readthedocs.io/en/latest/servable-publication.html).

# Quick Start
Install Foundry-ML via command line with:
`pip install foundry_ml`

You can use the following code to import and instantiate Foundry-ML, then load a dataset.

```python
from foundry import Foundry
f = Foundry(index="mdf")


f = f.load("10.18126/e73h-3w6n", globus=False)
```
*NOTE*: This will download the dataset using HTTPS; if you want to download a very large dataset, set `globus=True` and be sure to install the [Globus Connect Personal endpoint](https://www.globus.org/globus-connect-personal).

If running this code in a notebook, a table of metadata for the dataset will appear:

<img width="903" alt="metadata" src="https://user-images.githubusercontent.com/16869564/197038472-0b6ae559-4a6b-4b20-88e5-679bb6eb4f5c.png">

We can use the data with `f.load_data()` and specifying splits such as `train` for different segments of the dataset, then use matplotlib to visualize it.

```python
res = f.load_data()

imgs = res['train']['input']['imgs']
desc = res['train']['input']['metadata']
coords = res['train']['target']['coords']

n_images = 3
offset = 150
key_list = list(res['train']['input']['imgs'].keys())[0+offset:n_images+offset]

fig, axs = plt.subplots(1, n_images, figsize=(20,20))
for i in range(n_images):
    axs[i].imshow(imgs[key_list[i]])
    axs[i].scatter(coords[key_list[i]][:,0], coords[key_list[i]][:,1], s = 20, c = 'r', alpha=0.5)
```
<img width="595" alt="Screen Shot 2022-10-20 at 2 22 43 PM" src="https://user-images.githubusercontent.com/16869564/197039252-6d9c78ba-dc09-4037-aac2-d6f7e8b46851.png">

[See full examples](./examples)

# Contributing
Foundry is an Open Source project and we encourage contributions from the community. To contribute, please fork from the `main` branch and open a Pull Request on the `main` branch. A member of our team will review your PR shortly.

# Primary Support
This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure".

# Other Support
Foundry-ML brings together many components in the materials data ecosystem. Including [MAST-ML](https://mastmldocs.readthedocs.io/en/latest/), the [Data and Learning Hub for Science](https://www.dlhub.org) (DLHub), and the [Materials Data Facility](https://materialsdatafacility.org) (MDF).

## MAST-ML
This work was supported by the National Science Foundation (NSF) SI2 award No. 1148011 and DMREF award number DMR-1332851

## The Data and Learning Hub for Science (DLHub)
This material is based upon work supported by Laboratory Directed Research and Development (LDRD) funding from Argonne National Laboratory, provided by the Director, Office of Science, of the U.S. Department of Energy under Contract No. DE-AC02-06CH11357.
https://www.dlhub.org

## The Materials Data Facility
This work was performed under financial assistance award 70NANB14H012 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the [Center for Hierarchical Material Design (CHiMaD)](http://chimad.northwestern.edu). This work was performed under the following financial assistance award 70NANB19H005 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Materials Design (CHiMaD). This work was also supported by the National Science Foundation as part of the [Midwest Big Data Hub](http://midwestbigdatahub.org) under NSF Award Number: 1636950 "BD Spokes: SPOKE: MIDWEST: Collaborative: Integrative Materials Design (IMaD): Leverage, Innovate, and Disseminate".
https://www.materialsdatafacility.org

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.dlhub.org"><img src="https://avatars.githubusercontent.com/u/4753182?v=4?s=100" width="100px;" alt="Ben Blaiszik"/><br /><sub><b>Ben Blaiszik</b></sub></a><br /><a href="#infra-blaiszik" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=blaiszik" title="Tests">⚠️</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=blaiszik" title="Code">💻</a> <a href="#data-blaiszik" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://kjschmidt.com"><img src="https://avatars.githubusercontent.com/u/16869564?v=4?s=100" width="100px;" alt="KJ Schmidt "/><br /><sub><b>KJ Schmidt </b></sub></a><br /><a href="#infra-kjschmidt913" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=kjschmidt913" title="Tests">⚠️</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=kjschmidt913" title="Code">💻</a> <a href="#data-kjschmidt913" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ascourtas"><img src="https://avatars.githubusercontent.com/u/18538526?v=4?s=100" width="100px;" alt="ascourtas"/><br /><sub><b>ascourtas</b></sub></a><br /><a href="#infra-ascourtas" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=ascourtas" title="Tests">⚠️</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=ascourtas" title="Code">💻</a> <a href="#data-ascourtas" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/blue442"><img src="https://avatars.githubusercontent.com/u/1233784?v=4?s=100" width="100px;" alt="Steve Wangen"/><br /><sub><b>Steve Wangen</b></sub></a><br /><a href="#infra-blue442" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=blue442" title="Tests">⚠️</a> <a href="https://github.com/MLMI2-CSSI/foundry/commits?author=blue442" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ribhavb"><img src="https://avatars.githubusercontent.com/u/68833659?v=4?s=100" width="100px;" alt="ribhavb"/><br /><sub><b>ribhavb</b></sub></a><br /><a href="https://github.com/MLMI2-CSSI/foundry/commits?author=ribhavb" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/WardLT"><img src="https://avatars.githubusercontent.com/u/7003149?v=4?s=100" width="100px;" alt="Logan Ward"/><br /><sub><b>Logan Ward</b></sub></a><br /><a href="https://github.com/MLMI2-CSSI/foundry/commits?author=WardLT" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
