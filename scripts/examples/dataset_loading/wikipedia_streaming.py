# Remote URL and builder file
from datasets import load_dataset
dataset = load_dataset('wikipedia', "20220301.fr", split='train', streaming=True)
# print(next(iter(dataset)))

# Wrap the dataset with a pytorch dataloader
from torch.utils.data import DataLoader
dataloader = DataLoader(dataset, batch_size=2, num_workers=4)

from tqdm import tqdm
# Calculate the number of words
num_words = 0
for batch in tqdm(dataloader):
    num_words += len(" ".join(batch['text']).split())
print(num_words)
