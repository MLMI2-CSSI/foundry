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

<!-- to do: 
Update authors with ORCID ID's
fill out the equal-contrib part. There are other selections to choose from
-->

authors:
  - name: Aristana Scourtas
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2"
  - name: KJ Schmidt
    orcid: 0000-0000-0000-0000
    equal-contrib: true 
    affiliation: "1, 2"
  - name: Marcus Schwarting
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 3
  - name: Jingrui Wei
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 4  
    - name: Xiangguo Li
    orcid: 0000-0-0000-0000
    equal-contrib: true
    affiliation: 4  
    - name: Ryan Jacobs
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 4 
    - name: Michael Ferris
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 5  
    - name: Paul Voyles
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 4
     - name: Dane Morgan
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: 4
     - name: Ian Foster
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2, 3"
     - name: Ben Blaiszik
    orcid: 0000-0000-0000-0000
    equal-contrib: true
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

date: January 2023

bibliography: paper.bib

---

# Summary

Machine learning and data science approaches are becoming critical to scientific and technological
advancement, with thousands of new scientific publications yearly[?] and countless private companies relying on ML as critical aspects of their business models[?]. For this growth to translate into applications
and scientific impact, both datasets and models need to be easily accessible for training, retraining, reproducing, and verifying usefulness on chosen tasks. Unfortunately, the discovery of datasets, models,
and the underlying code is a challenge and often impossible task if they are not published openly[1].

To overcome this challenge, we introduce Foundry, a service to enable researchers a simple path to publish
and discover datasets for machine learning in science and to link these datasets to predictive models.
Foundry is a synthesis of service capabilities from the Materials Data Facility[2] and DLHub[3], layered
with Python software tooling, standardized metadata, and a file structure specification to meet the
needs of the machine learning community.

# Statement of need

The application of machine learning to science, engineering, and industry-relevant problems is a critical, well-recognized component of cross-department U.S. AI strategy, proposed as a new engine to
drive new technological innovation and economic prosperity across numerous diverse sectors. Yet, the
processes by which data and trained models are made available and the methods that used to measure
the fitness of these models remains decentralized, without standards, and scattered with a few notable
exceptions. This in turn makes it costly, and frequently impossible to 1)
identify models for a specific application, understanding it’s domain of relevance and quantitative 
performance; 2) reproduce work without expending months of effort; and 3) build upon previous results
without starting from scratch. While a number of separate services can be used and combined to fulfill
portions of the requisite workflow, Foundry offers end-to-end coverage from dataset publication,
model publication and deployment for inference on distributed computing, and benchmark challenge
creation.

Foundry focuses on accessibility, reproducibility, and collaboration within research. Users can upload large datasets and models to Foundry, making them easy to share, use, and discover by the rest of the scientific community.

For researchers looking to discover machine learning models and machine learning ready datasets, Foundry provides a curated collection of both. Users can access any Foundry dataset without barriers. All datasets are listed on the website with full instructions on how to use them. We believe in access to high quality data, so all of the datasets go through a curation process where an actual person assesses the data.

With interpretability in mind, we created required metadata that is completed by the authors of each dataset. All metadata is formatted the same way, so it's easy to understand across all of our content. Reproducibility efforts on the data side become almost trivial.

Foundry's infrastructure is designed for sharing large files, making collaboration easy.

Foundry is designed to be domain agnostic,
which allows our software to be a part of solving problems across scientific domains.
It has been successfully used by graduate students and researchers at the University of Wisconsin[4], MIT[5], and
the University of Chicago[6].
The level of accessibility, ease of use, and compute resources enable Foundry to further
exciting developments science.


# Citations

<!-- Notes to be organized before putting it all in the bib:

1. Reproducibility standards for machine learning in the life sciences

  Maybe also: 
  D. Morgan and R. Jacobs, “Opportunities and challenges for machine learning in materials science,”
  Annual Review of Materials Research, vol. 50, pp. 71–103, 2020

2. MDF paper(s) - 
  B. Blaiszik, L. Ward, M. Schwarting, J. Gaff, R. Chard, D. Pike, K. Chard, and I. Foster, “A data ecosys-
  tem to support machine learning in materials science,” MRS Communications, vol. 9, no. 4, pp. 1125–
  1133, 2019

  B. Blaiszik, K. Chard, J. Pruyne, R. Ananthakrishnan, S. Tuecke, and I. Foster, “The Materials Data
  Facility: Data services to advance materials science research,” Journal of Materials, 2016.

3. DLHub paper - 
  Z. Li, R. Chard, L. Ward, K. Chard, T. J. Skluzacek, Y. Babuji, A. Woodard, S. Tuecke, B. Blaiszik,
  and M. J. Franklin, “DLHub: Simplifying publication, discovery, and use of machine learning models in
  science,” Journal of Parallel and Distributed Computing, vol. 147, pp. 64–76, 2021.

4. UW paper (bandgaps or atom position finding) - 
  J. Wei, B. Blaiszik, D. Morgan, and P. Voyles, “Benchmark tests of atom-locating CNN models with a
  consistent dataset,” Microscopy and Microanalysis, vol. 27, no. S1, pp. 2518–2520, 2021.

  X.-G. Li, B. Blaiszik, M. E. Schwarting, R. Jacobs, A. Scourtas, K. Schmidt, P. M. Voyles, and D. Mor-
  gan, “Graph network based deep learning of bandgaps,” The Journal of Chemical Physics, vol. 155,
  no. 15, p. 154702, 2021

5. Zeolite paper

6. ?  

-->


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
