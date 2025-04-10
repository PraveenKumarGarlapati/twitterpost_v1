"""
Monkey patches for Tweepy to fix SSL certificate verification issues
"""
import logging
import os
import inspect
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def apply_tweepy_patches():
    """Apply monkey patches to Tweepy to allow disabling SSL verification"""
    try:
        import tweepy
        from tweepy.client import BaseClient
        
        # Check if SSL verification should be disabled
        disable_ssl = os.environ.get("DISABLE_SSL_VERIFICATION", "").lower() in ("true", "1", "yes")
        
        if not disable_ssl:
            logging.info("SSL verification is enabled (default) - no patches applied to Tweepy")
            return True
            
        logging.warning("Applying monkey patches to Tweepy to disable SSL verification - NOT RECOMMENDED FOR PRODUCTION")
        
        # Suppress insecure request warnings
        urllib3.disable_warnings(InsecureRequestWarning)
        
        # Store the original _make_http_request method
        original_make_http_request = BaseClient._make_http_request
        
        def patched_make_http_request(self, *args, **kwargs):
            """Patched method to disable SSL verification in Tweepy requests"""
            # Get the requests session from the client
            session = getattr(self, 'session', None)
            
            # Create a session if it doesn't exist
            if session is None:
                session = requests.Session()
                self.session = session
            
            # Disable SSL verification for this session
            session.verify = False
            
            if '_http_client' in self.__dict__ and hasattr(self._http_client, 'session'):
                self._http_client.session.verify = False
            
            # Call the original method
            return original_make_http_request(self, *args, **kwargs)
        
        # Replace the method with our patched version
        BaseClient._make_http_request = patched_make_http_request
        
        logging.info("Tweepy patches applied successfully - SSL verification disabled")
        return True
        
    except ImportError:
        logging.error("Could not import tweepy - patches not applied")
        return False
    except Exception as e:
        logging.error(f"Error applying Tweepy patches: {e}")
        return False

# Apply patches automatically when module is imported
if __name__ != "__main__":
    apply_tweepy_patches()