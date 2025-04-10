#!/usr/bin/env python
"""
Quick fix for NumPy compatibility issues - downgrade to a compatible version
"""
import subprocess
import sys
import logging

# Configure logging if not already configured
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def fix_numpy():
    """Downgrade NumPy to a compatible version"""
    logging.info("Fixing NumPy compatibility issue...")
    
    # Uninstall current NumPy version
    logging.info("Removing current NumPy installation...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "numpy"])
        logging.info("Successfully removed NumPy")
    except Exception as e:
        logging.warning(f"Warning when removing NumPy: {e}")
    
    # Install compatible version
    logging.info("Installing compatible NumPy version...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.26.3"])
        logging.info("Successfully installed NumPy 1.26.3")
        return True
    except Exception as e:
        logging.error(f"Failed to install NumPy 1.26.3: {e}")
        try:
            logging.info("Trying alternative version...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.4"])
            logging.info("Successfully installed NumPy 1.24.4")
            return True
        except Exception as e2:
            logging.error(f"Failed to install NumPy 1.24.4: {e2}")
            return False

if __name__ == "__main__":
    logging.info("NumPy Compatibility Fixer")
    logging.info("-------------------------")
    success = fix_numpy()
    
    if success:
        logging.info("\nNumPy has been downgraded to a compatible version.")
        logging.info("Please restart your program to use the new version.")
    else:
        logging.error("\nFailed to fix NumPy.")
        logging.info("You may need to manually run: pip install numpy==1.26.3")
        sys.exit(1)