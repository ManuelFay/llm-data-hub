from datasets import load_dataset

dataset = load_dataset("json", data_files="/home/manuel/Downloads/theses_fr_13_23.jsonl")
print(dataset)
dataset.push_to_hub("manu/theses_fr_2013_2023")
