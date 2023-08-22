# Local builder file
from datasets import load_dataset, load_from_disk
dataset = load_from_disk('./dataset_collection/french/french_open_subtitles/data/formatted')
print(next(iter(dataset)))


# Remote URL and builder file
from datasets import load_dataset
dataset = load_dataset('manu/french_open_subtitles', split='train', streaming=True, use_auth_token=True)
print(next(iter(dataset)))



