from fp.fp import FreeProxy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, wait
import pandas as pd
import requests
import argparse
import urllib3
import random
import time
import re
import os

# Suppressing InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to scrape lyrics for an album
def scrape_album(args, album, artist_name):
    album_name = album.find('a').text
    album_year = album.find('em').text

    song_table = album.find_next('table')
    song_rows = song_table.find_all('tr')

    proxy = FreeProxy(rand=True).get()

    for song_row in song_rows:
        song_number = song_row.find(class_='track-number').text.strip('.')
        song_title = song_row.find(class_='track-title').text
        song_link = urljoin(args.url, song_row.find(class_='track-title').find('a')['href'])

        # When scrapping is detected, change proxy and try again as long as the proxy is not working
        errors = 0
        while errors < 100:
            try:
                song_html = requests.get(song_link, proxies={"http": proxy, 'https': proxy}, timeout=5, verify=False).content
                song_soup = BeautifulSoup(song_html, 'html.parser')

                text_section = song_soup.find("div", class_="text")

                en_tags = text_section.find_all('strong')
                fr_tags = text_section.find_all('em')

                en_lyrics = '\n'.join([en.get_text() for en in en_tags])
                fr_lyrics = '\n'.join([fr.get_text() for fr in fr_tags])

                en_lyrics = re.sub(r'([a-z])([A-Z])', r'\1\n\2', en_lyrics)
                fr_lyrics = re.sub(r'([a-z])([A-Z])', r'\1\n\2', fr_lyrics)

                print(f"{artist_name} - {song_title}")
                lyrics_data.append([
                    artist_name,
                    album_name,
                    album_year,
                    song_title,
                    song_number,
                    en_lyrics,
                    fr_lyrics
                ])
                time.sleep(random.uniform(0.25, 1))
                break
            except:
                errors+=1
                proxy = FreeProxy(rand=True).get()

# Function to scrape albums for an artist
def scrape_artist(args, artist_info):
    artist_name, artist_url = artist_info

    # When scrapping is detected, change proxy and try again as long as the proxy is not working
    proxy = FreeProxy(rand=True).get()
    errors = 0
    while errors < 100:
        try:
            artist_html = requests.get(urljoin(args.url, artist_url), proxies={"http": proxy, 'https': proxy}, timeout=5, verify=False).content
            artist_soup = BeautifulSoup(artist_html, 'html.parser')
            # If there is no album(s), this means that scraping is detected.
            album_sections = artist_soup.find_all('h6')
            if not album_sections: raise
            break
        except:
            errors+=1
            proxy = FreeProxy(rand=True).get()

    # Scrapping songs from albums
    with ThreadPoolExecutor(max_workers=args.max_albums_workers) as album_executor:
        album_tasks = [album_executor.submit(scrape_album, args, album, artist_name) for album in album_sections]
        wait(album_tasks)

    artist_seen.append(artist_name)

def main():
    parser = argparse.ArgumentParser(description="Scrape lyrics data from a website.")
    parser.add_argument("--url", type=str, default="https://www.lacoccinelle.net/artistes/index.html", help="Starting URL for scraping")
    parser.add_argument("--max_albums_workers", type=int, default=20, help="Maximum number of album workers")
    parser.add_argument("--max_artist_workers", type=int, default=5, help="Maximum number of artist workers")
    args = parser.parse_args()

    global lyrics_data
    global url
    global artist_seen
    lyrics_data = []
    url = args.url
    artist_seen = []

    if os.path.exists("lyrics_dataframe.csv"):
        print("Loading logs...")
        df = pd.read_csv("lyrics_dataframe.csv")
        artist_seen = df['artist_name'].unique()
        lyrics_data = df.values.tolist()

    proxy = FreeProxy(rand=True).get()
    while url:
        # When scrapping is detected, change proxy and try again as long as the proxy is not working
        while True:
            try:
                html = requests.get(url, proxies={"http": proxy, 'https': proxy}, timeout=5, verify=False).content
                soup = BeautifulSoup(html, 'html.parser')

                artists = []
                artist_url_pattern = re.compile(r'^\/[0-9]+.*\.html')
                artist_links = soup.find_all('a', href=artist_url_pattern)

                # If there is no artist, this means that scraping is detected.
                if not artist_links: raise

                for a_tag in artist_links:
                    href = a_tag.get('href', '')
                    if 'title' in a_tag.attrs and a_tag['title'] not in artist_seen:
                        artists.append((a_tag['title'], href))
                break
            except:
                proxy = FreeProxy(rand=True).get()

        # Scrap artists' lyrics
        if artists != []:
            with ThreadPoolExecutor(max_workers=args.max_artist_workers) as artist_executor:
                artist_tasks = [artist_executor.submit(scrape_artist, args, artist) for artist in artists]
                wait(artist_tasks)

        # When all artists of the page are scrapped, saved them.
        lyrics_dataframe = pd.DataFrame(lyrics_data, columns=['artist_name', 'album_name', 'year', 'title', 'number', 'en', 'fr'])
        lyrics_dataframe = lyrics_dataframe.drop_duplicates()
        lyrics_dataframe.to_csv("lyrics_dataframe.csv", index=False)

        # Go to the next page
        next_page = soup.find("a", text=">")
        url = urljoin(url, next_page["href"]) if next_page else ""

if __name__ == "__main__":
    main()
