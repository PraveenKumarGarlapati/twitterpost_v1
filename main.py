import pandas as pd
import os
import tweepy
from gnews import GNews
import google.generativeai as genai

api = GH_API
api_secret = GH_API_SECRET 
access_token = GH_ACCESS_TOKEN
access_token_secret = GH_ACCESS_TOKEN_SECRET
GEMINI_API_KEY = GH_GEMINI_API

## Gets the latest news from India, pickes the top 2
google_news = GNews()
google_news.period = '7d'  # News from last 7 days
google_news.max_results = 5  # number of responses across a keyword
google_news.country = 'India'  # News from a specific country 
google_news.language = 'english' 

news_list = google_news.get_news_by_location('India')
print(news_list)

titles = [item['title'] for item in news_list]
titles_string = ','.join(titles[:2])
print(titles_string)

###############
### Passes the above trending news as a prompt to LLM and gets a quirky tweet.

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content(f"Give me a quirky tweet along with hashtags. Length has to be less than 160 characters. Here are your cues - {titles_string}..")
print(response.text)

###############
### Picks that text and posts to my profile as a new tweet

client = tweepy.Client(
    consumer_key=api,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret= access_token_secret
)

client.create_tweet(text = response.text)



