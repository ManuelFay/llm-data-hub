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

New datasets should be added by creating a new folder in the `datasets` folder, and adding a `[folder_name].py` file responsible for downloading the data and processing it into a `Dataset` object.
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

Ideally, the dataset should be streamable for easy processing and debugging, but this is not a requirement and 
having a smaller dummy dataset for debugging purposes is acceptable.

A usage example should be included in the folder.

### Warnings

Larger datasets such as OSCAR or Wikipedia can be used in streaming mode.
In streaming mode, modifications to the [dataset].py file will not be reflected in the dataset, as the dataset is downloaded from the HuggingFace Hub at each run.

To run locally, the dataset should be downloaded and stored locally, and the `streaming` flag should be set to `False` in load_dataset() function.
A beam runner should be specified (Spark, Dataflow, etc.), or the "direct" runner should be used for smaller datasets.

Note that operations can still be done on a streamed dataset https://huggingface.co/docs/datasets/stream in order 
to format data to be coherent with the rest of the datasets.

## Data Processing

Data processing is done through the `Dataset` class, which is a wrapper around a HuggingFace dataset.
Custom functions are implemented to perform the following tasks:
- [ ] Tokenization
- [ ] Quality Filtering (OCR)
- [ ] Language Tagging
- [ ] Dealing with parallel data (across languages)
- [ ] Deduplication
- [ ] Dataset Aggregation
- [ ] Splitting into train, validation, and test sets

## Data Analysis

Detailed statistics about the data can be computed through the data analysis module.
This stores the data in a `pandas` dataframe, and allows for easy plotting and analysis.

## Tests

```bash
make test
```