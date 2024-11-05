# database.py
import os
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to initialize the database and create table (if it doesn't exist)
def init_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            image_filename TEXT,
            vote TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a vote into the database
def insert_vote(image_filename, vote):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (image_filename, vote)
        VALUES (%s, %s)
    ''', (image_filename, vote))
    conn.commit()
    conn.close()

# Function to get vote counts for a specific image
def get_vote_counts(image_filename):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT vote, COUNT(*) FROM feedback
        WHERE image_filename = %s
        GROUP BY vote
    ''', (image_filename,))
    votes = cursor.fetchall()
    vote_counts = {'Good': 0, 'Reject': 0}
    for row in votes:
        vote_counts[row['vote']] = row['count']
    conn.close()
    return vote_counts['Good'], vote_counts['Reject']

# Function to get a summary of votes for all images
def get_vote_summary():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT image_filename, 
               SUM(CASE WHEN vote = 'Good' THEN 1 ELSE 0 END) AS good_votes,
               SUM(CASE WHEN vote = 'Reject' THEN 1 ELSE 0 END) AS reject_votes
        FROM feedback
        GROUP BY image_filename
    ''')
    rows = cursor.fetchall()
    vote_summary = pd.DataFrame(rows, columns=['Image', 'Good Votes', 'Reject Votes'])
    conn.close()
    return vote_summary

# Function to reset (clear) all votes in the database
def reset_votes():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback")
    conn.commit()
    conn.close()
