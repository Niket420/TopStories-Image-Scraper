import csv
import requests
import os

# Input CSV file
input_csv = '/Users/niketanand/Documents/MLOps/task1/image_data.csv'  # Replace with your CSV file path
output_csv = 'output.csv'  # Output CSV file with new image names

# Create a folder to store the downloaded images
os.makedirs('images', exist_ok=True)

# Read the input CSV file
with open(input_csv, newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

# Skip the header row (if there is one)
rows = rows[1:]  # This removes the first row (header)

# List to store new data (image name and caption)
new_rows = []

# Loop through each row to download the image and rename it sequentially
for idx, row in enumerate(rows, start=1):
    image_url = row[0].strip()  # Image URL is in the first column
    caption = row[1]           # Caption is in the second column

    # Check if the URL starts with 'http' or 'https'
    if not image_url.startswith(('http://', 'https://')):
        print(f"Invalid URL format for image {idx}: {image_url}")
        continue

    # Download the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        # Save the image with a sequential name (e.g., image1.jpg, image2.jpg)
        image_name = f"image{idx}.jpg"
        image_path = os.path.join('images', image_name)

        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)

        # Add the new image name and caption to the new rows list
        new_rows.append([image_name, caption])

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {idx}: {e}")

# Write the new CSV file with updated image names and captions
with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Image Name', 'Caption'])  # Write the header row
    writer.writerows(new_rows)

print(f"Downloaded images and created {output_csv} successfully.")