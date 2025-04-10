import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class Config:
    """Central configuration for the Twitter posting application"""
    
    # Twitter API credentials
    TWITTER_API_KEY = os.environ.get('GH_API')
    TWITTER_API_SECRET = os.environ.get('GH_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('GH_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('GH_ACCESS_TOKEN_SECRET')
    
    # AI services
    PERPLEXITY_API_KEY = os.environ.get('GH_PERP_API')
    
    # Supabase
    SUPABASE_URL = os.environ.get('GH_SB_PROJECT_URL')
    SUPABASE_KEY = os.environ.get('GH_SB_API')
    
    # Retry settings
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 5
    
    @classmethod
    def get_supabase_client(cls) -> Client:
        """Get a configured Supabase client"""
        if not cls.SUPABASE_URL or not cls.SUPABASE_KEY:
            raise ValueError("Missing Supabase configuration")
        return create_client(cls.SUPABASE_URL, cls.SUPABASE_KEY)

# Create a singleton config instance
config = Config()