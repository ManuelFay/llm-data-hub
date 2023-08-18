# Local builder file
from datasets import load_dataset
dataset = load_dataset('./dataset_collection/french/oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
print(next(iter(dataset)))

# Remote URL and builder file
from datasets import load_dataset
dataset = load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
print(next(iter(dataset)))

