# Overview

Foundry is an open source machine learning platform for scientists. Our core services and software support dataset publication, running inference with pre-trained published models with cloud computing, and we are in the process of building a web interface that makes both data and models easy to use and share. Our collection of datasets and models primarily consists of datasets for materials science and chemistry, but we are continuing to expand to other scientific domains.

Foundry's functionality is built on a variety of existing services, bringing together useful tools and features into one easy-to-use platform. Our API layer facilitates communication with these other services through a unified interface (see Figure below). This is true for both researchers publishing data as well as data and model consumers.

![](../../.gitbook/assets/foundry-overview.png)

**Datasets:** For dataset publication, we use the [Materials Data Facility (MDF)](https://materialsdatafacility.org). Using Foundry alone, you can publish a dataset to Foundry's collection, which is made available via MDF storage resources. Because we use MDF as our data provider, the data are a made available and discoverable via MDF as well. We plan to add more data providers in the future.

**Models:** Model publishing and storage is made possible with [DLHub](https://www.dlhub.org). When publishing or running a model on Foundry, you'll use our interface to do so. Your published model will be a part of both Foundry and DLHub's collections.

**Access:** When a consumer wants to access a dataset or model, they'll use Foundry's interface. Behind the scenes, our API layer communicates with MDF to pull the data and DLHub to run the model. The consumer will only ever need to interact with Foundry to get everything they need.



