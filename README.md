
<picture>
  <source srcset="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-white.png" height=175" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/MLMI2-CSSI/foundry/main/assets/foundry-black.png" height="175">
</picture>

[![PyPI](https://img.shields.io/pypi/v/foundry_ml.svg)](https://pypi.python.org/pypi/foundry_ml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/tests.yml)
[![Tests](https://github.com/MLMI2-CSSI/foundry/actions/workflows/python-publish.yml/badge.svg)](https://github.com/MLMI2-CSSI/foundry/actions/workflows/python-publish.yml)
[![NSF-1931306](https://img.shields.io/badge/NSF-1931306-blue)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1931306&HistoricalAwards=false)
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

You can use the following code to import and instantiate Foundry-ML, then find and load a dataset.

```python
from foundry import Foundry
import pandas as pd # Optional: for handling search results as a DataFrame

# Initialize Foundry. 
# For remote environments (e.g., Google Colab, Binder), use:
# f = Foundry(no_browser=True, no_local_server=True)
# By default, Foundry uses the "mdf" index and Globus for data transfers.
# To disable Globus transfers (e.g., if Globus Connect Personal is not set up), use:
# f = Foundry(use_globus=False) 
f = Foundry() 

# Search for a dataset by DOI or query string
# This example uses a DOI. Searching by query (e.g., "elwood") also works.
dataset_doi = "10.18126/e73h-3w6n" # Example: Elwood Monomer Properties
results_df = f.search(dataset_doi)

if results_df.empty:
    print(f"Dataset with DOI {dataset_doi} not found.")
else:
    # Access the FoundryDataset object from the search results DataFrame
    # The DataFrame might contain multiple results if searching by query string.
    dataset = results_df.iloc[0].FoundryDataset

    # Display dataset metadata (if in a Jupyter environment, it renders as HTML)
    print(f"Dataset Name: {dataset.dataset_name}")
    # In Jupyter, just 'dataset' on a line would render its HTML representation:
    # dataset 

    # Load the actual data from the dataset
    # This might download files if not already cached.
    # 'load()' is an alias for 'get_as_dict()'.
    # Specify splits if the dataset has them (e.g., "train", "test").
    # The structure of 'data_splits' depends on the dataset's specific schema.
    try:
        data_splits = dataset.load() # Loads all available splits if `split` param is None
        
        # Example: Accessing data from a 'train' split (structure is dataset-dependent)
        # This part of the example assumes a specific dataset structure for demonstration.
        # You'll need to inspect 'data_splits.keys()' and the dataset's metadata
        # to understand how to access its specific contents.
        if "train" in data_splits:
            train_data = data_splits["train"]
            # Suppose train_data is a dict with 'input' and 'target' keys,
            # and 'input' itself is a dict containing 'imgs', 'metadata', etc.
            if isinstance(train_data, dict) and "input" in train_data and "target" in train_data:
                 # The following lines are highly specific to the original example's dataset structure
                 # and may not apply to the dataset "10.18126/e73h-3w6n".
                 # Adapt based on the actual structure of the loaded dataset.
                 # imgs = train_data['input'].get('imgs', {}) 
                 # desc = train_data['input'].get('metadata', {})
                 # coords = train_data['target'].get('coords', {})
                 print("Train data loaded successfully. Explore its structure.")
            else:
                 print(f"Train data structure: {type(train_data)}")
        else:
            print(f"No 'train' split found. Available splits: {list(data_splits.keys())}")

    except Exception as e:
        print(f"Error loading data: {e}")

```
*NOTE*: Foundry uses Globus for authentication and (by default) for efficient data transfers. If you run locally and don't want to install [Globus Connect Personal](https://www.globus.org/globus-connect-personal), you can initialize Foundry with `f = Foundry(use_globus=False)`. This will use HTTPS for downloads, which may be slower for large datasets. For cloud environments, initializing with `f = Foundry(no_browser=True, no_local_server=True)` enables a compatible authentication flow.

If running this code in a notebook and a `FoundryDataset` object is the last item in a cell, its metadata will be displayed as an HTML table:
<img width="903" alt="metadata" src="https://user-images.githubusercontent.com/16869564/197038472-0b6ae559-4a6b-4b20-88e5-679bb6eb4f5c.png">
*(Image shows an example of metadata display)*

Visualizing data (example assumes a specific image dataset structure):
```python
# This visualization example is illustrative and depends heavily on the dataset's structure.
# After loading data with `data_splits = dataset.load()`, 
# you would adapt the following based on the actual content of `data_splits`.

# For instance, if you loaded the original example's atomic position dataset:
# imgs = data_splits['train']['input']['imgs']
# coords = data_splits['train']['target']['coords']

# key_list = list(imgs.keys())[offset:n_images+offset] # Choose some images

# import matplotlib.pyplot as plt # Ensure plt is imported
# fig, axs = plt.subplots(1, n_images, figsize=(20,20))
# for i in range(n_images):
#     axs[i].imshow(imgs[key_list[i]])
#     axs[i].scatter(coords[key_list[i]][:,0], coords[key_list[i]][:,1], s=20, c='r', alpha=0.5)
# plt.show() # Display the plot
```
<img width="595" alt="Screen Shot 2022-10-20 at 2 22 43 PM" src="https://user-images.githubusercontent.com/16869564/197039252-6d9c78ba-dc09-4037-aac2-d6f7e8b46851.png">
*(Image shows an example of data visualization)*

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
