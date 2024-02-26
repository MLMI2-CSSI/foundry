# Introduction and Installation

<figure><img src=".gitbook/assets/foundry-logo-new.png" alt=""><figcaption></figcaption></figure>

## What is Foundry?

Foundry is a Python package that simplifies the discovery and usage of machine-learning ready datasets in materials science and chemistry. We provide software tools that make it easy to load datasets and work with them in local or cloud environments.&#x20;

**Capability Status:** Researchers can contribute by publishing new [datasets](publishing/publishing-datasets.md) through a self-service publication process. Our dataset capabilities are currently in **production.**

## Installation

Foundry can be installed on any operating system with Python with pip

```
pip install foundry-ml
```

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td></td><td>Use Datasets</td><td></td><td><a href="loading-and-using/examples.md">examples.md</a></td><td><a href=".gitbook/assets/foundry-down.png">foundry-down.png</a></td></tr><tr><td></td><td>Publish Datasets</td><td></td><td><a href="publishing/publishing-datasets.md">publishing-datasets.md</a></td><td><a href=".gitbook/assets/foundry-up.png">foundry-up.png</a></td></tr></tbody></table>

### Globus

We use the Globus platform for authentication and optimization of some data transfer operations. Follow the steps below to get set up.

* [Create a free account.](https://app.globus.org) You can create a free account here with your institutional credentials or with free IDs (GlobusID, Google, ORCID, etc).
* [Set up a Globus Connect Personal endpoint ](https://www.globus.org/globus-connect-personal)_**(optional)**_. While this step is optional, some Foundry capabilities will work more efficiently when using Globus Connect Personal (GCP).
