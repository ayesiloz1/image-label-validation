import pandas as pd
import os
import shutil

# Read the CSV file
df = pd.read_csv('vote_results.csv')

# Create directories for good and reject if they do not exist
os.makedirs('good', exist_ok=True)
os.makedirs('reject', exist_ok=True)

# Iterate over the DataFrame and move images to respective directories
for index, row in df.iterrows():
    image_name = row['Image']
    source_path = os.path.join('potentially_mislabeled', image_name)
    if row['Good Votes'] == 0:
        destination_path = os.path.join('reject', image_name)
    else:
        destination_path = os.path.join('good', image_name)
    shutil.move(source_path, destination_path)