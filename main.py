import pandas as pd
import os
import tweepy
import random
from gnews import GNews
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import os

load_dotenv()

#Getting all the necessary keys in
api = os.environ['GH_API']
api_secret = os.environ['GH_API_SECRET'] 
access_token = os.environ['GH_ACCESS_TOKEN']
access_token_secret = os.environ['GH_ACCESS_TOKEN_SECRET']
GEMINI_API_KEY = os.environ['GH_GEMINI_API']
news_api = os.environ['GH_NEWS_API']


###############

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=news_api)

#Pick a topic at random to get the news
master_list = ['science','business','technology','sports','entertainment']
selected_topic = random.choice(master_list)

# Get the dump of all news items
all_articles = newsapi.get_top_headlines(sources = 'google-news-in', language = 'en')

# all_articles = newsapi.get_everything(q=selected_topic,
#                                       language='en',
#                                       sort_by='relevancy'
#                                       )


### Setup LLM API Key

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-pro")
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,      
    }

## Defining an elaborate prompt to generate the tweet

prompt = f"""

{all_articles}

You are a witty social media expert who creates engaging, quirky tweets that get high engagement. Your task is to create a tweet based on the given text

Guidelines for tweet creation:

Don't go with the first one. See all the topics covered and prioritise one that has a scope for witty humor
Use contemporary Internet language
Include a humorous take
Occasionally use emojis.
Make it shareable and engaging. Add a call to action if necessary.
Include hastags for twitter

Tone variations (use a mix of these two):
Keen observer
Chaotic good energy

Give out only 1 tweet. Keep it under 280 characters. 
"""

response = model.generate_content(prompt,
    safety_settings = safety_settings)
print(response.text)

# Creation of Twitter client to post to my profile 
client = tweepy.Client(
    consumer_key=api,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret= access_token_secret
)


client.create_tweet(text = response.text)
