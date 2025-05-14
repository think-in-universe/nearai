import json
import logging
from typing import Any, Dict, Optional, TypeVar
import requests
from .constants import CLOUD_API_URL
from .credentials import get_api_key

# Set up logging
logger = logging.getLogger(__name__)

T = TypeVar('T')

def safe_stringify(obj: Any) -> str:
    """Safely stringify objects that might contain cyclic references"""
    try:
        return json.dumps(obj)
    except TypeError as error:
        if 'cyclic' in str(error):
            return '[Cyclic Object]'
        return str(obj)

class ApiClient:
    """API client for making requests to the Phala Cloud API"""
    
    def __init__(self, base_url: str):
        """Initialize the API client with the base URL"""
        logger.debug(f"Creating API client with base URL: {base_url}")
        self.base_url = base_url
        self.api_key: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'nearai'
        })
    
    def _ensure_api_key(self) -> None:
        """Ensure we have a valid API key"""
        if not self.api_key:
            self.api_key = get_api_key()
            if not self.api_key:
                raise Exception('API key not found. Please set an API key first with "phala auth login"')
            logger.debug(f"API key loaded: {self.api_key[:5]}...")
    
    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Any:
        """Make an HTTP request with proper error handling"""
        self._ensure_api_key()
        
        headers = kwargs.pop('headers', {})
        headers['X-API-Key'] = self.api_key
        
        full_url = f"{self.base_url}{url}"
        logger.debug(f"Making {method} request to: {full_url}")
        
        try:
            response = self.session.request(
                method,
                full_url,
                json=data,
                headers=headers,
                **kwargs
            )
            
            if response.status_code >= 400:
                error_data = response.json()
                logger.debug(f"Received error response: {response.status_code} - {safe_stringify(error_data)}")
                
                if response.status_code == 401:
                    logger.error('Authentication failed. Please check your API key.')
                elif response.status_code == 403:
                    logger.error('You do not have permission to perform this action.')
                elif response.status_code == 404:
                    logger.error('Resource not found.')
                else:
                    logger.error(f"API Error ({response.status_code}): {error_data.get('message', safe_stringify(error_data))}")
                
                raise Exception(f"API Error: {error_data.get('message', str(error_data))}")
            
            logger.debug(f"Received successful response from: {url}")
            return response.json()
            
        except requests.RequestException as error:
            logger.error('No response received from the server. Please check your internet connection.')
            logger.debug(f"Request details: {safe_stringify(error)[:200]}...")
            raise Exception(f"Network error: {str(error)}")
        except Exception as error:
            logger.error(f"Error: {str(error)}")
            raise
    
    def get(self, url: str, **kwargs: Any) -> Any:
        """Make a GET request"""
        try:
            logger.debug(f"GET request to: {url}")
            return self._make_request('GET', url, **kwargs)
        except Exception as error:
            logger.debug(f"GET request failed: {str(error)}")
            raise
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        """Make a POST request"""
        try:
            logger.debug(f"POST request to: {url}")
            return self._make_request('POST', url, data=data, **kwargs)
        except Exception as error:
            logger.debug(f"POST request failed: {str(error)}")
            raise
    
    def put(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        """Make a PUT request"""
        try:
            logger.debug(f"PUT request to: {url}")
            return self._make_request('PUT', url, data=data, **kwargs)
        except Exception as error:
            logger.debug(f"PUT request failed: {str(error)}")
            raise
    
    def delete(self, url: str, **kwargs: Any) -> Any:
        """Make a DELETE request"""
        try:
            logger.debug(f"DELETE request to: {url}")
            return self._make_request('DELETE', url, **kwargs)
        except Exception as error:
            logger.debug(f"DELETE request failed: {str(error)}")
            raise
    
    def patch(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        """Make a PATCH request"""
        try:
            logger.debug(f"PATCH request to: {url}")
            return self._make_request('PATCH', url, data=data, **kwargs)
        except Exception as error:
            logger.debug(f"PATCH request failed: {str(error)}")
            raise
    
    def close(self) -> None:
        """Close the requests session"""
        self.session.close()

# Create and export a singleton instance
logger.debug(f"Initializing API client with URL: {CLOUD_API_URL}")
api_client = ApiClient(CLOUD_API_URL) 