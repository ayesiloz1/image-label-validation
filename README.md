# Image Classification Voting System

This repository contains a Streamlit-based voting application designed to help validate or correct image labels in our dataset. Users can vote on each image as either "Good" or "Reject." The app also includes an admin panel with password-protected access to reset the voting data.

## Features

- **Voting System**: Users can classify images as either "Good" or "Reject."
- **Summary Table**: Displays real-time voting statistics for each image.
- **CSV Export**: Users can download a CSV file containing all voting results.
- **Admin Panel**: Allows an administrator to reset the voting database with password protection.

## Setup and Installation

### Prerequisites

- Python 3.7+
- Conda (for environment management)

### Cloning the Repository

```sh
git clone https://github.com/ayesiloz1/image-label-validation.git
cd image-label-validation

Option 1: Using environment.yml with Conda

If you are using Conda, you can create the environment using the provided environment.yml file.
conda env create -f environment.yml
conda activate image-voting-env


Option 2: Using requirements.txt with Pip
Alternatively, you can set up the environment using requirements.txt if you are not using Conda.

pip install -r requirements.txt

streamlit run app.py -- --admin_password your_password
# image-label-validation
