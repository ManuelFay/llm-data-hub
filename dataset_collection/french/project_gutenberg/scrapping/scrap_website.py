import requests
import re
# Optional dependency
# pip install beautifulsoup4
try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("Please install beautifulsoup4 to run this script")


START_URL = "https://www.gutenberg.org/robot/harvest?offset=0&filetypes[]=txt&langs[]=fr"


def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and href.endswith("-8.zip"):
            links.append(href)

    print(f"Found {len(links)} links on {url}")
    if "harvest?offset" in str(link) and len(links) > 0:
        print("Found next page")
        # convert bs4 tag to string
        res = re.findall(r'harvest\?offset=(\d+)&amp;filetypes\[\]=txt&amp;langs\[\]=fr', str(link))[0]
        links = links + get_links_from_page("https://www.gutenberg.org/robot/harvest?offset=" + res + "&filetypes[]=txt&langs[]=fr")

    return links


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Scrap the Project Gutenberg website to get all the links to the French books')
    parser.add_argument('--save_path', type=str, help='Directory where the extracted urls will be saved')
    args = parser.parse_args()
    all_links = get_links_from_page(START_URL)
    print(f"Found {len(all_links)} links in total")
    with open(args.save_path, "w") as f:
        for link in all_links:
            f.write(link + "\n")
    print("Links saved to " + args.save_path)

    # Download all files with wget
    # wget -i links.txt