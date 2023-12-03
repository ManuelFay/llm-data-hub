import os
import argparse
import configue

from dataset_construction.utils import get_config_hash


def count_files(dataset_config, save_dir):

    dataset_config_hash = get_config_hash(dataset_config)
    folder_path = os.path.join(save_dir, "dataset_cache", dataset_config_hash)
    print(folder_path)
    counts = {}
    if os.path.exists(folder_path):
        splits = [split for split in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, split))]
        print(f"Found dataset {dataset_config.dataset_path} with splits: {splits}")

        for split in splits:
            files = [file for file in os.listdir(os.path.join(folder_path, split)) if file.endswith(".arrow")]
            print(f"Split {split} consists of {len(files)} files.")

            assert os.path.exists(os.path.join(folder_path, split, "dataset_info.json"))
            assert os.path.exists(os.path.join(folder_path, split, "state.json"))

            print("All files have been found")
            counts[split] = len(files)

    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/mock_testing.yaml")
    parser.add_argument("--save_dir", type=str, default=None)
    args = parser.parse_args()

    config = configue.load(args.config)["data_mix"]

    counts = []
    for dataset in config.datasets:
        counts.append(count_files(config.datasets[0], args.save_dir))

    train_files = sum(item['train'] for item in counts)
    test_files = sum(item['test'] for item in counts)

    print(train_files, test_files)

    # Todo: Finish the copying
    raise NotImplementedError("Script in WIP")
