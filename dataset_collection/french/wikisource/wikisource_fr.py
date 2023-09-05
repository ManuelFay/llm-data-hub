import datasets
from datasets import load_dataset
from tqdm import tqdm


def gen():
    for i in tqdm(range(24)):
        ds = load_dataset("bigscience-data/roots_fr_wikisource",
                          data_files=f"data/train-000{i:02d}-of-00024.parquet",
                          split="train",
                          verification_mode='no_checks',
                          streaming=True)
        for sample in ds:
            yield {'id': eval(sample['meta'])['title'], 'text': sample['text']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert raw files from Wikisource to HF dataset')
    parser.add_argument('--hub_id', type=str, default=None, help='HF hub id to push the dataset to')
    args = parser.parse_args()
    final_ds = datasets.Dataset.from_generator(gen)
    final_ds.push_to_hub(args.hub_id)

