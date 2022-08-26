# Introduction and Installation

![](<../.gitbook/assets/foundry-purple (2).png>)

## What is Foundry?

Foundry is a Python package that simplifies the discovery and usage of machine-learning ready datasets and published models in materials science and chemistry. We provide software tools that make it easy to load datasets and work with them in local or cloud environments and to perform inference using published ML models.&#x20;

**Capability Status:** Researchers can contribute by publishing new [datasets](publishing/publishing-datasets.md) and [models](under-development/publishing-models.md) through a self-service publication process. Our dataset capabilities are currently in **production** and our model capabilities are still **in development**.

## Installation

Foundry can be installed on any operating system with Python with pip

```
pip install foundry-ml
```

### Globus

We use the Globus platform for authentication and optimization of some data transfer operations. Follow the steps below to get set up.

* [Create a free account.](https://app.globus.org) You can create a free account here with your institutional credentials or with free IDs (GlobusID, Google, ORCID, etc).
* [Set up a Globus Connect Personal endpoint ](https://www.globus.org/globus-connect-personal)_**(optional)**_. While this step is optional, some Foundry capabilities will work more efficiently when using Globus Connect Personal (GCP).

## Now you're ready to publish or access data&#x20;

Keep the momentum going with our [loading data section](examples.md) or [publishing guide](publishing/publishing-datasets.md).
