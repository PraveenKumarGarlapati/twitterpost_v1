import tweepy
import time
import pandas as pd
import logging
from datetime import datetime, timezone
from supabase import Client

# Configure logging if not already configured
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def post_tweet_with_retry(client, message, max_retries=3, initial_delay=5):
    """
    Attempt to post a tweet with retries on failure.
    
    Args:
        client (tweepy.Client): The Twitter API client
        message (str): The tweet text to post.
        max_retries (int): Maximum number of retry attempts.
        initial_delay (int): Initial delay in seconds before retrying.
        
    Returns:
        bool: True if tweet was posted successfully, False otherwise.
    """
    attempt = 0
    delay = initial_delay

    while attempt < max_retries:
        try:
            # Attempt to post the tweet
            client.create_tweet(text=message)
            logging.info(f"Tweet posted successfully")
            return True  # Exit function if successful

        except tweepy.errors.Forbidden as e:
            attempt += 1
            logging.warning(f"Attempt {attempt}/{max_retries} failed with 403 Forbidden: {e}")
            
            if attempt == max_retries:
                logging.error("Max retries reached. Tweet could not be posted.")
                return False
            
            # Exponential backoff: delay doubles each retry
            logging.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2
            
        except Exception as e:
            # Handle other unexpected errors
            logging.error(f"Unexpected error: {e}")
            return False
    
    return False

def save_tweet_data(supabase: Client, tweet_text: str):
    """
    Save tweet data to Supabase and local CSV
    
    Args:
        supabase (Client): Supabase client
        tweet_text (str): The text of the tweet
        
    Returns:
        tuple: (date_time1, date_time2) timestamps
    """
    # Get current date and time as a single string
    date_time1 = datetime.now().strftime("%y%m%d%H%M%S")
    date_time2 = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f+00")

    # Storing the tweet to a persistent database
    try:
        supabase.table("post_logs")\
        .insert({"id": date_time1, "created_at": date_time2, "tweet_text": tweet_text})\
        .execute()
        logging.info(f"Tweet saved to Supabase database with ID: {date_time1}")
    except Exception as e:
        logging.error(f"Error saving to Supabase: {e}")

    # Create a simple dataframe and saves the latest record
    try:
        data = {
            "created_date": [date_time2],
            "tweet_text": [tweet_text]
        }

        df = pd.DataFrame(data)
        csv_filename = "latest_tweet_record.csv"
        df.to_csv(csv_filename, index=False)
        logging.info(f"Tweet saved to {csv_filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")
    
    return date_time1, date_time2

def get_previous_tweets(supabase: Client, limit=5):
    """
    Get the most recent tweets from Supabase
    
    Args:
        supabase (Client): Supabase client
        limit (int): Number of tweets to retrieve
        
    Returns:
        str: Concatenated tweet texts
    """
    try:
        sb_data = supabase.table("post_logs").select("*").order('created_at', desc=True).limit(limit).execute()
        if len(sb_data.data) > 0:
            tweets = [tweet['tweet_text'].strip('"') for tweet in sb_data.data]
            logging.info(f"Retrieved {len(tweets)} previous tweets from Supabase")
            return " ".join(tweets)
        logging.info("No previous tweets found in database")
        return ""
    except Exception as e:
        logging.error(f"Error retrieving tweets from Supabase: {e}")
        return ""