# app.py
import streamlit as st
from PIL import Image
import database
import voting
import os

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
    # Display image title above the image
    st.subheader(f"Image: {selected_image}")
    st.markdown("---")

    # Set up two columns: one for the image and one for the voting interface
    col1, col2 = st.columns([2, 1])

    # Display the image in the left column
    with col1:
        image_path = os.path.join(voting.IMAGE_FOLDER, selected_image)
        image = Image.open(image_path)
        max_width, max_height = 400, 400
        image.thumbnail((max_width, max_height))
        st.image(image, use_column_width=True)

    # Display the voting interface in the right column
    with col2:
        # Display current vote counts for the selected image
        good_votes, reject_votes = database.get_vote_counts(selected_image)
        st.markdown("**Current Votes:**")
        st.write(f"👍 Good: {good_votes}")
        st.write(f"👎 Reject: {reject_votes}")
        st.markdown("---")

        # Voting with two buttons: Good and Reject
        if st.button("Good 👍", key="good_vote"):
            database.insert_vote(selected_image, "Good")
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

# Admin-only Reset Votes button
with st.expander("Admin Panel"):
    admin_input = st.text_input("Enter admin password to reset votes", type="password")
    if admin_input == "your_admin_password":  # replace with a secure password
        if st.button("Reset Votes"):
            database.reset_votes()
            st.warning("All votes have been reset.")
            st.session_state.voted_images = []
            st.rerun()
    elif admin_input and admin_input != "your_admin_password":
        st.error("Incorrect password.")
