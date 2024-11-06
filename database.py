# database.py
import sqlite3
import pandas as pd

# SQLite database file
DB_FILE = 'votes.db'

# Function to create the SQLite database and table (if it doesn't exist)
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_filename TEXT,
            vote TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a vote into the database
def insert_vote(image_filename, vote):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Insert the feedback into the table
    cursor.execute('''
        INSERT INTO feedback (image_filename, vote)
        VALUES (?, ?)
    ''', (image_filename, vote))
    
    conn.commit()
    conn.close()

# Function to get vote counts for a specific image
def get_vote_counts(image_filename):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Query for counting votes
    cursor.execute('''
        SELECT vote, COUNT(*) FROM feedback
        WHERE image_filename = ?
        GROUP BY vote
    ''', (image_filename,))
    
    # Fetch the results and organize them into a dictionary
    votes = cursor.fetchall()
    vote_counts = {'Good': 0, 'Reject': 0}
    
    for vote, count in votes:
        vote_counts[vote] = count
    
    conn.close()
    return vote_counts['Good'], vote_counts['Reject']

# Function to get a summary of votes for all images
def get_vote_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Query to get total counts for each image
    cursor.execute('''
        SELECT image_filename, 
               SUM(CASE WHEN vote = "Good" THEN 1 ELSE 0 END) AS good_votes,
               SUM(CASE WHEN vote = "Reject" THEN 1 ELSE 0 END) AS reject_votes
        FROM feedback
        GROUP BY image_filename
    ''')
    
    # Fetch all results into a DataFrame
    rows = cursor.fetchall()
    vote_summary = pd.DataFrame(rows, columns=['Image', 'Good Votes', 'Reject Votes'])
    
    conn.close()
    return vote_summary

# Function to reset (clear) all votes in the database
def reset_votes():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Delete all rows in the feedback table
    cursor.execute("DELETE FROM feedback")
    conn.commit()
    conn.close()