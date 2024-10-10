"""
Only used for interim testing
"""

import os
import random
from dotenv import load_dotenv

load_dotenv()

news_api = os.environ['GH_NEWS_API']

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=news_api)

#Pick a topic at random to get the news
master_list = ['AI','business','finance','sports','politics']
selected_topic = random.choice(master_list)
selected_topic = 'india'

# Get the dump of all news items
all_articles = newsapi.get_everything(q=selected_topic,
                                      language='en',
                                      sort_by='relevancy',
                                      )