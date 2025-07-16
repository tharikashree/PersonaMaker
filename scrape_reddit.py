import praw
from dotenv import dotenv_values
from datetime import datetime
import logging
import dotenv

env = dotenv_values(".env")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialize Reddit instance using PRAW
reddit = praw.Reddit(
    client_id=env["REDDIT_CLIENT_ID"],
    client_secret=env["REDDIT_CLIENT_SECRET"],
    user_agent=env["REDDIT_USER_AGENT"]
)

def get_user_content(username, max_posts=20, max_comments=20):
    user = reddit.redditor(username)

    posts = []
    comments = []

    # Scrape user's posts
    logging.info(f"Fetching up to {max_posts} posts for u/{username}")
    try:
        for post in user.submissions.new(limit=max_posts):
            posts.append(post.title + " — " + post.selftext)
    except Exception as e:
        logging.warning(f"Error fetching posts for u/{username}: {e}")

    # Scrape user's comments
    logging.info(f"Fetching up to {max_comments} comments for u/{username}")
    try:
        for comment in user.comments.new(limit=max_comments):
            comments.append(comment.body)
    except Exception as e:
        logging.warning(f"Error fetching comments for u/{username}: {e}")

    return posts, comments
