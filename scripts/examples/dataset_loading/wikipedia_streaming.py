# Remote URL and builder file
from datasets import load_dataset
dataset = load_dataset('wikipedia', "20220301.fr", split='train', streaming=True)
print(next(iter(dataset)))

