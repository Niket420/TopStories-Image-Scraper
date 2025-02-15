from pymongo import MongoClient
from datetime import datetime
import argparse
import sys

class MongoDBAtlasStorage:
    def __init__(self, connection_string, dbname="news_db"):
        """
        Initialize the MongoDB Atlas connection and database.
        :param connection_string: MongoDB Atlas connection string
        :param dbname: Name of the database (default: "news_db")
        """
        # Connect to MongoDB Atlas
        self.client = MongoClient(connection_string)
        # Select the database
        self.db = self.client[dbname]
        # Create/select the collections for headlines and images
        self.headlines = self.db["headlines"]
        self.images = self.db["images"]

    def insert_data(self, headline, image_url, article_url=None, article_date=None):
        """
        Insert extracted data into MongoDB Atlas.
        :param headline: Caption or headline of the story
        :param image_url: URL of the thumbnail image
        :param article_url: URL of the article (optional)
        :param article_date: Date of the article (optional)
        """
        # Prepare the headline data
        headline_data = {
            "headline": headline,  # Caption or headline
            "article_url": article_url,  # URL of the article
            "scrape_timestamp": datetime.now(),  # Timestamp of when the data was scraped
            "article_date": article_date  # Date of the article (if available)
        }
        # Insert the headline data into the "headlines" collection
        headline_id = self.headlines.insert_one(headline_data).inserted_id

        # Prepare the image data
        image_data = {
            "image_url": image_url,  # URL of the thumbnail image
            "headline_id": headline_id  # Reference to the corresponding headline
        }
        # Insert the image data into the "images" collection
        self.images.insert_one(image_data)

    def close(self):
        """
        Close the MongoDB Atlas connection.
        """
        self.client.close()


