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
from datetime import datetime, timezone, timedelta
import boto3

load_dotenv()  # Loads variables from .env file in root

# Connect to PostgreSQL
conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )

# Set export threshold (e.g., 7 days ago)
threshold = datetime.now() - timedelta(days=7)

# Query older data
posts_query = "SELECT * FROM reddit_posts WHERE timestamp < %s;"
posts_df = pd.read_sql(posts_query, conn, params=[threshold])

comments_query = "SELECT * FROM reddit_comments WHERE timestamp < %s;"
comments_df = pd.read_sql(comments_query, conn, params=[threshold])

# Save as CSV
posts_filename = f"archived_reddit_posts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
posts_df.to_csv(posts_filename, index=False)

comments_filename = f"archived_reddit_comments_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
comments_df.to_csv(comments_filename, index=False)

# Upload to S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket = os.getenv("S3_BUCKET_NAME")

try:
    s3.upload_file(posts_filename, bucket, posts_filename)
    s3.upload_file(comments_filename, bucket, comments_filename)
    print("Upload to S3 successful.")
    print(f"Archived {len(posts_df)} posts and {len(comments_df)} comments.")
except Exception as e:
    print(f"Error uploading to S3: {e}")

# Optional: delete rows from DB after archiving
with conn.cursor() as cur:
    cur.execute("DELETE FROM reddit_posts WHERE timestamp < %s;", (threshold,))
    cur.execute("DELETE FROM reddit_comments WHERE timestamp < %s;", (threshold,))
    conn.commit()

conn.close()