import os
import logging

logger = logging.getLogger(__name__)

# Environment variable name for the API key
API_KEY_ENV_VAR = 'PHALA_API_KEY'

def get_api_key() -> str:
    """
    Get the API key from environment variable.
    
    Returns:
        str: The API key if found
        
    Raises:
        Exception: If no API key is found in environment variables
    """
    api_key = os.getenv(API_KEY_ENV_VAR)
    
    if not api_key:
        logger.error(f"No API key found. Please set the {API_KEY_ENV_VAR} environment variable.")
        raise Exception(f"API key not found. Please set the {API_KEY_ENV_VAR} environment variable.")
    
    logger.debug(f"API key loaded from environment variable {API_KEY_ENV_VAR}")
    return api_key 