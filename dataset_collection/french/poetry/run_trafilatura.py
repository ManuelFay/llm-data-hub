from tqdm import tqdm
import datasets
import re
from trafilatura import fetch_url, extract

LINKS_PATH = "./data/links.txt"

with open(LINKS_PATH) as f:
    links = f.readlines()

print(f"Found {len(links)} links")
# regex filter to keep only links to poems
links = [link for link in links if "/poeme-" in link]
print(f"Kept {len(links)} links")

# remove duplicates
links = list(set(links))
print(f"Removed duplicates, {len(links)} links remaining")

# Process all links with trafilatura


poems = []

for link in tqdm(links):
    link = link.strip()
    downloaded = extract(fetch_url(link))
    if downloaded is None:
        continue
    # extract regex pattern r"Titre : (.*)\nPoète : (.*)\n"
    titre = re.findall(r"Titre : (.*)\nPoète : (.*)\n", downloaded)[0][0]
    poete = re.findall(r"Titre : (.*)\nPoète : (.*)\n", downloaded)[0][1]
    poems.append({"title": titre, "poet": poete, "text": downloaded, "link": link, "id": "-".join(link.split("/")[-2:])[:-4]})

print(f"Extracted {len(poems)} poems")

ds = datasets.Dataset.from_list(poems)
print(ds)
ds.push_to_hub("manu/french_poetry")
