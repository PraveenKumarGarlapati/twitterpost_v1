"""
Sarcastic tweet generator that posts to Twitter
"""
from config import config
from utils import post_tweet_with_retry, save_tweet_data, get_previous_tweets
from api_clients import TwitterClient, PerplexityClient
import traceback
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_main(actually_post=False):
    """Test function to verify functionality without posting to Twitter"""
    try:
        # Get Supabase client
        supabase = config.get_supabase_client()
        logging.info("Supabase client connected successfully")
        
        # Get previous tweets to avoid repetition
        try:
            last_tweets = get_previous_tweets(supabase)
            tweet_count = last_tweets.count(' ') + 1 if last_tweets else 0
            logging.info(f"Retrieved {tweet_count} previous tweets")
        except Exception as e:
            logging.error(f"Error retrieving previous tweets: {str(e)}")
            last_tweets = ""
        
        # Initialize API clients
        twitter_client = TwitterClient()
        perplexity_client = PerplexityClient()
        logging.info("API clients initialized")
        
        # Generate tweet content
        logging.info("Generating sarcastic tweet...")
        final_message = perplexity_client.generate_sarcastic_tweet(last_tweets)
        logging.info(f"Generated tweet: \"{final_message}\"")
        
        if actually_post:
            # Post to Twitter and save tweet data
            success = post_and_save_tweet(twitter_client, supabase, final_message)
            return success
        else:
            logging.info("TEST MODE: Tweet not actually posted to Twitter")
            return True
            
    except Exception as e:
        logging.error(f"Error during test: {str(e)}")
        logging.debug(traceback.format_exc())
        return False

def post_and_save_tweet(twitter_client, supabase, final_message):
    """Helper function to post tweet and save data"""
    try:
        # Post to Twitter
        logging.info("Posting to Twitter...")
        success = post_tweet_with_retry(
            twitter_client.get_client(), 
            final_message,
            config.MAX_RETRIES,
            config.INITIAL_RETRY_DELAY
        )
        
        if success:
            # Save tweet data to database and CSV
            save_tweet_data(supabase, final_message)
            logging.info("Tweet posted and saved successfully")
            return True
        else:
            logging.error("Failed to post tweet after retries")
            return False
            
    except Exception as e:
        logging.error(f"Error posting/saving tweet: {str(e)}")
        logging.debug(traceback.format_exc())
        return False

def main():
    """Main function to generate and post a sarcastic tweet"""
    try:
        # Get Supabase client
        supabase = config.get_supabase_client()
        
        # Get previous tweets to avoid repetition
        last_tweets = get_previous_tweets(supabase)
        
        # Initialize API clients
        twitter_client = TwitterClient()
        perplexity_client = PerplexityClient()
        
        # Generate tweet content
        logging.info("Generating sarcastic tweet...")
        final_message = perplexity_client.generate_sarcastic_tweet(last_tweets)
        logging.info(f"Generated tweet: {final_message}")
        
        # Post to Twitter and save data
        return post_and_save_tweet(twitter_client, supabase, final_message)
            
    except Exception as e:
        logging.error(f"Error in tweet generation process: {str(e)}")
        logging.debug(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Change this line to test_main() to test without posting
    # or test_main(actually_post=True) to test with posting
    main()