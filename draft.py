"""
Only used for interim testing
"""

import os
import random
from dotenv import load_dotenv

load_dotenv()
news_api = 'ee7fa319f91c4d948fee37f130acc2fe'
# news_api = os.environ['GH_NEWS_API']

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=news_api)

#Pick a topic at random to get the news
master_list = ['science','business','technology','sports','entertainment']
selected_topic = random.choice(master_list)
# selected_topic = 'india'

all_articles = newsapi.get_top_headlines(sources = 'google-news-in', language = 'en')
sources = newsapi.get_sources(country='in')

# # Get the dump of all news items
# all_articles = newsapi.get_everything(q=selected_topic,
#                                       language='en',
#                                       sort_by='relevancy',
#                                       )