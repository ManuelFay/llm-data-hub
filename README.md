# LLM Data Hub

This repository regroups code related to data gathering, data processing, and data analysis for the LLM training project.


## Installation

Requirements are not all necessary, to install all requirements, run the following command in  a virtual environment:
```bash
make init
```

## Data Gathering

For the moment, data is stored either on the HuggingFace Hub as a public dataset, 
or as a Git LFS file (uploaded to a private HuggingFace dataset repository). Storage is subject to change,
given the storage solutions available through the project partners.

New datasets should be added by creating a new folder in the `datasets` folder, and adding a `dataset.py` file responsible for downloading the data and processing it into a `Dataset` object.
This follows HuggingFace conventions for datasets, and allows for easy integration with the HuggingFace ecosystem.
The data format, post loading, should be standard across all datasets. 

Metadata should include:
- The dataset name
- The dataset description
- The dataset citation (if applicable)
- The dataset license (if applicable)
- The dataset homepage (if applicable)
- The dataset size
- The dataset languages


## Data Processing

Data processing is done through the `Dataset` class, which is a wrapper around a HuggingFace dataset.
Custom functions are implemented to perform the following tasks:
- Tokenization
- Data splitting
- Quality Filtering (OCR)
- Language Tagging
- Dealing with parallel data (across languages)
- Deduplication

## Data Analysis

Detailed statistics about the data can be computed through the data analysis module.
This stores the data in a `pandas` dataframe, and allows for easy plotting and analysis.
