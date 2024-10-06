import pandas as pd
import os
import tweepy
import random
from gnews import GNews
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

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
master_list = ['AI','business','finance','sports','politics']
selected_topic = random.choice(master_list)

# Get the dump of all news items
all_articles = newsapi.get_everything(q=selected_topic,
                                      language='en',
                                      sort_by='relevancy'
                                      )


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

Don't go with the first one. See all the topics covered and pick one that has a scope for witty humor
If you can find some content for India, give it more weightage
Keep it under 280 characters. 
Use informal, contemporary internet language
Include either humor, irony, or a controversial-yet-acceptable take
Occasionally use emojis.
Reference current memes or trends when relevant
Make it shareable and engaging
Include hastags for twitter

Tone variations (use a mix of these two):
Sarcastic observer
Chaotic good energy

Give out only 1 tweet
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
