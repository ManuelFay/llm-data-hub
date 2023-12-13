import datasets
import os
import re
import argparse


def create_dataset(data_dir):
    def align_data():
        for path in os.listdir(data_dir):
            if path.startswith("cometkiwi_metadata_"):
                ending = re.match("cometkiwi_metadata_(.*)", path).group(1)

                fr_path = os.path.join(data_dir, f"cometkiwi_data_{ending}.en-fr.fr")
                en_path = os.path.join(data_dir, f"cometkiwi_data_{ending}.en-fr.en")
                metadata_path = os.path.join(data_dir, f"cometkiwi_metadata_{ending}")
                assert os.path.isfile(fr_path)
                assert os.path.isfile(en_path)
                assert os.path.isfile(metadata_path)

                # concatenate all lines from the 3 files on a single line
                with open(fr_path, 'r') as file_fr, open(en_path, 'r') as file_en, open(metadata_path,
                                                                                        'r') as file_metadata:
                    for line_a, line_b, line_meta in zip(file_fr, file_en, file_metadata):
                        yield {"fr": line_a.strip(), "en": line_b.strip(), "source": line_meta.strip()}

    dataset = datasets.Dataset.from_generator(
        align_data
    )
    return dataset

if __name__ == "__main__":
    argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="Path to the directory containing the data")
    parser.add_argument("--output_dir", type=str, help="Path to the directory where the dataset will be saved")
    parser.add_argument("--hub_id", type=str, help="Hub ID of the dataset", default=None)

    args = parser.parse_args()

    dataset = create_dataset(args.data_dir)
    dataset.save_to_disk(args.output_dir)
    if args.hub_id is not None:
        dataset.push_to_hub(args.hub_id)
