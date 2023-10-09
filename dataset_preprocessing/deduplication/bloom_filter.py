import argparse
from pybloom_live import ScalableBloomFilter
from datasets import load_dataset
from tqdm import tqdm

def duplicates_filter(item, bloom_filter, column_name):
    if item[column_name] in bloom_filter:
        return False
    else:
        bloom_filter.add(item[column_name])
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hugging_face_id", type=str)
    parser.add_argument("--column_name", type=str, default="text")
    parser.add_argument("--expected_size", type=int, default=10000)
    parser.add_argument("--false_positive_rate", type=float, default=0.001)
    parser.add_argument("--deduplicate_test_split", action=argparse.BooleanOptionalAction)
    parser.add_argument("--streaming_mode", action=argparse.BooleanOptionalAction)
    parser.add_argument("--push_to_hub", action=argparse.BooleanOptionalAction)
    parser.add_argument("--save_locally", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    # --------------------------

    bloom_filter = ScalableBloomFilter(args.expected_size, args.false_positive_rate)
    ds = load_dataset(args.hugging_face_id, streaming=args.streaming_mode)
    
    # If dataset has a test split, we start by adding them to the bloom filter.
    if "test" in ds:
        # If we also want to deduplicate the test split.
        if args.deduplicate_test_split:
            ds["test"] = ds["test"].filter(lambda example: duplicates_filter(example, bloom_filter, args.column_name))
        else :
            for row in tqdm(ds["test"]):
                bloom_filter.add(row[args.column_name])

    # Then, we filter each item in the train split to remove it if it's a duplicate within the train split or if it's already in the test split.
    ds["train"] = ds["train"].filter(lambda example: duplicates_filter(example, bloom_filter, args.column_name))

    # --------------------------

    if args.push_to_hub:
        try:
            ds.push_to_hub(args.hugging_face_id)
        except Exception as e:
            print("Failed to push to hub: ", e)
            ds.save_to_disk(args.hugging_face_id)

    if args.save_locally:
        ds.save_to_disk(args.hugging_face_id)
        with open(f"{args.hugging_face_id}_bloom_filter", 'wb') as file:
            bloom_filter.tofile(file)