import os
import tweepy

from dotenv import load_dotenv


def get_client():
    client = tweepy.Client(os.getenv("BEARER_TOKEN"))
    return client


def get_media_keys(client):
    media = client.get_liked_tweets(
        id=1610756529346469889,
        expansions="attachments.media_keys",
        max_results=5,
        media_fields=["url", "height"],
    )[1]["media"]
    media_keys = []
    for tweet in media:
        media_keys.append(tweet["media_key"])
    return media_keys


def start():
    load_dotenv()
    client = get_client()
    media_keys = get_media_keys(client)
    print(media_keys)


start()
