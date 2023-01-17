import os
import tweepy
import time

import urllib.request

from dotenv import load_dotenv


def get_client():
    client = tweepy.Client(os.getenv("BEARER_TOKEN"))
    return client


def get_urls(client):
    media = client.get_liked_tweets(
        id=1610756529346469889,
        max_results=100,
        expansions="attachments.media_keys",
        media_fields="url",
    ).includes["media"]
    print(media)
    ids = []
    for tweet in media:
        print(tweet.url)
        ids.append(tweet.url)
    return ids
        
def download_image(urls):
    os.makedirs("images", exist_ok=True)
    for url in urls:
        filename = url.split("/")[-1]
        filepath = os.path.join("images", filename)
        if os.path.exists(filepath):
            print(f"Skipping {filename} because it already exists")
            continue
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded {filename}!")
        time.sleep(1)


def start():
    load_dotenv()
    client = get_client()
    urls = get_urls(client)
    download_image(urls)


start()
