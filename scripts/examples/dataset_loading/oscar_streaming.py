# Remote URL and builder file
from datasets import load_dataset
dataset = load_dataset('oscar-corpus/OSCAR-2301', "fr", split='train', streaming=True)
print(next(iter(dataset)))

