import requests
from bs4 import BeautifulSoup
import argparse

# Function to fetch the home page and parse it
def fetch_homepage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for bad HTTP responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the homepage: {e}")
        return None

# Function to scrape the "Top Stories" link dynamically
def scrape_top_stories(homepage_html, selector):
    soup = BeautifulSoup(homepage_html, 'html.parser')
    
    # Find the link using the selector
    top_stories_link = soup.select_one(selector)
    
    if top_stories_link:
        return top_stories_link['href']
    else:
        print("Top Stories link not found.")
        return None

# Main function to run the script
def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Scrape the 'Top Stories' link from the homepage")
    parser.add_argument('--url', required=True, help="The URL of the homepage to scrape.")
    parser.add_argument('--selector', required=True, help="The CSS selector to find the 'Top Stories' link.")
    
    args = parser.parse_args()

    # Fetch homepage HTML
    homepage_html = fetch_homepage(args.url)
    if homepage_html:
        # Scrape the 'Top Stories' link
        top_stories_url = scrape_top_stories(homepage_html, args.selector)
        
        if top_stories_url:
            print(f"Top Stories URL: {top_stories_url}")
        else:
            print("Failed to find Top Stories link.")
    else:
        print("Failed to fetch homepage content.")

if __name__ == "__main__":
    main()