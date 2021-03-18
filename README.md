# README

![](.gitbook/assets/foundry.png)

Foundry is a Python package that simplifies the discovery and usage of machine-learning ready datasets in materials science and chemistry. Foundry provides software tools that make it easy to load these datasets and work with them in local or cloud environments. Further, Foundry provides a dataset specification, and defined curation flows, that allow users to create new datasets for the community to use through this same interface.

## Installation

Foundry can be installed via pip with:

`pip install foundry-ml`

## Example Usage

The Foundry client can be used to access datasets using a `source_id`, e.g. here "\_test\_foundry\_fashion\_mnist\_v1.1":

```python
from foundry import Foundry
f = Foundry()
f = f.load("_test_foundry_fashion_mnist_v1.1")
```

This will remotely load the necessary metadata as well as download the data to local storage if it is not already present. To ensure successful data download, have a Globus endpoint [setup](https://www.globus.org/globus-connect-personal) on your machine. Once the data is accessible locally, load the data into the client:

```python
X, y = f.load_data()
```

The data is then usable:

```python
n_cols = 6
display_shape = (28,28)
fig, ax = plt.subplots(1,n_cols)

for i in range(0, n_cols):
    ax[i].imshow(X[i].reshape(display_shape), cmap='gray')
```

This example can be found in `examples/fashion-mnist/`.

#### Other uses

To just download the data without loading the additional metadata:

```python
f = Foundry().download("_test_foundry_fashion_mnist_v1.1")
```

While it is strongly recommended to load metadata remotely, it can be done locally with a `foundry_metadata.json` file:

```python
f = Foundry().from_file()
```

## Using Foundry on Cloud Computing Resources

Foundry works with common cloud computing providers like the NSF sponsored Jetstream and Google Colab. When instantiating the Foundry client, simple add the following arguments to use a compatible authentication flow.

```python
f = Foundry(no_browser=True, no_local_server=True)
```

When downloading data, add the following argument to download contents by HTTPS. This method may be non-performant for large datasets

```python
f.download(globus=False)
```

## Primary Support

This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure".

## Other Support

Foundry brings together many components in the materials data ecosystem. Including MAST-ML, the Data and Learning Hub for Science \(DLHub\), and The Materials Data Facility \(MDF\).

### MAST-ML

This work was supported by the National Science Foundation \(NSF\) SI2 award No. 1148011 and DMREF award number DMR-1332851

### The Data and Learning Hub for Science \(DLHub\)

This material is based upon work supported by Laboratory Directed Research and Development \(LDRD\) funding from Argonne National Laboratory, provided by the Director, Office of Science, of the U.S. Department of Energy under Contract No. DE-AC02-06CH11357. [https://www.dlhub.org](https://www.dlhub.org)

### The Materials Data Facility

This work was performed under financial assistance award 70NANB14H012 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the [Center for Hierarchical Material Design \(CHiMaD\)](http://chimad.northwestern.edu). This work was performed under the following financial assistance award 70NANB19H005 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Materials Design \(CHiMaD\). This work was also supported by the National Science Foundation as part of the [Midwest Big Data Hub](http://midwestbigdatahub.org) under NSF Award Number: 1636950 "BD Spokes: SPOKE: MIDWEST: Collaborative: Integrative Materials Design \(IMaD\): Leverage, Innovate, and Disseminate". [https://www.materialsdatafacility.org](https://www.materialsdatafacility.org)

## Documentation

Formal documentation is currently under development. You may see the Foundry documentation thus far [here](https://foundry.readthedocs.io/en/latest/?).

### Building the documentation locally

#### Instructions for developers

Foundry documentation is built and served by [Read the Docs](https://docs.readthedocs.io/en/stable/). To run a local build and generate the HTML files on your local machine, you need to install [Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html):

```text
pip install sphinx
```

When you clone the Foundry repo, there should be a `/docs` directory with all the relevant files, including a Makefile and a `/source` subdirectory.

To generate the build files, from the root of the `/docs` subdirectory run

```text
make html
```

Now, under `/docs/build/html` you should find the necessary HTML files. Open `index.html` in your browser to view the documentation.

Between changes to `confy.py` or associated source files, it's good practice to run `make clean` before running `make html`.

