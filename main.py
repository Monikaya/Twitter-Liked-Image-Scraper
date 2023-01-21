import math
import os
import tweepy
import asyncio
import shutil

import urllib.request

from dotenv import load_dotenv


async def get_client():
    client = tweepy.Client(os.getenv("BEARER_TOKEN"), wait_on_rate_limit=True)
    return client


async def get_pages(client, page_limit, tweets_per_page, user_id):
    pages = []

    for response in tweepy.Paginator(
        client.get_liked_tweets,
        id=user_id,
        max_results=tweets_per_page if tweets_per_page != None else page_limit,
        expansions="attachments.media_keys",
        media_fields="url",
        limit=page_limit if page_limit > 0 else float("inf"),
    ):
        print(response)
        try:
            pages.append(response.includes["media"])
        except KeyError:
            continue
    return pages


async def format_pages(page):
    urls = []
    for tweet in page:
        urls.append(tweet.url)
    return urls


async def download_images(page):
    urls = await format_pages(page)

    os.makedirs("images", exist_ok=True)
    for url in urls:
        try:
            filename = url.split("/")[-1]
            filepath = os.path.join("images", filename)
            if os.path.exists(filepath):
                print(f"Skipping {filename} because it already exists")
                continue
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, filepath)
            print(f"Downloaded {filename}!")
        except Exception:
            print(f"Failed to download a file! Skipping...")
            continue

        await asyncio.sleep(1)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def setup_env():
    if not os.path.exists(".env"):
        print("Seems you don't have a .env file!")
        print("Let's create one!!")
        bearer = input(
            "Please input your bearer token: (If you don't know what this is, check the README!) "
        )
        user_id = input("Please input your desired twitter user id: ")
        with open(".env", "w") as f:
            f.write(f'BEARER_TOKEN="{bearer}"\n')
            f.write(f'USER_ID="{user_id}"')
        print("Done! Now let's get to downloading some images!")


async def start():
    clear()
    setup_env()
    load_dotenv()
    print("Welcome to my Twitter Liked Image Downloader!")
    print("If you would like to iterate over all of your liked tweets input '-1'")
    num_tweets = input("How many tweets would you like to download? ")
    if int(num_tweets) < 10000 and int(num_tweets) > 25 or int(num_tweets) == -1:
        if not int(num_tweets) == -1:
            num_pages = math.sqrt(int(num_tweets))
            tweets_per_page = None
        else:
            num_pages = -1
            tweets_per_page = 50
    else:
        print("Your number appears to be either above 10000 or below 25")
        print("Unfortunately we can't process those numbers at the moment")
        print(
            "Instead though, you can define the number of pages, and tweets per page you want"
        )
        print("# of pages * # of tweets per page = # of tweets")
        satisfied = False
        while not satisfied:
            num_pages = input("How many pages would you like to iterate over? ")
            tweets_per_page = input("How many tweets per page would you like to iterate over? ")
            print(num_pages)
            print(tweets_per_page)
            print(int(num_pages) * int(tweets_per_page))
            print(f"Your number of tweets is {int(num_pages) * int(tweets_per_page)}")
            if input("Is this correct? (y/n) ") == "y":
                satisfied = True
                print("Great! Let's get to downloading some images!")

    client = await get_client()
    pages = await get_pages(client, int(num_pages), tweets_per_page if tweets_per_page != None else None, os.getenv("USER_ID"))

    print("Downloading images... This may take a while...")
    await asyncio.sleep(2)
    tasks = [asyncio.create_task(download_images(page)) for page in pages]
    for task in tasks:
        await task

    await asyncio.sleep(1)
    clear()
    print("Done! All images have been downloaded to the images folder!")
    if (
        input(
            "Last thing, would you like to pack all of the images into a zip file? (y/n) "
        )
        == "y"
    ):
        shutil.make_archive("images", "zip", "images")
        print("Done! The zip file is in the same directory as the script!")
        await asyncio.sleep(1)
    print("Thanks for using my Twitter Liked Image Downloader! :D")
    input("Press enter to exit...")
    exit()


asyncio.run(start())
