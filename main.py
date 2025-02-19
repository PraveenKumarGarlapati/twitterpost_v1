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
            "content": "I am a social media influencer that posts updates on daily basis. I crave attention and controverty. Sarcasm is in my blood"
        },
        {
            "role": "user",
            "content": f"""
            Example format for the tweets-

            Breaking : Trump and Modi announce a trade deal
            Funny that someone has to go all the way across oceans to crack 1 deal #hellojoke

            Breaking : Kohli retires from T20 cricket
            Oh No. All those kohli bashers are unemployed now #jobloss

            Steps -

            Content 1: Pick the top news from leading news websites in india - business, sports, entertainment, tech
            Content 2: Also pick the top trending topics in India from twitter as of now.
            Content 3: See what people are talking about this on reddit forums

            Do not pick any topic from these last tweets : {last_tweets}

            Using both content 1, content 2 and content 3, please generate a funny and witty tweet. Give more weightate to reddit forums. Feel free to make it controversial and sarcastic. Structure the final tweet as per the given example format. Use only one hashtag in the final tweet
            Output only the final tweet.
            """
        }
    ],
    "max_tokens": 123,
    "temperature": 0.5,
    "top_p": 0.9,
    "search_domain_filter": None,
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "hour",
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

client.create_tweet(text = final_message)

# Get current date and time as a single string
date_time1 = datetime.now().strftime("%y%m%d%H%M%S")
date_time2 = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f+00")

#Storing the tweet to a persistent database
supabase.table("post_logs")\
.insert({"id": date_time1, "created_at": date_time2, "tweet_text": final_message})\
.execute()

# Create a simple dataframe and saves the latest record
data = {
    "created_date": date_time2,
    "tweet_text": final_message
}

df = pd.DataFrame(data)
csv_filename = "latest_tweet_record.csv"  # Change this to your desired local path, e.g., "C:/Users/YourName/Documents/tweets.csv"
df.to_csv(csv_filename, index=False)
print(f"CSV file saved to {csv_filename}")