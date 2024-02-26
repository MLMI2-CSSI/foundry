# About Foundry-ML

Foundry is an open source machine learning platform for scientists. Our core services and software support dataset publication and a web interface that makes data easy to use and share. Our collection of datasets primarily consists of datasets for materials science and chemistry, but we are continuing to expand to other scientific domains.

Foundry's functionality is built on a variety of existing services, bringing together useful tools and features into one easy-to-use platform. Our API layer facilitates communication with these other services through a unified interface. This is true for both researchers publishing data as well as data consumers.

**Datasets:** For dataset publication, we use the [Materials Data Facility (MDF)](https://materialsdatafacility.org/). Using Foundry alone, you can publish a dataset to Foundry's collection, which is made available via MDF storage resources. Because we use MDF as our data provider, the data are a made available and discoverable via MDF as well. We plan to add more data providers in the future.

{% hint style="info" %}
When datasets are published you will receive a [Digital Object Identifier (DOI) ](https://en.wikipedia.org/wiki/Digital\_object\_identifier)to enable citation of the research artifact
{% endhint %}



**Access:** When a consumer wants to access a dataset, they'll use Foundry's interface. Behind the scenes, our API layer communicates with MDF to pull the data (via HTTPS or Globus). The consumer will only ever need to interact with Foundry to get everything they need.
