# Preprocessors

Preprocessors are used to preprocess the data before it is used for training. The preprocessing is done in the following order:
- Dataset specific preprocessing
- Global preprocessing

This folder contains the code for the global preprocessing, which is applied to all datasets.

## Usage

Preprocessors take in one or more `Dataset` class instances, apply operations on them, and return a `Dataset` class instance.
