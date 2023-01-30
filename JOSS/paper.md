---
title: 'Foundry-ML - Software and Services to Simplify Access to Machine
Learning Datasets and Models in Materials Science'

tags:
  - Python
  - Machine Learning
  - Artificial Intelligence
  - Materials Science
  - Data

authors:
  - name: KJ Schmidt
    orcid: 0000-0000-0000-0000
    equal-contrib: true 
    affiliation: "1, 2"
  - name: Aristana Scourtas
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2"
  - name: Marcus Schwarting
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 3
  - name: Isaac Darling
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 3
  - name: Ethan Truelove
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 3
  - name: Aadit Ambadkar
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 1
  - name: Ribhav Bose
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 1
  - name: Zoa Katok
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 1
  - name: Jingrui Wei
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 4  
  - name: Xiangguo Li
    orcid: 0000-0-0000-0000
    equal-contrib: false
    affiliation: 4  
  - name: Ryan Jacobs
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 4 
  - name: Michael Ferris
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 5  
  - name: Paul Voyles
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 4
  - name: Dane Morgan
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: 4
  - name: Ian Foster
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: "1, 2, 3"
  - name: Ben Blaiszik
    orcid: 0000-0000-0000-0000
    equal-contrib: false
    affiliation: "1, 2"

affiliations:
 - name: Globus, University of Chicago
   index: 1

 - name: Data Science and Learning Division, Argonne National Laboratory
   index: 2

 - name: Department of Computer Science, University of Chicago
   index: 3

 - name: Department of Materials Science and Engineering, University of Wisconsin-Madison
   index: 4

 - name: Department of Computer Science, University of Wisconsin-Madison
   
   index: 5

date: Feb 01, 2023

bibliography: paper.bib

---

# Summary

The application of open science and machine learning to science, engineering, and industry-relevant problems is a critical, component of cross-department U.S. AI strategy highlighted e.g., by the AI Initiative, the Year of Open Data, and Materials Genome Initiative. As of 2023, ML and data science approaches are becoming central to scientific and technological
advancement, with thousands of new scientific publications yearly[cite Blaiszik]. For this growth to translate more rapidly into applications and scientific impact, it's important for datasets to be easily accessible for training, retraining, reproducing, and verifying model usefulness on chosen tasks. However, the discovery of high-quality, curated datasets is a challenge.
<!-- Add references to -->

To overcome this dataset access challenge, we introduce Foundry-ML, a service to enable researchers a simple path to publish
and discover structured datasets for ML in science, specifically in materials science and chemistry. Foundry-ML consists of a Python client, a web app, and standardized metadata and file structure built on top of services including the Materials Data Facility[2], and Globus combined with Python software tooling, standardized metadata, to dramatically simplify data access patterns.

# Statement of need

The processes by which high-quality structured science datasets are published and accessed remains decentralized, without standards, and scattered with some exceptions (e.g., [@matbench, @moses, @moleculenet; @wei2021benchmark]). With Foundry-ML, we provide 1) a simple Python interface that allows users to access structured ML-ready materials science and chemistry datasets with just a few lines of code, 2) a prototype web based interface for dataset search and discovery, and 3) a place where users can publish their own ML-ready datasets in a self-service manner.

* Foundry-ML focuses foremost on accessibility and reproducibility. \autoref{fig1} shows an example of how, with just a few lines of code, researchers can access a curated collection of ML-ready datasets, the associated metadata describing the dataset contents, split details, and other information (e.g., number of entries). As of Q1 2023, we have collected and made available 30 datasets in the Foundry format with data represented in formats including tabular data (e.g., csv, Excel), key-value data (e.g, JSON), to image sets and hierarchical data (e.g., HDF5). 

<!-- Screenshot showing one use case -->
![A Foundry-ML use case for zeolite design. (a) A user instantiates the Foundry-ML Python client and loads the descriptive metadata using the DOI. (b) Descriptive metadata includes information about the keys included in the datasets, associated units, and a short description. The metadata also include information about the dataset including the associated splits (e.g., train, test, validate), and the amount of data included. (c) A user can then load the data using the `load_data` function. This function returns a Pandas or Dask dataframe for tabular data.  The zeolite dataset show here, its metadata, and the data itself from researchers Daniel Schwalba-Koda and Rafael Gomez-Bombarelli.\label{fig1}](JOSS-zeolite.png)

* Building on the Materials Data Facility [@mdf-2019; @mdf-2016], Foundry-ML users can upload large datasets (MDF supports multi-TB datases, with potentially millions of files), making them easy to share, use, and discover by the rest of the scientific community.

* A prototype web interface has been developed (\autoref{fig2}), listing all datasets with instructions on how to access them. 

* With interpretability in mind, we Foundry-ML datasets have required metadata (see \autoref{fig1}b) that are provided by the authors of each dataset. All metadata are stored in Globus Search [@globuspublish] to facilitate queries. Query helpers are provided through the Foundry-ML Python client.

![Foundry Website UI for browsing Datasets. This figure shows a web user interface for browsing available datasets with summary information about the datasets.\label{fig2}](foundry-datasets.png)

While the example presented here come from the domains of materials science and chemistry, Foundry-ML is ultimately designed to be domain agnostic. This
will allow the same software to be a part of solving similar problems across scientific domains.


<!-- Fix these refs (e.g., Zeolite, Logan's work...)  -->

to image sets 
<!-- Fix these refs (Northwestern, Wisconsin, ARPA-E.. ) -->
It has been successfully used in educational curricula [@foundrynanohub]
and by research teams at the University of Chicago, Argonne National Lab, the University of Toronto [@dmc], 3M [@mmm], the University of Wisconsin [@wei2021benchmark; @li2021graph], MIT [@schwalbe2021priori] \autoref{fig 2}, and more. In \autoref{fig 2}, we highlight a use case for the ML-guided design of organic structure–directing agents (OSDAs) to promote zeolite formation. With just a few lines of code and the dataset DOI \autoref{fig1}a, a researcher can load descriptive metadata \autoref{fig1}b to understand the dataset contents, and load the data \autoref{fig1}c for analysis and exploration.     

# Future Directions
 In future work, we intend to add capabilities to Foundry-ML that enable publication and connection of datasets with ML models creating a combined ecosystem of datasets and models. This work will be completed in collaboration with the new NSF project (#2209892) Garden: A FAIR Framework for Publishing and Applying AI Models for Translational Research in Science, Engineering, Education, and Industry.

# Documentation
To learn more, we have documentation available via GitBook at the following location [GitBook documentation](https://ai-materials-and-chemistry.gitbook.io/foundry/v/docs/). We also have made available a number of [example notebooks](https://github.com/MLMI2-CSSI/foundry/tree/main/examples) that show how to publish and retrieve Foundry-ML datasets. 

# Acknowledgements

This work was supported by the National Science Foundation under NSF Award Number: 1931306 "Collaborative Research: Framework: Machine Learning Materials Innovation Infrastructure". **MDF** This work was performed under the following financial assistance award 70NANB19H005 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Materials Design (CHiMaD).

# References
