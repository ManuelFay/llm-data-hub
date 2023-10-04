import os
import re
import json
import docx
import shutil
import zipfile
import tarfile
import logging
import argparse
import xml.etree.ElementTree as ET
from datasets import load_dataset
from tqdm import tqdm

def clean_text(text, mode=None):
    cleaned_text = text.strip()
    if len(cleaned_text) >= 30:
        if mode:
            if mode=="DEBATS":
                replacements = {'\u0080': ' ', '\u0082': ' '}
                cleaned_text = ''.join(replacements.get(char, char) for char in text)
            elif mode in ["BALO", "JORF"]:
                cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
                cleaned_text = re.sub(r"'\s+", "'", cleaned_text)
        return cleaned_text
    else: return ""

# ------------------------------------

def extract_text_from_node(x, mode=None):
    if x.text and x.text.strip() != "":
        return x.text + "\n"
    elif x.tail and x.tail.strip() != "":
        return x.tail + "\n"
    return ""

def explore_nodes(node, whitelist=None, mode=None):
    if whitelist and node.tag in whitelist:
    # This gives all the child nodes under the nested tags
        return explore_nodes(node, mode=mode)

    text = ""
    for child in node:
        if (child.text or child.tail) and ((not whitelist) or (child.tag in whitelist)):
            text += extract_text_from_node(child, mode)
        text += explore_nodes(child, whitelist=whitelist, mode=mode)
    return text


def xml_parser(child, mode):
    if mode in ["KALI", "CNIL", "CAPP", "CASS", "CONSTIT", "INCA", "JADE", "JORF", "DOLE", "SARDE"]:
        return explore_nodes(child, whitelist=["CONTENU"])
    elif mode == "QR":
        return explore_nodes(child, whitelist=["TEXTE_QUESTION", "TEXTE_REPONSE", "Texte_Question", "Texte_Reponse"])
    elif mode == "LEGI":
        return explore_nodes(child, whitelist=["BLOC_TEXTUEL"])
    elif mode == "DEBATS":
        return explore_nodes(child, whitelist=["Para"], mode=mode)
    return explore_nodes(child)

def process_xml_file(file_path, json_path, mode=None):
    parsed_doc = {}
    try:
        tree = ET.parse(file_path)
        root_xml = tree.getroot()
    except:
        logging.warning(f"Could not parse {file_path}")
        return

    parsed_doc["path"] = file_path if mode == None else f"{mode}/{os.path.basename(file_path)}"
    parsed_doc["body"] = clean_text(xml_parser(root_xml, mode=mode))
    
    if parsed_doc["body"].replace("\n", "").strip() == "":
        return

    logging.info(f"Writing {parsed_doc['path']}")
    with open(json_path, "a+") as f:
        f.write(json.dumps(parsed_doc) + "\n")

# ------------------------------------

def docx_parser(doc):
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def process_docx_file(file_path, json_path, mode=None):
    parsed_doc = {}
    try:
        doc = docx.Document(file_path)
    except:
        logging.warning(f"Could not parse {file_path}")
        return
    
    parsed_doc["path"] = file_path if mode == None else f"{mode}/{os.path.basename(file_path)}"
    parsed_doc["body"] = clean_text(docx_parser(doc), mode=mode)

    if parsed_doc["body"].replace("\n", "").strip() == "":
        return

    logging.info(f"Writing {parsed_doc['path']}")
    with open(json_path, "a+") as f:
        f.write(json.dumps(parsed_doc) + "\n")

# ------------------------------------

def process_txt_file(file_path, json_path, mode=None):
    parsed_doc = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
    except:
        logging.warning(f"Could not parse {file_path}")
        return
    
    parsed_doc["path"] = file_path if mode == None else f"{mode}/{os.path.basename(file_path)}"
    parsed_doc["body"] = clean_text(text, mode=mode)

    if parsed_doc["body"].replace("\n", "").strip() == "":
        return

    logging.info(f"Writing {parsed_doc['path']}")
    with open(json_path, "a+") as f:
        f.write(json.dumps(parsed_doc) + "\n")

# ------------------------------------

def explore_files(path, json_path: str, mode=None):
    for root, _, files in tqdm(os.walk(path), desc=f"Exploring {path}"):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Extract archives
            if file.endswith((".taz", ".tar.gz", ".tar", ".zip")):
                logging.info(f"Extracting {file_path}")
                folder_path = file_path.replace(".tar.gz", "").replace(".taz", "").replace(".tar", "").replace(".zip", "")
                
                if file.endswith((".taz", ".tar")):
                    os.makedirs(folder_path, exist_ok=True)
                    os.system(f"tar -zxvf {file_path} -C {folder_path}")
                elif file.endswith(".tar.gz"):
                    os.makedirs(folder_path, exist_ok=True)
                    tar = tarfile.open(file_path, "r:gz")
                    tar.extractall(path=folder_path)
                    tar.close()
                elif file.endswith(".zip"):
                    os.makedirs(folder_path, exist_ok=True)
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(folder_path)
                    
                # Depth exploration then delete
                explore_files(folder_path, json_path, mode=mode)
                shutil.rmtree(folder_path)

            # Read files
            # If XML
            if file.endswith(".xml") and mode not in ["ACCO"]:
                if mode not in ["DEBATS"]:
                    process_xml_file(file_path, json_path, mode=mode)
                elif mode == "DEBATS" and file.startswith(("CRI", "SEN")): process_xml_file(file_path, json_path, mode=mode)
            # If docx
            elif mode == "ACCO" and file.endswith(".docx"):
                process_docx_file(file_path, json_path, mode=mode)
                # If txt
            elif mode == "BALO" and file.endswith(".txt"):
                process_txt_file(file_path, json_path, mode=mode)

# ------------------------------------

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
    explore_files(args.base_path, save_path, mode=args.prefix.upper())

    if args.hub_id:
        dataset = load_dataset("json", data_files=save_path)
        dataset = dataset.rename_column("path", "id")
        dataset = dataset.rename_column("body", "text")
        try:
            dataset.push_to_hub(args.hub_id)
        except Exception as e:
            print("Failed to push to hub: ", e)
            dataset.save_to_disk(os.path.join(args.save_dir, f"{args.prefix}_opendata"))
