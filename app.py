# app.py
import argparse
import streamlit as st
from PIL import Image
import database
import voting
import os

# Parse command-line arguments to create an password so we can reset votes 
def get_args():
    parser = argparse.ArgumentParser(description="Image Classification Voting System")
    parser.add_argument('--admin_password', type=str, required=True, 
                        help="Admin password to reset votes.")
    return parser.parse_args()

# Get password from command-line arguments
args = get_args()
ADMIN_PASSWORD = args.admin_password

# Initialize the database (create table if needed)
database.init_db()

# Display app title
st.title("Image Classification Voting System")

# Set up session state to track images user has already voted on
if 'voted_images' not in st.session_state:
    st.session_state.voted_images = []

# Get a random image that the user has not voted on
selected_image = voting.get_random_unvoted_image(st.session_state.voted_images)

if not selected_image:
    st.subheader("You have voted on all images. Thank you!")
else:

    st.markdown("---")

    # Set up two columns: one for the image and one for the voting interface
    col1, col2 = st.columns([2, 1])

    # Display the image in the left column
    with col1:
            # Display image title above the image
        st.subheader(f"Image: {selected_image}")
        image_path = os.path.join(voting.IMAGE_FOLDER, selected_image)
        image = Image.open(image_path)
        max_width, max_height = 1000, 750
        image.thumbnail((max_width, max_height))
        st.image(image, use_column_width=True)

    # Display the voting interface in the right column
    with col2:
        # Add some vertical space
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
        # Voting with two buttons: Good and Reject
        if st.button("Good 👍", key="good_vote"):
            database.insert_vote(selected_image, "Good")
            # lower the buttons 
            st.session_state.voted_images.append(selected_image)
            st.success(f"Thank you! You voted: Good for {selected_image}")
            st.rerun()
    
        if st.button("Reject 👎", key="reject_vote"):
            database.insert_vote(selected_image, "Reject")
            st.session_state.voted_images.append(selected_image)
            st.success(f"Thank you! You voted: Reject for {selected_image}")
            st.rerun()
# Add spacing and a divider
st.markdown("---")

# Display the voting summary table for all images
st.write("### Voting Results for All Images")
vote_summary = database.get_vote_summary()
st.dataframe(vote_summary)

# Create a download button in Streamlit for the CSV file
csv_file = voting.export_votes_to_csv()
with open(csv_file, "rb") as file:
    st.download_button(
        label="Download Voting Results as CSV",
        data=file,
        file_name="vote_results.csv",
        mime="text/csv"
    )

# Admin-only Reset Votes button with unique key
with st.expander("Admin Panel"):
    admin_input = st.text_input("Enter admin password to reset votes", type="password")
    if st.button("Reset Votes", key="admin_reset") and admin_input == ADMIN_PASSWORD:
        database.reset_votes()
        st.warning("All votes have been reset.")
        st.session_state.voted_images = []
        st.rerun()
    elif admin_input and admin_input != ADMIN_PASSWORD:
        st.error("Incorrect password! Please try again.")
