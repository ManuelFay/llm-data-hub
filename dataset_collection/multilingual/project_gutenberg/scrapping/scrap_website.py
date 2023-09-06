import requests
import re
import os
# Optional dependency
# pip install beautifulsoup4
try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("Please install beautifulsoup4 to run this script")


START_URL = """https://www.gutenberg.org/robot/harvest?offset=0&filetypes[]=txt&langs[]={lang}"""


def get_links_from_page(url, lang="fr", max_tries=5):
    print("Getting links from " + url)
    for try_idx in range(max_tries):
        try:
            response = requests.get(url)
            break
        except requests.exceptions.ConnectionError:
            if try_idx < max_tries - 1:
                print(f"Connection error, retrying for the {try_idx + 1} time")
            else:
                raise ConnectionError("Could not connect to the website")

    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and href.endswith("-8.zip"):
            links.append(href)

    print(f"Found {len(links)} links on {url}")
    if len(links) > 0 and "harvest?offset" in str(link):
        print("Found next page")
        # convert bs4 tag to string
        res = re.findall(r'harvest\?offset=(\d+)&amp;filetypes\[\]=txt&amp;langs\[\]=', str(link))[0]
        links = links + get_links_from_page("https://www.gutenberg.org/robot/harvest?offset=" + res + "&filetypes[]=txt&langs[]="+lang, lang=lang)

    return links


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Scrap the Project Gutenberg website to get all the links to the target language books')
    parser.add_argument('--save_dir', type=str, help='Directory where the extracted urls will be saved')
    parser.add_argument('--lang', type=str, default="all", help='Target language')
    args = parser.parse_args()

    if args.lang == "all":
        langs = ["es", "it", "de", "fr", "pt", "nl", "ko", "zh", "ru", "pl", "sv"]
        for lang in langs:
            print("Getting links for " + lang)
            all_links = get_links_from_page(START_URL.format(lang=lang), lang=lang)
            print(f"Found {len(all_links)} links in total")
            with open(os.path.join(args.save_dir, "links_" + lang + ".txt"), "w") as f:
                for link in all_links:
                    f.write(link + "\n")
            print("Links saved to " + args.save_dir)
    else:
        save_path = os.path.join(args.save_dir, "links_" + args.lang + ".txt")
        all_links = get_links_from_page(START_URL.format(lang=args.lang), lang=args.lang)
        print(f"Found {len(all_links)} links in total")
        with open(save_path, "w") as f:
            for link in all_links:
                f.write(link + "\n")
        print("Links saved to " + save_path)

    # Download all files with wget
    # wget -i links.txt