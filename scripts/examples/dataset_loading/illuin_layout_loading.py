# Local builder file
from datasets import load_dataset
dataset = load_dataset('./dataset_collection/french/illuin_layout_dataset', split='train', streaming=False)
# push to hub
# dataset.push_to_hub('manu/illuin_layout_dataset_text_only', private=True)
print(next(iter(dataset)))


# Remote URL and builder file
from datasets import load_dataset
dataset = load_dataset('manu/illuin_layout_dataset_text_only', split='train', streaming=True, use_auth_token=True)
print(next(iter(dataset)))



