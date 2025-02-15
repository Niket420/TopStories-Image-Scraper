import pymongo
import csv

# MongoDB connection string
MONGO_URI = "mongodb+srv://niketanand420:NA22B056@cluster0.bmbdc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB connection string

# Create a MongoDB client and connect to the database
client = pymongo.MongoClient(MONGO_URI)
db = client["google_news"]  # Replace with your database name

# Define the collections
headlines_collection = db["headlines"]  # Ensure this is the correct collection
images_collection = db["images"]  # Ensure this is the correct collection

# Open a CSV file to write the data
with open("image_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow(["Image URL", "Caption"])

    # Retrieve the data from both collections
    headlines = {headlin['_id']: headlin['headline'] for headlin in images_collection.find()}
    
    # Debug: Print out the headlines to verify
    print("Fetched Headlines:", headlines)

    images = list(images_collection.find())
    
    # Debug: Print out the images to verify
    print("Fetched Images:", images)

    data_found = False  # Flag to check if we are getting any data

    # Check if images collection is empty
    if not images:
        print("No images found in the images collection.")
    else:
        # Iterate through images collection
        for image_data in images:
            print("Inside for loop - processing image_data")

            # Get the image URL and image _id
            image_url = image_data.get("thumbnail_url")  # Assuming the URL field is "thumbnail_url"
            image_id = image_data.get("_id")  # Getting the image's _id

            # Debug: Print the image URL and _id
            print("Image URL:", image_url)
            print("Image ID:", image_id)

            # Find the corresponding caption from headlines using image _id
            caption = headlines.get(image_id)  # Using image _id to find the corresponding headline caption

            # Check if both image_url and caption are valid
            if image_url and caption:
                data_found = True
                # Write to the CSV file
                writer.writerow([image_url, caption])
            else:
                print(f"Missing image_url or caption for image with _id {image_id}")

    # Check if no data was found and printed
    if not data_found:
        print("No valid data found to write in CSV.")

print("CSV writing completed.")