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
sb_response = supabase.table("post_logs").select("*").execute()


last_tweets = []

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
            Pick a topic that is trending in the last hour in India as of today.
            Ensure you pick a topic that is not from the last 10 tweets that I posted. 
            Last 10 tweets : {last_tweets}
            Make a funny, witty tweet on the same news. Feel free to make it controversial and sarcastic. 
            Output only the final tweet.
            """
        }
    ],
    "max_tokens": 123,
    "temperature": 0.2,
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
print(message_content)


# Creation of Twitter client to post to my profile 
client = tweepy.Client(
    consumer_key=api,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret= access_token_secret
)


client.create_tweet(text = message_content)
