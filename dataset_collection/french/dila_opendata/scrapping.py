import os
import json
import tarfile
import xml.etree.ElementTree as ET
import shutil
import logging
from tqdm import tqdm
import argparse

# Walk all files in a directory using os.walk

logging.basicConfig(level=logging.WARNING)


def extract_text_from_node(x):
    if x.text:
        if x.text.strip() != "":
            return x.text + "\n"
    if x.tail:
        if x.tail.strip() != "":
            return x.tail + "\n"
    return ""


def extract_all_text_from_node(node, whitelist=None):
    if whitelist and (node.tag in whitelist):
        return extract_all_text_from_node(node)

    text = ""
    for child in node:
        if (child.text or child.tail) and ((whitelist and child.tag in whitelist) or (not whitelist)):
            text += extract_text_from_node(child)
        text += extract_all_text_from_node(child, whitelist=whitelist)
    return text


def explore_node(path, write_path: str, mode=None):
    for root, dirs, files in tqdm(os.walk(path), desc=f"Exploring {path}"):
        for file in files:
            # Unzip
            if file.endswith(".taz") or file.endswith(".tar.gz"):
                folder_path = os.path.join(root, file).replace(".tar.gz", "").replace(".taz", "")
                # rename as tar.gz
                if file.endswith(".taz"):
                    logging.info(f"Extracting {os.path.join(root, file)}")
                    # uncompress from command line
                    # os.system(f"zcat {os.path.join(root, file)} | tar -xvf -")
                    # mkdir folder_path
                    os.system(f"mkdir {folder_path}")
                    os.system(f"tar -zxvf {os.path.join(root, file)} -C {folder_path}")

                    # tar = tarfile.open(os.path.join(root, file), "r:gz")
                    # tar.extractall(path=folder_path)
                    # tar.close()
                if file.endswith(".tar.gz"):
                    logging.info(f"Extracting {os.path.join(root, file)}")
                    tar = tarfile.open(os.path.join(root, file), "r:gz")
                    tar.extractall(path=folder_path)
                    tar.close()
                    # os.remove(os.path.join(root, file))

                # Depth first exploration
                explore_node(folder_path, write_path, mode=mode)
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

                parsed_doc = {}
                parsed_doc["path"] = os.path.join(root, file)
                parsed_doc["body"] = dataset_specific_parser(root_xml, mode=mode)
                if parsed_doc["body"].replace("\n", "").strip() == "":
                    parsed_doc = {}

                # Write to JSONL file
                if parsed_doc != {}:
                    # print(f"Writing {parsed_doc['path']}")
                    logging.info(f"Writing {parsed_doc['path']}")
                    with open(write_path, "a+") as f:
                        f.write(json.dumps(parsed_doc) + "\n")


def dataset_specific_parser(child, mode):
    if mode == "KALI":
        return extract_all_text_from_node(child, whitelist=["CONTENU"])
    if mode == "QR":
        return extract_all_text_from_node(child, whitelist=["TEXTE_QUESTION", "TEXTE_REPONSE", "Texte_Reponse", "Texte_Question"])
    if mode == "LEGI":
        headers = extract_all_text_from_node(child, whitelist=["CONTEXTE"])
        return extract_all_text_from_node(child, whitelist=["BLOC_TEXTUEL"])
    if mode == "CNIL":
        return extract_all_text_from_node(child, whitelist=["CONTENU"])
    return extract_all_text_from_node(child)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_path", type=str, default="./")
    parser.add_argument("--save_dir", type=str, default="./")
    parser.add_argument("--prefix", type=str, default="dila")
    parser.add_argument("--hub_id", type=str, default=None)
    args = parser.parse_args()

    save_path = os.path.join(args.save_dir, f"{args.prefix}_opendata.jsonl")
    if os.path.exists(save_path):
        os.remove(save_path)
    print(f"Saving to {save_path}")
    explore_node(args.base_path, save_path, mode=args.prefix.upper())

    if args.hub_id:
        from datasets import load_dataset
        dataset = load_dataset("json", data_files=save_path)
        # dataset = dataset.rename_column("headers", "title")
        dataset = dataset.rename_column("path", "id")
        dataset = dataset.rename_column("body", "text")
        try:
            dataset.push_to_hub(args.hub_id)
        except Exception as e:
            print("Failed to push to hub: ", e)
            dataset.save_to_disk(os.path.join(args.save_dir, f"{args.prefix}_opendata"))

    # logging.info(f"Converting {save_path} to csv")
    # jsonl_to_pandas(save_path).to_csv(os.path.join(args.save_dir, f"{args.prefix}_opendata.csv"))
