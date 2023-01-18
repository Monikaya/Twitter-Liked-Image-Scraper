import os
import tweepy
import asyncio
import shutil

import urllib.request

from dotenv import load_dotenv


async def get_client():
    client = tweepy.Client(os.getenv("BEARER_TOKEN"), wait_on_rate_limit=True)
    return client

async def get_pages(client, page_limit, user_id):
    pages = []

    for response in tweepy.Paginator(client.get_liked_tweets, id=user_id, 
        max_results=10,
        expansions="attachments.media_keys",
        media_fields="url",
        limit = page_limit if page_limit > 0 else float("inf")):
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
            print(f"Failed to download a file!")
            continue
        
        await asyncio.sleep(1)

def clear():
    os.system("cls" if os.name=='nt' else 'clear')

def setup_env():
    if not os.path.exists(".env"):
        print("Seems you don't have a .env file!")
        print("Let's create one!!")
        bearer = input("Please input your bearer token: (If you don't know what this is, check the README!) ")
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
    print("One page is equivalent to 10 tweets")
    num_pages = input("How many pages of tweets do you want to download? ")
    client = await get_client()
    pages = await get_pages(client, int(num_pages), os.getenv("USER_ID"))

    print("Downloading images... This may take a while...")
    await asyncio.sleep(2)
    tasks = [asyncio.create_task(download_images(page)) for page in pages]
    for task in tasks:
        await task
    
    await asyncio.sleep(1)
    clear()
    print("Done! All images have been downloaded to the images folder!")
    if input("Last thing, would you like to pack all of the images into a zip file? (y/n) ") == "y":
        shutil.make_archive("images", "zip", "images")
        print("Done! The zip file is in the same directory as the script!")
        await asyncio.sleep(1)
    print("Thanks for using my Twitter Liked Image Downloader! :D")
    input("Press enter to exit...")
    exit()


asyncio.run(start())
