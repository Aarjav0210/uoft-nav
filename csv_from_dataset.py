### CAN DELETE FROM REPO ###

import os
import csv

# Folder containing the images
folder_path = os.path.join(os.getcwd(), 'images')

# List all files in the folder
files = os.listdir(folder_path)

# Filter for image files (e.g., .jpg, .png, etc.)
image_files = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]

# Create a dictionary to store target strings and their corresponding unique integer values
target_dict = {}

# Create a list to store the image names and target integer values
data = []
# Extract image name and target from each filename
for image_file in image_files:
    image_name = image_file
    target = image_file[:7]  # Extract first 6 characters

    # Check if target string is already in the dictionary, if not, assign a new integer value
    if target not in target_dict:
        target_dict[target] = len(target_dict) + 1

    # Append image name and target integer value to the data list
    data.append([image_name, target_dict[target]])

# Write the data to a CSV file
csv_file_path = os.path.join(os.getcwd(), 'dataset.csv')
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image', 'target'])  # Write header row
    writer.writerows(data)  # Write data rows

print(f'Saved CSV file to: {csv_file_path}')