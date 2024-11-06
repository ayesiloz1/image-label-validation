# voting.py
import os
import random
import pandas as pd
import database

# Path to your images directory
IMAGE_FOLDER = 'potentially_mislabeled'

# List of image filenames in the image folder
image_files = os.listdir(IMAGE_FOLDER)

# Function to get a random unvoted image
def get_random_unvoted_image(voted_images):
    available_images = [img for img in image_files if img not in voted_images]
    if available_images:
        return random.choice(available_images)
    else:
        return None

# Function to export the voting data to a CSV file for external analysis
def export_votes_to_csv():
    vote_data = database.get_vote_summary()
    csv_file = "vote_results.csv"
    vote_data.to_csv(csv_file, index=False)
    return csv_file