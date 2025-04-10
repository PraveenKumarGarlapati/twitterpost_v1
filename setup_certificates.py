"""
Setup script to fix SSL certificate issues for Twitter bot
"""
import os
import sys
import subprocess
import logging

# Configure logging if not already configured
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def install_certifi():
    """Install certifi package to fix SSL certificate issues"""
    logging.info("Installing certifi package to fix SSL certificate issues...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "certifi"])
        logging.info("certifi installed successfully")
        return True
    except Exception as e:
        logging.error(f"Failed to install certifi: {e}")
        return False

def setup_environment():
    """Set up SSL certificate environment variables"""
    logging.info("Setting up SSL certificate environment...")
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        logging.info(f"Environment variables set:")
        logging.info(f"  SSL_CERT_FILE = {os.environ['SSL_CERT_FILE']}")
        logging.info(f"  REQUESTS_CA_BUNDLE = {os.environ['REQUESTS_CA_BUNDLE']}")
        return True
    except ImportError:
        logging.error("certifi package not found. Installing...")
        if install_certifi():
            return setup_environment()
        return False
    except Exception as e:
        logging.error(f"Failed to set up environment: {e}")
        return False

def manual_certificate_fix():
    """Instructions for manual certificate fix if automatic setup fails"""
    logging.info("\n=== MANUAL CERTIFICATE FIX ===")
    logging.info("If you continue to have SSL certificate issues, try these steps:")
    logging.info("\n1. Install certifi package:")
    logging.info("   pip install --upgrade certifi")
    logging.info("\n2. Find certificate path:")
    logging.info("   python -m certifi")
    logging.info("\n3. Set environment variables in your terminal:")
    logging.info("   export SSL_CERT_FILE=/path/to/cacert.pem")
    logging.info("   export REQUESTS_CA_BUNDLE=/path/to/cacert.pem")
    logging.info("\n4. Alternatively for macOS, try installing certificates for Python:")
    logging.info("   /Applications/Python 3.x/Install Certificates.command")
    logging.info("\n5. For Windows, verify your system's certificate store is properly configured")
    logging.info("\n=== END OF MANUAL INSTRUCTIONS ===")

def diagnostic_info():
    """Print diagnostic information about the Python environment"""
    logging.info("\n=== DIAGNOSTIC INFO ===")
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Python executable: {sys.executable}")
    logging.info(f"Platform: {sys.platform}")
    
    try:
        import ssl
        logging.info(f"SSL version: {ssl.OPENSSL_VERSION}")
        logging.info(f"Default verify paths: {ssl.get_default_verify_paths()}")
    except ImportError:
        logging.warning("SSL module not available")
    
    logging.info("\nChecking for common packages:")
    for package in ["certifi", "requests", "httpx", "tweepy"]:
        try:
            import importlib
            module = importlib.import_module(package)
            try:
                version = module.__version__
            except AttributeError:
                version = "installed (version unknown)"
            logging.info(f"✓ {package}: {version}")
        except ImportError:
            logging.warning(f"✗ {package}: not installed")
    
    logging.info("=== END OF DIAGNOSTIC INFO ===\n")

if __name__ == "__main__":
    logging.info("=== Twitter Bot SSL Certificate Setup ===")
    diagnostic_info()
    
    if setup_environment():
        logging.info("\nCertificate setup completed successfully")
        logging.info("Try running your Twitter bot code now")
    else:
        logging.error("\nAutomatic certificate setup failed")
        manual_certificate_fix()
    
    logging.info("\nTo use these certificates in your code, add these lines to the top of your scripts:")
    logging.info("import os")
    logging.info("import certifi")
    logging.info("os.environ['SSL_CERT_FILE'] = certifi.where()")
    logging.info("os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()")