import datasets
import os
import re


class DatasetConverter:
    def __init__(self, data_dir: str, save_dir: str):
        self.data_dir = data_dir
        self.save_dir = save_dir

    @staticmethod
    def text_parser(text):
        # Remove the first line
        a = re.findall(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n((.*\n){1,4})\n\d+\n', text)
        a = [x[0] for x in a]
        return "\n".join(a)

    def convert(self):
        # list all .srt files in subdirectories
        srt_files = []
        for root, dirs, files in os.walk(self.data_dir, topdown=False):
            for name in files:
                if name.endswith(".srt"):
                    srt_files.append(os.path.join(root, name))

        # Create an empty dataset
        def gen():
            for file in srt_files:
                try:
                    with open(os.path.join(file), 'r', encoding="utf-8") as f:
                        text = f.read()
                        text = self.text_parser(text)
                    # Add the text to the dataset
                    yield {'id': file[:-4], 'text': text}
                except:
                    pass
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
    print(dataset[0])
    print("Copying the dataset to the save directory")
    converter.save(dataset, args.save_dir)
    if args.hub_id is not None:
        print("Pushing the dataset to the HF hub")
        dataset.push_to_hub(args.hub_id, private=True)
