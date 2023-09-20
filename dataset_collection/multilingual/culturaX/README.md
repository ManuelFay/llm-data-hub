# CulturaX

Large Multilingual Dataset made of Oscar and mC4 texts, hosted on the [HuggingFace Hub](https://huggingface.co/datasets/uonlp/CulturaX).

In French, the dataset contains 319.3B tokens.


```python
from datasets import load_dataset
ds = load_dataset("uonlp/CulturaX", "fr")
```