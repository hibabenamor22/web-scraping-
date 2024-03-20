import argparse
import subprocess
import sys
import shutil
import os
import importlib
subprocess.run(["git", "clone", "https://github.com/shaikhsajid1111/facebook_page_scraper.git"])
subprocess.run(["pip3", "install", "facebook-page-scraper"])
subprocess.run(["git", "clone", "https://github.com/shaikhsajid1111/twitter-scraper-selenium"])
subprocess.run(["pip3", "install", "twitter-scraper-selenium"])
subprocess.run(["git", "clone", "https://github.com/hibabenamor22/instagram-.git"])

def move_files():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    instagram_path = os.path.join(script_dir, "instagram.py")
    twitter_scrape_path = os.path.join(script_dir, "twitter_scraper_selenium")
    
    # Check if files or folders already exist
    if not os.path.exists(instagram_path):
        shutil.move("instagram-/instagram.py", instagram_path)
    if not os.path.exists(twitter_scrape_path):
        shutil.move("twitter-scraper-selenium/twitter_scraper_selenium", twitter_scrape_path)
        
move_files()

    
from facebook_page_scraper import Facebook_scraper
from twitter_scraper_selenium import get_profile_details, scrape_profile
from subprocess import check_output
from instagram import Instagram

def main():
    parser = argparse.ArgumentParser(description="Social Media Scraper")
    parser.add_argument("name", type=str, help="Name of the person or page to scrape on Facebook, Twitter, and Instagram")
    parser.add_argument("--count", type=int, default=10, help="Number of posts to scrape (default: 10)")
    args = parser.parse_args()

    scrape_social_media(args.name, args.count)



def scrape_social_media(name, count): 
    try:
        scrape_twitter(name, count)
    except Exception as e:
        print(f"An error occurred while scraping Twitter data for '{name}': {str(e)}")

    try:
        scrape_instagram(name)
    except Exception as e:
        print(f"An error occurred while scraping Instagram data for '{name}': {str(e)}")
    try:
        scrape_facebook(name, count)
    except Exception as e:
        print(f"An error occurred while scraping Facebook data for '{name}': {str(e)}")
        
def scrape_twitter(name, count):
    try:
        scrape_profile(twitter_username=name, output_format="csv", browser="firefox", tweets_count=count, filename=name, directory="/home/kali/Downloads")
        get_profile_details(twitter_username=name, filename=name)
        print(f"Twitter data scraped successfully for '{name}'")
    except Exception as e:
        print(f"An error occurred while scraping Twitter data for '{name}': {str(e)}")

def scrape_instagram(name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    instagram_script_path = os.path.join(script_dir, "instagram.py")
    
    try:
        output = check_output(["python3", instagram_script_path, name]).decode()
        print(output)
        print(f"Instagram data scraped successfully for '{name}'")
    except Exception as e:
        print(f"An error occurred while scraping Instagram data for '{name}': {str(e)}")

def scrape_facebook(name, count):
    try:
        browser = "firefox"  # or "chrome" if you prefer
        timeout = 600
        headless = False
        scraper = Facebook_scraper(name, count, browser, timeout=timeout, headless=headless)
        directory = "/content"  # Or any other directory within your Colab environment
        filename = f"{name}_facebook_data"
        scraper.scrap_to_csv(filename, directory)
        print(f"Facebook data scraped successfully for '{name}' and saved to '{directory}/{filename}.csv'")
    except Exception as e:
        print(f"An error occurred while scraping Facebook data for '{name}': {str(e)}")      



if __name__ == "__main__":
    main()
