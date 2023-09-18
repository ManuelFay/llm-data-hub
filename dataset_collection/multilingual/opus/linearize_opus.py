import random
from datasets import load_dataset


def linearize_row(row):
    dict = row["translation"]
    languages = list(dict.keys())
    translation, original = (dict[languages[0]], dict[languages[1]]) if random.random() > 0.5 else (
    dict[languages[1]], dict[languages[0]])
    return {"id": hash(row["translation"][languages[0]]), "text": f"{translation}\t{original}"}


def linearize_dataset(dataset, subset):
    dataset = load_dataset(dataset, subset, streaming=False)
    dataset = dataset.map(linearize_row)
    dataset = dataset.remove_columns(["translation"])
    return dataset


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="opus100")
    parser.add_argument("--subset", type=str, default="en-fr")
    parser.add_argument("--hub_id", type=str, default="manu/opus100-en-fr")
    args = parser.parse_args()

    ds = linearize_dataset(args.dataset, args.subset)
    ds.push_to_hub(args.hub_id)
