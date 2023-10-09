import logging
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
    
def internal_deduplication(dataset, split_name, column_name, expected_size, false_positive_rate):
    bloom_filter = ScalableBloomFilter(expected_size, false_positive_rate)
    dataset[split_name] = dataset[split_name].filter(lambda example: duplicates_filter(example, bloom_filter, column_name))
    return dataset

def external_deduplication(dataset_1, split_name_1, column_name_1, split_name_2, column_name_2, expected_size, false_positive_rate, dataset_2=None):
    bloom_filter = ScalableBloomFilter(expected_size, false_positive_rate)
    for row in tqdm(dataset_1[split_name_1], desc="Creating Bloom Filter"):
        bloom_filter.add(row[column_name_1])

    if dataset_2 != None:
        dataset_2[split_name_2] = dataset_2[split_name_2].filter(lambda example: example[column_name_2] not in bloom_filter)
    else:
        dataset_1[split_name_2] = dataset_1[split_name_2].filter(lambda example: example[column_name_2] not in bloom_filter)
    return dataset_1, dataset_2

    # --------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub_id_1", type=str, required=True)
    parser.add_argument("--hub_id_2", type=str)
    parser.add_argument("--split_1", type=str, required=True)
    parser.add_argument("--split_2", type=str)

    parser.add_argument("--column_name_1", type=str, default="text")
    parser.add_argument("--column_name_2", type=str, default="text")

    parser.add_argument("--split_1_internal_deduplication", action=argparse.BooleanOptionalAction)
    parser.add_argument("--split_2_internal_deduplication", action=argparse.BooleanOptionalAction)
    parser.add_argument("--push_to_hub_1", action=argparse.BooleanOptionalAction)
    parser.add_argument("--push_to_hub_2", action=argparse.BooleanOptionalAction)

    parser.add_argument("--expected_size", type=int, default=1000000)
    parser.add_argument("--false_positive_rate", type=float, default=0.000001)
    parser.add_argument("--streaming_mode", action=argparse.BooleanOptionalAction)

    parser.add_argument("--save_locally", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    # --------------------------

    # Loading different datasets
    ds1 = load_dataset(args.hub_id_1, streaming=args.streaming_mode)
    ds2 = load_dataset(args.hub_id_2, streaming=args.streaming_mode) if args.hub_id_2 and args.hub_id_1 != args.hub_id_2 else None

    # Internal split deduplication
    if args.split_1_internal_deduplication:
        logging.info(f" Starting - Internal deduplication split 1.")
        ds1 = internal_deduplication(ds1, args.split_1, args.column_name_1, args.expected_size, args.false_positive_rate)
        logging.info(f" Ending - Internal deduplication split 1.")

    if args.split_2_internal_deduplication:
        logging.info(f" Starting - Internal deduplication split 2.")
        if ds2 != None: 
            ds2 = internal_deduplication(ds2, args.split_2, args.column_name_2, args.expected_size, args.false_positive_rate)
        else:
            ds1 = internal_deduplication(ds1, args.split_2, args.column_name_2, args.expected_size, args.false_positive_rate)
        logging.info(f" Ending - Internal deduplication split 2.")

    # Deduplications of split
    if args.split_2:
        logging.info(f" Starting - External deduplication between split 1 and 2")
        ds1, ds2 = external_deduplication(ds1, args.split_1, args.column_name_1, args.split_2, args.column_name_2, args.expected_size, args.false_positive_rate, ds2)
        logging.info(f" Ending - External deduplication between split 1 and 2")
        
    # --------------------------

    logging.info(f" Final result dataset {args.hub_id_1}:\n {ds1}")
    if ds2: logging.info(f" Final result dataset {args.hub_id_2}:\n {ds2}")

    if args.push_to_hub_1:
        try:
            ds1.push_to_hub(args.hub_id_1+"_filter")
        except Exception as e:
            print("Failed to push to hub: ", e)
            ds1.save_to_disk(args.hub_id_1)
    if args.push_to_hub_2 and ds2 != None:
        try:
            ds2.push_to_hub(args.hub_id_2+"_filter")
        except Exception as e:
            print("Failed to push to hub: ", e)
            ds2.save_to_disk(args.hub_id_2)

    if args.save_locally:
        ds1.save_to_disk(args.hub_id_1)
        if ds2 != None: ds2.save_to_disk(args.hub_id_2)