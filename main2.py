import pandas as pd
import os
import tweepy
import random
from gnews import GNews
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import os
import requests
import os
from supabase import create_client, Client
import json
from datetime import datetime, timezone
import time



load_dotenv()

#Getting all the necessary keys in
api = os.environ['GH_API']
api_secret = os.environ['GH_API_SECRET'] 
access_token = os.environ['GH_ACCESS_TOKEN']
access_token_secret = os.environ['GH_ACCESS_TOKEN_SECRET']
GEMINI_API_KEY = os.environ['GH_GEMINI_API']
news_api = os.environ['GH_NEWS_API']

perp_api = os.environ['GH_PERP_API']
sb_project_url = os.environ['GH_SB_PROJECT_URL']
sb_api = os.environ['GH_SB_API']

supabase: Client = create_client(sb_project_url, sb_api)

#Fetch data 
# get last 5 tweets
sb_data = supabase.table("post_logs").select("*").execute()
last_tweets = " ".join(tweet['tweet_text'].strip('"') for tweet in sb_data.data[-5:])
print(last_tweets)

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "system",
            "content": "You're a data science leader that is building great products one step at a time - a very practical no-nonsense person"
        },
        {
            "role": "user",
            "content": f"""

            Do not pick any topic related to these last tweets : {last_tweets}

            Pick the latest who said what in the world of AI in the last one day.
            Think like a data scientist geek. Be critical if you need to be. 
            Generate a tweet(under 270 characters) in pointers type, covering the key aspects and what could be the ramifications of this.
            Do NOT use any hashtag in the final tweet.
            Do not use any bold or italic characters. Output just the final tweet that can posted directly.

            """
        }
    ],
    "max_tokens": 150,
    "temperature": 0.5,
    "top_p": 0.9,
    "search_domain_filter": None,
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "day",
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1,
    "response_format": None
}
headers = {
    "Authorization": f"Bearer {perp_api}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

data = response.json()
print(data)
message_content = data["choices"][0]["message"]["content"]
final_message = message_content.strip('"')
print(final_message)


# Creation of Twitter client to post to my profile 
client = tweepy.Client(
    consumer_key=api,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret= access_token_secret
)

# client.create_tweet(text = final_message)

##
def post_tweet_with_retry(message, max_retries=2, initial_delay=10):
    """
    Attempt to post a tweet with retries on 403 Forbidden error.
    
    Args:
        message (str): The tweet text to post.
        max_retries (int): Maximum number of retry attempts.
        initial_delay (int): Initial delay in seconds before retrying.
    """
    attempt = 0
    delay = initial_delay

    while attempt < max_retries:
        try:
            # Attempt to post the tweet
            client.create_tweet(text=message)
            print(f"Tweet posted successfully: '{message}'")
            return  # Exit function if successful

        except tweepy.errors.Forbidden as e:
            attempt += 1
            print(f"Attempt {attempt}/{max_retries} failed with 403 Forbidden: {e}")
            
            if attempt == max_retries:
                print("Max retries reached. Tweet could not be posted.")
                break
            
            # Exponential backoff: delay doubles each retry (5s, 10s, 20s, etc.)
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2

        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error: {e}")
            break

post_tweet_with_retry(final_message)
##


# Get current date and time as a single string
date_time1 = datetime.now().strftime("%y%m%d%H%M%S")
date_time2 = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f+00")

#Storing the tweet to a persistent database
supabase.table("post_logs")\
.insert({"id": date_time1, "created_at": date_time2, "tweet_text": final_message})\
.execute()

# Create a simple dataframe and saves the latest record
data = {
    "created_date": [date_time2],
    "tweet_text": [final_message]
}

df = pd.DataFrame(data)
csv_filename = "latest_tweet_record.csv"  # Change this to your desired local path, e.g., "C:/Users/YourName/Documents/tweets.csv"
df.to_csv(csv_filename, index=False)
print(f"CSV file saved to {csv_filename}")