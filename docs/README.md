# Getting started with Foundry

![](.gitbook/assets/foundry-purple%20%283%29.png)

## What is Foundry?

Foundry is a Python package that simplifies the discovery and usage of machine-learning ready datasets in materials science and chemistry. Foundry provides software tools that make it easy to load these datasets and work with them in local or cloud environments. Further, Foundry provides a dataset specification, and defined curation flows, that allow users to create new datasets for the community to use through this same interface.

## Installation

Foundry can be installed on any operating system with Python with pip

```text
pip install foundry-ml
```

### Globus

Foundry uses the Globus platform for authentication, search, and (optionally) to optimize data transfer operations. Here’s how it works and how to get set up:

1.  **Globus Account:**
    *   You'll need a Globus account. You can [create a free account](https://app.globus.org) using your institutional credentials, GlobusID, Google ID, ORCID iD, etc.

2.  **Authentication Process:**
    *   When you first initialize `Foundry()` (e.g., `f = Foundry()`), the library attempts to authenticate with Globus.
    *   **Interactive Environments (Default):** By default, Foundry will try to open a web browser, taking you to a Globus authentication page. After you successfully log in and grant consent, Globus will redirect you back to a local web server that Foundry starts temporarily on your machine (usually on `localhost` at a specific port) to capture an authentication code. Once the code is captured, the local server shuts down, and authentication is complete.
    *   **Tokens:** Successful authentication results in securing tokens from Globus, which are then used for accessing Foundry services (like search and data transfer). These tokens are typically long-lived but can expire. Foundry will attempt to refresh them automatically when needed. If a refresh fails (e.g., after a very long period of inactivity or if consents are revoked), you might need to re-authenticate.

3.  **Headless or Remote Environments:**
    *   If you are using Foundry on a remote server, a Jupyter Hub, Google Colab, or any environment where a browser cannot be automatically opened or a local redirect server cannot be reliably used, you need to modify the authentication flow:
        *   `f = Foundry(no_browser=True, no_local_server=True)`
    *   **`no_browser=True`**: Prevents Foundry from trying to automatically open a web browser. Instead, it will print a Globus authentication URL to your console. You must copy this URL and paste it into a browser on your local machine (or any machine where you can access a browser).
    *   **`no_local_server=True`**: After you authenticate in the browser via the URL provided, Globus will redirect you to a page displaying an authentication code. You must copy this code from your browser and paste it back into your terminal/notebook where Foundry is waiting for it.
    *   This two-parameter setup enables authentication in almost any environment.

4.  **Globus Connect Personal (GCP) _(Optional)_:**
    *   For the most efficient data transfers, especially for large datasets, Foundry can use Globus transfers. To enable your local machine (like a laptop or workstation) or a server to be a source or destination for Globus transfers, you can install [Globus Connect Personal](https://www.globus.org/globus-connect-personal).
    *   If you don't have GCP set up or prefer not to use Globus for transfers, you can initialize Foundry to use HTTPS for downloads:
        *   `f = Foundry(use_globus=False)`
    *   HTTPS downloads are universally compatible but may be slower than Globus transfers for large datasets or datasets with many files.
    *   Note: Even if `use_globus=False` is set for data transfers, Globus is still used for the initial authentication and for searching datasets.

## Project Support

This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure".

### Other Support

Foundry brings together many components in the materials data ecosystem. Including MAST-ML, the Data and Learning Hub for Science \(DLHub\), and The Materials Data Facility \(MDF\).

#### MAST-ML

This work was supported by the National Science Foundation \(NSF\) SI2 award No. 1148011 and DMREF award number DMR-1332851

#### The Data and Learning Hub for Science \(DLHub\)

This material is based upon work supported by Laboratory Directed Research and Development \(LDRD\) funding from Argonne National Laboratory, provided by the Director, Office of Science, of the U.S. Department of Energy under Contract No. DE-AC02-06CH11357. [https://www.dlhub.org](https://www.dlhub.org)

#### The Materials Data Facility

This work was performed under financial assistance award 70NANB14H012 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the [Center for Hierarchical Material Design \(CHiMaD\)](http://chimad.northwestern.edu). This work was performed under the following financial assistance award 70NANB19H005 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Materials Design \(CHiMaD\). This work was also supported by the National Science Foundation as part of the [Midwest Big Data Hub](http://midwestbigdatahub.org) under NSF Award Number: 1636950 "BD Spokes: SPOKE: MIDWEST: Collaborative: Integrative Materials Design \(IMaD\): Leverage, Innovate, and Disseminate". [https://www.materialsdatafacility.org](https://www.materialsdatafacility.org)

