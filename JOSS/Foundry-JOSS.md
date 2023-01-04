# Foundry

---
title: 'Foundry - Software and Services to Simplify Access to Machine
Learning Datasets and Models in Materials Science'

tags:
  - Python
  - Machine Learning
  - Artificial Intelligence
  - Materials Science
  - Data

authors:
  - name: 
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2"
  - name: 
    orcid: 0000-0000-0000-0000
    equal-contrib: true 
    affiliation: "1, 2"
  - name: Author with no affiliation
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2"

affiliations:
 - name: University of Chicago
   
   index: 1
 - name: Argonne National Laboratory
   
   index: 2

date: January 2023

bibliography: paper.bib

---

# Summary

Machine learning and data science approaches are becoming critical to scientific and technological
advancement, with thousands of new scientific publications yearly and countless private companies 
relying on ML as critical aspects of their business models. For this growth to translate into applications
and scientific impact, both datasets and models need to be easily accessible for training, retraining, 
reproducing, and verifying usefulness on chosen tasks. Unfortunately, the discovery of datasets, models,
and the underlying code is a challenge and often impossible task if they are not published openly.

To overcome this challenge, we introduce Foundry, a service to enable researchers a simple path to publish
and discover datasets for machine learning in science and to link these datasets to predictive models.
Foundry is a synthesis of service capabilities from the Materials Data Facility and DLHub, layered
with Python software tooling, standardized metadata, and a file structure specification to meet the
needs of the machine learning community. We demonstrate the power of this approach by showcasing
simple examples from the broader machine learning community and two examples from the domains
of materials science and chemistry.

# Statement of need

The application of machine learning to science, engineering, and industry-relevant problems is a critical,
well-recognized component of cross-department U.S. AI strategy, proposed as a new engine to
drive new technological innovation and economic prosperity across numerous diverse sectors. Yet, the
processes by which data and trained models are made available and the methods that used to measure
the fitness of these models remains decentralized, without standards, and scattered with a few notable
exceptions. This in turn makes it costly, and frequently impossible to 1)
identify models for a specific application, understanding it’s domain of relevance and quantitative 
performance; 2) reproduce work without expending months of effort; and 3) build upon previous results
without starting from scratch. While a number of separate services can be used and combined to fulfill
portions of the requisite workflow [2,3], Foundry offers end-to-end coverage from dataset publication,
model publication and deployment for inference on distributed computing, and benchmark challenge
creation.

Foundry is designed to be domain agnostic,
which allows our software to be a part of solving these problems across scientific domains.
It has been successfully used by graduate students and researchers at the University of Wisconsin, MIT, and
the University of Chicago.
The level of accessibility, ease of use, and compute resources enable Foundry to further
exciting developments science.


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from 

# References
