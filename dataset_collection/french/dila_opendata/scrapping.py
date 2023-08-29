import os
import json
import tarfile
import xml.etree.ElementTree as ET
import shutil
import logging
from tqdm import tqdm
import pandas as pd
import argparse

# Walk all files in a directory using os.walk

logging.basicConfig(level=logging.WARNING)


def extract_all_text_from_node(node):
    text = ""
    for child in node:
        if child.text:
            text += child.text
        text += extract_all_text_from_node(child)
    return text


def explore_node(path, write_path: str):
    for root, dirs, files in tqdm(os.walk(path), desc=f"Exploring {path}"):
        for file in files:
            # Unzip
            if file.endswith(".taz") or file.endswith(".tar.gz"):
                folder_path = os.path.join(root, file).replace(".tar.gz", "").replace(".taz", "")
                # rename as tar.gz
                if file.endswith(".taz"):
                    logging.info(f"Extracting {os.path.join(root, file)}")
                    tar = tarfile.open(os.path.join(root, file), "r:gz")
                    tar.extractall(path=folder_path)
                    tar.close()
                if file.endswith(".tar.gz"):
                    logging.info(f"Extracting {os.path.join(root, file)}")
                    tar = tarfile.open(os.path.join(root, file), "r:gz")
                    tar.extractall(path=folder_path)
                    tar.close()
                    # os.remove(os.path.join(root, file))

                # Depth first exploration
                explore_node(folder_path, write_path)
                # Delete after extraction
                shutil.rmtree(folder_path)

            # Read XML files
            if file.endswith(".xml"):
                parsed_doc = {}
                # parse xml file to keep text only
                try:
                    tree = ET.parse(os.path.join(root, file))
                    root_xml = tree.getroot()
                except:
                    logging.warning(f"Could not parse {os.path.join(root, file)}")
                    continue
                for child in root_xml:
                    if child.tag == "CONTEXTE":
                        parsed_doc["headers"] = extract_all_text_from_node(child)
                    if child.tag == "BLOC_TEXTUEL":
                        parsed_doc["body"] = extract_all_text_from_node(child)
                        parsed_doc["path"] = os.path.join(root, file)

                if "body" not in parsed_doc:
                    parsed_doc = {}
                elif parsed_doc["body"].replace("\n", "").strip() == "":
                # check if empty body or \n only
                    parsed_doc = {}

                # if parsed_doc == {}:
                #     # Plan B, extract everything
                #     parsed_doc["all"] = extract_all_text_from_node(root_xml)
                #

                # Write to JSONL file
                if parsed_doc != {}:
                    # print(f"Writing {parsed_doc['path']}")
                    logging.info(f"Writing {parsed_doc['path']}")
                    with open(write_path, "a+") as f:
                        f.write(json.dumps(parsed_doc) + "\n")


# def jsonl_to_pandas(jsonl_path: str):
#
#     df = pd.read_json(jsonl_path, lines=True)
#     # rename columns: headers -> title, body -> text
#     df = df.rename(columns={"headers": "title", "body": "text"})
#     # remove duplicates
#     df = df.drop_duplicates(subset=["text"])
#     # remove empty texts
#     df = df[df["text"] != ""]
#
#     return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_path", type=str, default="./")
    parser.add_argument("--save_dir", type=str, default="./")
    parser.add_argument("--prefix", type=str, default="dila")
    parser.add_argument("--hub_id", type=str, default="manu/dila_opendata")
    args = parser.parse_args()

    save_path = os.path.join(args.save_dir, f"{args.prefix}_opendata.jsonl")
    if os.path.exists(save_path):
        os.remove(save_path)
    explore_node(args.base_path, save_path)

    from datasets import load_dataset

    dataset = load_dataset("json", data_files=save_path)
    dataset = dataset.remove_columns(["path"])
    dataset = dataset.rename_column("headers", "title")
    dataset = dataset.rename_column("body", "text")
    dataset.push_to_hub(args.hub_id)

    # logging.info(f"Converting {save_path} to csv")
    # jsonl_to_pandas(save_path).to_csv(os.path.join(args.save_dir, f"{args.prefix}_opendata.csv"))
