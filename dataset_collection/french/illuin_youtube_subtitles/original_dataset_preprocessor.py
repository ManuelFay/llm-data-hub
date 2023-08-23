from datasets import load_dataset, Dataset, DatasetDict


def get_youtube(dataset_path, split="train"):
    youtube = load_dataset(dataset_path, split=split)
    youtube = youtube.to_pandas()
    youtube = youtube.sort_values(by=['video_path', 'start_timestamp'])
    youtube = youtube.groupby('video_path')['sentence'].apply(' '.join).reset_index()
    youtube = youtube[['video_path', 'sentence']]
    # deduplicate by sentence
    youtube = youtube.drop_duplicates(subset=['sentence'])
    youtube = Dataset.from_pandas(youtube)
    youtube = youtube.remove_columns(list(set(youtube.column_names) - {"sentence"} - {"video_path"}))
    # rename features to match the ones from the other datasets
    youtube = youtube.rename_column("sentence", "text")
    youtube = youtube.rename_column("video_path", "id")
    return youtube


if __name__ == "__main__":
        # get the dataset
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dataset_path", type=str, help="Path to the raw dataset")
    parser.add_argument("--hub_id", type=str, help="Hub id to push the dataset to")
    args = parser.parse_args()
    df_train = get_youtube(split="train")
    df_test = get_youtube(split="test")
    # combine the two datasets into a train and test set within the same dataset
    df = DatasetDict({"train": df_train, "test": df_test})
    print(df["train"][0])
    df.push_to_hub(args.hub_id)
