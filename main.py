import os
import tweepy

from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(os.getenv("BEARER_TOKEN"))