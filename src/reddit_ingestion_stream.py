#!/usr/bin/env python
# coding: utf-8

# # Reddit API Ingestion Script

# In[1]:


# Required Library Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import os
import psycopg2
from psycopg2 import OperationalError, InterfaceError
from dotenv import load_dotenv
import praw
import threading
from datetime import datetime, timezone


# ## Connect to PostgreSQL and Create DB Tables

# In[2]:


load_dotenv()  # Loads variables from .env file in root

# Function to connect with retry
def connect_with_retry(retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            print("Connected to PostgreSQL!")
            return conn
        except (OperationalError, InterfaceError) as e:
            print(f"Connection failed: {e}")
            attempt += 1
            print(f"Retrying in {delay} seconds... ({attempt}/{retries})")
            time.sleep(delay)
    raise Exception("🚫 Could not connect to PostgreSQL after several retries.")

# Initial PostgreSQL Connection
conn = connect_with_retry()
cursor = conn.cursor()

# Function to create DB Tables
def create_tables(conn):
    cursor = conn.cursor()
    # Create reddit_posts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reddit_posts (
        id SERIAL PRIMARY KEY,
        post_id VARCHAR(30),
        title VARCHAR(300),
        selftext TEXT,
        author VARCHAR(30),
        score INT,
        num_comments INT,
        created_utc TIMESTAMP,
        subreddit VARCHAR(100),
        flair VARCHAR(100),
        url TEXT,
        over_18 BOOLEAN,
        is_self BOOLEAN,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create reddit_comments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reddit_comments (
        id SERIAL PRIMARY KEY,
        comment_id VARCHAR(30),
        body TEXT,
        author VARCHAR(30),
        score INT,
        created_utc TIMESTAMP,
        subreddit VARCHAR(100),
        is_submitter BOOLEAN,
        distinguished VARCHAR(30),
        parent_id VARCHAR(30),
        link_id VARCHAR(30),
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    cursor.close()

# PostgreSQL Auto-Reconnect script
try:
    create_tables(conn)
    print("Tables creation successful.")
except (OperationalError, InterfaceError):
    print("Connection lost. Reconnecting and retrying...")
    conn = connect_with_retry()
    create_tables(conn)


# ## Initialize Reddit Connection

# In[3]:


# Initialize PRAW for Reddit connection
def connect_to_reddit():
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("USER_AGENT")
        )

        # Confirm correct credentials
        print(f"Authenticated as: {reddit.user.me()}")

        # Test connection by accessing known subreddits
        for sub in ["news", "Showerthoughts", "gaming"]:
            print(f"Connected to subreddit: {reddit.subreddit(sub).display_name}")

        return reddit
    except Exception as e:
        print(f"Failed to connect to Reddit: {e}")
        raise

# Call the Reddit connection function
reddit = connect_to_reddit()


# ## Streaming Reddit Posts and Comments to PostgreSQL DB

# In[4]:


# Function to stream submissions (posts)
def stream_posts():
    for submission in reddit.subreddit("news+Showerthoughts+gaming").stream.submissions(skip_existing=True):
        try:
            ingested_time = datetime.now(timezone.utc)
            cursor.execute("""
                INSERT INTO reddit_posts (
                    post_id, title, selftext,
                    author, score, num_comments,
                    created_utc, subreddit, flair,
                    url, over_18, is_self, ingested_at)
                VALUES (
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s);
            """, (
                submission.id,
                submission.title,
                submission.selftext,
                submission.author.name if submission.author else None,
                submission.score,
                submission.num_comments,
                datetime.fromtimestamp(submission.created_utc, tz=timezone.utc),
                submission.subreddit.display_name,
                submission.link_flair_text,
                submission.url,
                submission.over_18,
                submission.is_self,
                ingested_time
            ))
            conn.commit()
            print(f"[Post] {submission.subreddit.display_name}: {submission.title}")
            time.sleep(0.5)
        except Exception as e:
            print("Post insert error:", e)
            conn.rollback()

# Function to stream comments
def stream_comments():
    for comment in reddit.subreddit("news+Showerthoughts+gaming").stream.comments(skip_existing=True):
        try:
            ingested_time = datetime.now(timezone.utc)
            cursor.execute("""
                INSERT INTO reddit_comments (
                    comment_id, body, author,
                    score, created_utc, subreddit,
                    is_submitter, distinguished,
                    parent_id, link_id, ingested_at)
                VALUES (
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s,
                    %s, %s, %s);
            """, (
                comment.id,
                comment.body,
                comment.author.name if comment.author else None,
                comment.score,
                datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                comment.subreddit.display_name,
                comment.is_submitter,
                comment.distinguished,
                comment.parent_id,
                comment.link_id,
                ingested_time
            ))
            conn.commit()
            print(f"[Comment] {comment.subreddit.display_name}: {comment.body[:60]}...")
            time.sleep(0.5)
        except Exception as e:
            print("Comment insert error:", e)
            conn.rollback()

# Start both streams in parallel threads
post_thread = threading.Thread(target=stream_posts, daemon=True)
comment_thread = threading.Thread(target=stream_comments, daemon=True)

post_thread.start()
comment_thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping...")
    cursor.close()
    conn.close()

