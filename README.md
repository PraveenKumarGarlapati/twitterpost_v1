# Twitter Bot - Automated Content Generator

An automated Twitter posting system that uses AI to generate and publish content on scheduled intervals.

## Overview

This bot automatically generates and posts tweets on a schedule using AI services. It has two different tweet generation processes:

1. **Sarcastic/Controversial Content** (`main.py`): Generates witty, sarcastic tweets based on trending news and topics.
2. **Data Science/AI Content** (`main2.py`): Creates tweets focused on latest AI developments with a data scientist's perspective.

## Project Structure

```
twitterpost_v1/
├── .github/workflows/      # GitHub Actions workflow files
│   ├── actions.yml         # Workflow for sarcastic tweets
│   └── actions2.yml        # Workflow for AI/data science tweets
├── config.py               # Configuration settings and environment variables
├── api_clients.py          # API client interfaces for Twitter and Perplexity
├── utils.py                # Common utility functions
├── main.py                 # Sarcastic tweet generator script
├── main2.py                # AI/Data Science tweet generator script
├── requirements.txt        # Project dependencies
├── .env                    # Local environment variables (not in git)
└── latest_tweet_record.csv # Local record of the most recent tweet
```

## Features

- **Content Generation**: Uses Perplexity AI to generate unique tweet content
- **Topic Tracking**: Ensures no topic repetition by checking previous tweets
- **Automatic Posting**: Posts to Twitter via the Twitter API (using Tweepy)
- **Retry Mechanism**: Handles Twitter API failures with automatic retries
- **Data Persistence**: Stores tweet history in both Supabase and local CSV

## Automation

The bot is automatically run on scheduled intervals using GitHub Actions:

- `actions.yml`: Runs `main.py` every 2 days at multiple times (4:30, 9:30, 14:30, 18:30 UTC)
- `actions2.yml`: Runs `main2.py` every 2 days at different times (1:30, 4:30, 7:30, 12:30, 15:30 UTC)

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with all required API keys (see `.env.example`)
4. Run locally with `python main.py` or `python main2.py`

## Environment Variables

The following environment variables need to be set either in a `.env` file (local development) or as GitHub Secrets (for automation):

- `GH_API`: Twitter API key
- `GH_API_SECRET`: Twitter API secret
- `GH_ACCESS_TOKEN`: Twitter access token
- `GH_ACCESS_TOKEN_SECRET`: Twitter access token secret
- `GH_GEMINI_API`: Google Gemini API key
- `GH_NEWS_API`: News API key
- `GH_PERP_API`: Perplexity API key
- `GH_SB_PROJECT_URL`: Supabase project URL
- `GH_SB_API`: Supabase API key
