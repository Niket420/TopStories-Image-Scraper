# TopStories-Image-Scraper

# Web Scraping Project for Headlines and Images

This project scrapes the "Top Stories" section from a given website, retrieves the image URLs and their captions (headlines), and stores them in a MongoDB Atlas database. It also provides a way to retrieve and save the data from the database.

## Project Structure

- **scrapping.py**: The main script that performs the web scraping and saves the scraped data to MongoDB.
- **fetching_top_stories.py**: A custom function specifically designed to scrape the "Top Stories" section. This is called within `scrapping.py`.
- **retrieving_data_MongoDB.py**: This script retrieves saved headlines and image URLs from MongoDB and stores them in a CSV file for further analysis.
- **requirements.txt**: A file that lists all required Python packages for the project.

## Steps to Run the Project

### 1. Clone the repository and install dependencies
First, clone the repository to your local machine and navigate to the project folder. Then install the required dependencies.

```bash
git clone <repository_url>
cd <project_folder>
pip install -r requirements.txt

### 2. Running the Scraping Script

Once you have installed the dependencies, you can run the main scraping script to fetch the "Top Stories" from a website and store the data in MongoDB.

#### Command to run:
```bash
python scrapping.py --home_url "website_url" --mongoDB_atlas_string "mongoDB_connection_string"


## for retrieving the scrapping data use:
```bash
python retrieving_data_MongoDB.py --mongoDB_atlas_string "mongoDB_connection_string"


