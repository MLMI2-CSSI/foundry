# Overview

Foundry is an open source machine learning platform for scientists. Our core services are data storage, pre-trained models run with cloud computing, and an interface that makes both data and models easy to use and share.

Foundry primarily consists of datasets for materials science and chemistry, but we're continuing to expand to other areas.

Foundry's functionality is built on top of a variety of already existing services, bringing together useful tools and features into one easy-to-use platform. Our API layer facilitates communication with these other services, so the only platform users communicate with directly is Foundry. This is true for both publishing users as well as data and model consuming users.

For dataset storage and publishing, we currently use [Materials Data Facility \(MDF\)](https://materialsdatafacility.org/). Using Foundry alone, you can publish a dataset to Foundry's collection, which is stored on MDF. Because we use MDF as our data provider, the data is a part of MDF's collection as well. We plan to add more data providers in the future.

Model publishing and storage is made possible with [DLHub](https://www.dlhub.org/). When publishing or running a model on Foundry, you'll use our interface to do so. Your model will be a part of both Foundry and DLHub's collections.

When a consumer wants to access a dataset or model, they'll use Foundry's interface. Behind the scenes, our API layer communicates with MDF to pull the data and DLHub to run the model. The consumer will only ever need to interact with Foundry to get everything they need.



![](../.gitbook/assets/foundry-overview.png)



