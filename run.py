#!/usr/bin/env python
"""
Wrapper script to run the Twitter bot with proper environment setup
"""
import os
import sys
import subprocess
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ensure_ssl_certificates():
    """Ensure SSL certificates are properly configured"""
    try:
        # Try to use our centralized configuration first
        from config import config
        if config.setup_ssl_environment():
            logging.info("SSL certificates configured successfully using config.setup_ssl_environment()")
            return True
    except ImportError:
        logging.warning("config module not found, falling back to alternative methods")
    except Exception as e:
        logging.warning(f"Error using config.setup_ssl_environment(): {e}")
    
    # Try setup_certificates module
    try:
        from setup_certificates import setup_environment
        if setup_environment():
            logging.info("SSL certificates configured successfully using setup_certificates")
            return True
    except ImportError:
        logging.warning("setup_certificates module not found, falling back to manual configuration")
    except Exception as e:
        logging.warning(f"Error in setup_certificates: {e}")
    
    # Fallback to manual certificate setup
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        logging.info(f"SSL certificates configured using certifi: {certifi.where()}")
        return True
    except Exception as e:
        logging.error(f"Failed to configure SSL certificates: {e}")
    
    # Last resort - disable SSL verification if allowed
    if os.environ.get("ALLOW_DISABLE_SSL", "").lower() in ("true", "1", "yes"):
        logging.warning("SSL verification disabled as last resort (ALLOW_DISABLE_SSL=true)")
        os.environ["DISABLE_SSL_VERIFICATION"] = "true"
        return True
    
    return False

def ensure_numpy_compatibility():
    """Ensure NumPy version is compatible"""
    try:
        import numpy
        version = numpy.__version__
        
        if version.startswith('2.'):
            logging.warning(f"Detected NumPy {version}, which may cause compatibility issues")
            
            try:
                from fix_numpy import fix_numpy
                if fix_numpy():
                    logging.info("NumPy downgraded successfully")
                    logging.info("Please restart this script for changes to take effect")
                    return False
                else:
                    logging.error("Failed to downgrade NumPy")
                    return False
            except ImportError:
                logging.error("fix_numpy module not found")
                logging.info("You may need to manually install NumPy 1.26.3:")
                logging.info("  pip install numpy==1.26.3")
                return False
            except Exception as e:
                logging.error(f"Error fixing NumPy: {e}")
                return False
        else:
            logging.info(f"NumPy version {version} is compatible")
            return True
    except ImportError:
        logging.info("NumPy not installed, continuing without it")
        return True
    except Exception as e:
        logging.error(f"Error checking NumPy: {e}")
        return True

def run_bot(bot_type="sarcastic", test_mode=True):
    """Run the Twitter bot"""
    if bot_type not in ["sarcastic", "ai"]:
        logging.error(f"Invalid bot type: {bot_type}")
        return False

    script_file = "main.py" if bot_type == "sarcastic" else "main2.py"
    mode_desc = "TEST MODE" if test_mode else "PRODUCTION MODE"
    
    logging.info(f"Running {bot_type} tweet generator in {mode_desc}")
    
    if test_mode:
        script = f"""
import traceback
try:
    from {script_file[:-3]} import test_main
    success = test_main(actually_post=False)
    exit(0 if success else 1)
except Exception as e:
    print(f"Error running bot: {{e}}")
    print(traceback.format_exc())
    exit(1)
"""
    else:
        script = f"""
import traceback
try:
    from {script_file[:-3]} import main
    success = main()
    exit(0 if success else 1)
except Exception as e:
    print(f"Error running bot: {{e}}")
    print(traceback.format_exc())
    exit(1)
"""
    
    # Execute the script with the current Python interpreter
    result = subprocess.call([sys.executable, "-c", script])
    return result == 0

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Twitter Bot Runner")
    parser.add_argument("--production", "-p", action="store_true", 
                        help="Run in production mode (tweets will be posted)")
    parser.add_argument("--disable-ssl", "-d", action="store_true", 
                        help="Disable SSL verification (not recommended)")
    parser.add_argument("--type", "-t", choices=["sarcastic", "ai"], default="sarcastic",
                        help="Type of tweets to generate (sarcastic or ai)")
    return parser.parse_args()

def main():
    """Main entry point for the script"""
    logging.info("=== Twitter Bot Environment Setup ===")
    
    args = parse_arguments()
    test_mode = not args.production
    bot_type = args.type
    
    if args.disable_ssl:
        logging.warning("SSL verification disabled (not recommended)")
        os.environ["DISABLE_SSL_VERIFICATION"] = "true"
    
    # Set up environment
    ssl_success = ensure_ssl_certificates()
    if not ssl_success:
        logging.warning("SSL certificate setup may not be complete")
    
    numpy_success = ensure_numpy_compatibility()
    if not numpy_success:
        logging.info("Please restart this script after fixing NumPy issues")
        return 1
    
    # Run the bot
    success = run_bot(bot_type, test_mode)
    
    if success:
        logging.info("Bot completed successfully")
        return 0
    else:
        logging.error("Bot encountered errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())