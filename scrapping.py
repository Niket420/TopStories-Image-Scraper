import time
import pymongo
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from mongo_atlas_storage import MongoDBAtlasStorage
import argparse




# Set up the WebDriver options for Selenium
options = Options()
options.headless = True  
service = Service(ChromeDriverManager().install())  # Use Service() properly
driver = webdriver.Chrome(service=service, options=options) 



#-------------- Directly fetch the URL for Top Stories, else use the function in fetching_top_stories.py file -------------------#
def fetch_top_stories_page(home_url):
    # Direct link to Google News "Top Stories"
    return home_url

# ---------------------------Scrape top stories from the "Top Stories" page------------------------------
def scrape_top_stories_page(url):
    print("Opening URL:", url)  # Debugging step
    driver.get(url)
    
    # Wait for the articles to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'article'))
        )
    except Exception as e:
        print("Error waiting for articles to load:", e)
        return []

    page_source = driver.page_source
    print("Page source length:", len(page_source))  # Check if content is loaded

    soup = BeautifulSoup(page_source, 'html.parser')
    stories = []

    for article in soup.find_all('article'):
        headline = article.find('h3')
        thumbnail = article.find('img')

        if headline and thumbnail:
            headline_text = headline.get_text(strip=True)
            thumbnail_url = thumbnail.get('src')
            article_url = article.find('a')['href']
            stories.append((headline_text, thumbnail_url, article_url))

    print(f"Total stories found: {len(stories)}")  # Debugging step

    return stories

# Store data in MongoDB
def store_data(stories):
    timestamp = datetime.now()
    for headline_text, thumbnail_url, article_url in stories:
        # Check if the headline already exists (basic de-duplication check)
        if not story_collection.find_one({"headline": headline_text}):
            # Insert story details
            story_collection.insert_one({
                "headline": headline_text,
                "url": article_url,
                "timestamp": timestamp,
                "article_date": timestamp
            })
            print(f"Stored headline: {headline_text}")
            print(f"URL path: {article_url}------------------------")

            # Insert image data if thumbnail exists
            if thumbnail_url:
                image_collection.insert_one({
                    "headline": headline_text,
                    "thumbnail_url": thumbnail_url,
                    "timestamp": timestamp
                })
                print(f"Stored thumbnail for: {headline_text}")
        else:
            print(f"Duplicate found: {headline_text}, skipping insert.")


    
    
    

# Run the scraper
if __name__ == "__main__":
    connection_string = "mongodb+srv://niketanand420:<password>@cluster0.bmbdc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    

    parser = argparse.ArgumentParser(description="enther the argument that is needed")
    parser.add_argument("--home_url",help = "enter the url u want to scrape",required=True)
    parser.add_argument("--mongoDB_atlas_string",help = "enter your mongoDB string to use it for your cloud",default=connection_string)
    args = parser.parse_args()


    # db = MongoDBAtlasStorage(connection_string)
    client = pymongo.MongoClient(connection_string)
    db = client['google_news']
    image_collection = db['images']
    story_collection = db['headlines']


    top_stories_url = fetch_top_stories_page(args.home_url)
    print(f"scraping just started baby boy")
    stories = scrape_top_stories_page(top_stories_url)
    store_data(stories)
    print("Scraping completed.")
    

    

