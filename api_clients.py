import os
import httpx
import logging
import tweepy

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TwitterClient:
    """Client for interacting with Twitter API"""
    
    def __init__(self):
        # Map environment variables from .env to expected Twitter API keys
        consumer_key = os.environ.get("GH_API", "")
        consumer_secret = os.environ.get("GH_API_SECRET", "")
        access_token = os.environ.get("GH_ACCESS_TOKEN", "")
        access_token_secret = os.environ.get("GH_ACCESS_TOKEN_SECRET", "")
        
        # Check for missing keys
        required_keys = [consumer_key, consumer_secret, access_token, access_token_secret]
        if not all(required_keys):
            raise ValueError("Missing required Twitter API keys")
            
        try:
            # Set up Twitter client
            self.client = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            logging.info("Twitter client initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing Twitter client: {str(e)}")
            raise

    def get_client(self):
        """Get the tweepy client instance"""
        return self.client

class PerplexityClient:
    """Client for interacting with Perplexity AI"""
    
    BASE_URL = "https://api.perplexity.ai/chat/completions"
    
    def __init__(self):
        self.api_key = os.environ.get("GH_PERP_API")
        if not self.api_key:
            raise ValueError("Perplexity API key not found in environment variables")
        
        self.client = httpx.Client()
        logging.info("Perplexity client initialized successfully")

    def _make_request(self, prompt):
        """Make a request to the Perplexity API"""
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        }
        
        response = self.client.post(
            self.BASE_URL,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def generate_sarcastic_tweet(self, last_tweets):
        """Generate a sarcastic tweet using Perplexity AI"""
        prompt = f"""
        Example format for the tweets-

        Trump and Modi announce a trade deal
        Funny that someone has to go all the way across oceans to crack one deal 

        Kohli retires from T20 cricket
        Oh No. All those kohli bashers are unemployed now #jobloss

        Take this format only for reference. Use your creativity to generate a tweet. 

        Steps -

        Content 1: Pick the top news from leading news websites in india - business, sports, entertainment, tech
        Content 2: Also pick the top trending topics in India from twitter as of now.
        Content 3: See what people are talking about this on reddit forums

        Do not pick any topic related to these last tweets : {last_tweets}

        Using both content 1, content 2 and content 3,  generate a funny and witty tweet. Vary the tweet length between 90-260 characters.
        Feel free to make it controversial and sarcastic. Do NOT use any hashtag in the final tweet
        Do not use any bold or italic characters. Output just the final tweet that can posted directly. 
        """
        data = self._make_request(prompt)
        message_content = data["choices"][0]["message"]["content"]
        final_message = message_content.strip('"')
        return final_message
    
    def generate_ai_tweet(self, last_tweets):
        """Generate an AI/data science focused tweet using Perplexity AI"""
        prompt = f"""
        Do not pick any topic related to these last tweets : {last_tweets}

        Pick the latest who said what in the world of AI in the last one day.
        Think like a data scientist geek. Be critical if you need to be. 
        Generate a tweet(under 270 characters) in pointers type, covering the key aspects and what could be the ramifications of this.
        Do NOT use any hashtag in the final tweet.
        Do not use any bold or italic characters. Output just the final tweet that can posted directly.
        """
        data = self._make_request(prompt)
        message_content = data["choices"][0]["message"]["content"]
        final_message = message_content.strip('"')
        return final_message