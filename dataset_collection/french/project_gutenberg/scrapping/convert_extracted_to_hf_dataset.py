import datasets
import os


class DatasetConverter:
    def __init__(self, data_dir: str, save_dir: str):
        self.data_dir = data_dir
        self.save_dir = save_dir

    def convert(self):
        files = [file for file in os.listdir(self.data_dir) if file.endswith('-8.txt')]

        # Create an empty dataset
        def gen():
            for file in files:
                # Convert from latin-1 to utf-8
                with open(os.path.join(self.data_dir, file), 'r', encoding='latin-1') as f:
                    text = f.read()
                # Add the text to the dataset
                yield {'id': file[:-4], 'text': text}
        ds = datasets.Dataset.from_generator(gen)
        return ds

    def save(self, dataset, save_dir):
        dataset.save_to_disk(save_dir)


if __name__ == '__main__':
    # CLI arguments
    import argparse

    parser = argparse.ArgumentParser(description='Convert raw files from Project Gutenberg to HF dataset')
    parser.add_argument('--data_dir', type=str, help='Directory where the raw files are stored')
    parser.add_argument('--save_dir', type=str, help='Directory where the converted dataset will be saved')
    parser.add_argument('--hub_id', type=str, default=None, help='HF hub id to push the dataset to')
    args = parser.parse_args()
    converter = DatasetConverter(args.data_dir, args.save_dir)
    dataset = converter.convert()
    print(dataset)
    print("Copying the dataset to the save directory")
    converter.save(dataset, args.save_dir)
    if args.hub_id is not None:
        print("Pushing the dataset to the HF hub")
        dataset.push_to_hub(args.hub_id, private=True)
