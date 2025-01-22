<picture>
  <source srcset="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-white.png" height=175" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-black.png" height="175">
</picture>

[![PyPI](https://img.shields.io/pypi/v/foundry_ml.svg)](https://pypi.python.org/pypi/foundry_ml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/python-publish.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/python-publish.yml)
[![NSF-1931306](https://img.shields.io/badge/NSF-1931306-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1931306&HistoricalAwards=false)
[<img src="https://img.shields.io/badge/view-documentation-blue">](https://ai-materials-and-chemistry.gitbook.io/foundry/)
[![Coverage](https://codecov.io/gh/MLMI2-CSSI/foundry/branch/main/graph/badge.svg)](https://codecov.io/gh/MLMI2-CSSI/foundry)


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

You can use the following code to import and instantiate Foundry-ML, then load a dataset:

```python
from foundry import Foundry

f = Foundry(index="mdf")
results_df = f.search(query="materials science", limit=10)
print(results_df.head())
```

Below is an example of publishing your own dataset with Foundry:

```python
# Let's assume you have a local folder of data you'd like to publish
from foundry.foundry_dataset import FoundryDataset

dataset = FoundryDataset(dataset_name="MyNewDataset")
dataset.add_data("/path/to/local_data_folder")  # Make sure to have the correct structure

# Then publish the dataset
res = f.publish_dataset(dataset, update=False, test=False)
print("Dataset submitted with response:", res)
```

If you run locally and don't want to install the [Globus Connect Personal endpoint](https://www.globus.org/globus-connect-personal), just set the `globus=False` when loading datasets.

# How to Contribute

We welcome contributions from the community to enhance Foundry-ML. Whether you want to fix a bug, propose a new feature, or improve documentation, follow the steps below to get started:

1. Fork the repository:
   - Click the "Fork" button at the top of this repository's page.

2. Clone your fork locally:
   - git clone https://github.com/your-username/foundry.git

3. Create a new branch for your feature or fix:
   - git checkout -b feature/my-new-feature

4. Install dependencies and set up a virtual environment if needed:
   - pip install -r requirements.txt

5. Make your changes and write tests:
   - For code-related changes, add or update tests under tests/ to ensure ongoing stability.

6. Run tests to confirm everything works:
   - pytest

7. Commit your changes and push the branch to GitHub:
   - git push origin feature/my-new-feature

8. Create a Pull Request:
   - On GitHub, open a Pull Request from your branch to the main branch of MLMI2-CSSI/foundry.

Our team will review your submission and provide feedback. Thank you for helping us grow Foundry-ML!

# How to Cite
If you find Foundry-ML useful, please cite the following [paper](https://doi.org/10.21105/joss.05467)

```
@article{Schmidt2024,
  doi = {10.21105/joss.05467},
  url = {https://doi.org/10.21105/joss.05467},
  year = {2024}, publisher = {The Open Journal},
  volume = {9},
  number = {93},
  pages = {5467},
  author = {Kj Schmidt and Aristana Scourtas and Logan Ward and Steve Wangen and Marcus Schwarting and Isaac Darling and Ethan Truelove and Aadit Ambadkar and Ribhav Bose and Zoa Katok and Jingrui Wei and Xiangguo Li and Ryan Jacobs and Lane Schultz and Doyeon Kim and Michael Ferris and Paul M. Voyles and Dane Morgan and Ian Foster and Ben Blaiszik},
  title = {Foundry-ML - Software and Services to Simplify Access to Machine Learning Datasets in Materials Science}, journal = {Journal of Open Source Software}
}
```

# Contributing
Foundry is an Open Source project and we encourage contributions from the community. To contribute, please fork from the `main` branch and open a Pull Request on the `main` branch. A member of our team will review your PR shortly.

## Developer notes
In order to enforce consistency with external schemas for the metadata and datacite structures ([contained in the MDF data schema repository](https://github.com/materials-data-facility/data-schemas)) the `dc_model.py` and `project_model.py` pydantic data models (found in the `foundry/jsonschema_models` folder) were generated using the [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/) tool. In order to ensure compliance with the flake8 linting, the `--use-annoted` flag was passed to ensure regex patterns in `dc_model.py` were specified using pydantic's `Annotated` type vs the soon to be deprecated `constr` type. The command used to run the datamodel-code-generator looks like:
```
datamodel-codegen --input dc.json --output dc_model.py --use-annotated
```

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

## Installation

Basic installation:
```bash
pip install foundry_ml
```

With optional features:
```bash
# For molecular data support
pip install foundry_ml[molecular]

# For PyTorch integration
pip install foundry_ml[torch]

# For TensorFlow integration
pip install foundry_ml[tensorflow]

# Install all optional dependencies
pip install foundry_ml[all]
```

## Development Installation

For development, you can install all dependencies including testing tools:

```bash
# Clone the repository
git clone https://github.com/MLMI2-CSSI/foundry.git
cd foundry

# Install in development mode with all extras
pip install -e .[all]

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest  # Run all tests
pytest --ignore=tests/test_molecular.py  # Skip tests requiring optional dependencies
```
