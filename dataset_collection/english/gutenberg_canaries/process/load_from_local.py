# load zip data as a local hf dataset

from datasets import load_from_disk, Value
# zipfile to decompress
# from zipfile import ZipFile

# # unzip the dataset
# PATH = 'dataset_collection/english/gutenberg_canaries/data/gutenberg_canaries.zip'
#
# with ZipFile(PATH, 'r') as zipObj:
#     zipObj.extractall('dataset_collection/english/gutenberg_canaries/data/')

# load the dataset
dataset = load_from_disk('dataset_collection/english/gutenberg_canaries/data/gutenberg_canaries')
# set id column to string type
dataset = dataset.cast_column("id", Value("string"))

# print the dataset
print(dataset)
# print the first sample
print(dataset[0])




# push the dataset to the hub
dataset.push_to_hub('manu/gutenberg_canaries', private=True)
