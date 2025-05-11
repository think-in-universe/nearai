import json
import requests
import os
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from urllib.parse import urljoin
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class PhalaConfig:
    """Configuration for Phala Cloud API client."""
    base_url: str = os.getenv('PHALA_BASE_URL', 'https://api.phala.cloud')
    api_key: str = os.getenv('PHALA_API_KEY', '')

class PhalaAPIError(Exception):
    """Base exception for Phala API errors."""
    pass

class PhalaClient:
    """Client for interacting with Phala Cloud API."""
    
    def __init__(self, config: Optional[PhalaConfig] = None):
        self.config = config or PhalaConfig()
        if not self.config.api_key:
            raise ValueError("API key is required. Set PHALA_API_KEY environment variable or provide it in PhalaConfig.")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': self.config.api_key
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Phala Cloud API."""
        url = urljoin(self.config.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise PhalaAPIError(f"API request failed: {str(e)}")

    # CVM Management Methods
    def list_cvms(self) -> List[Dict]:
        """List all CVMs associated with the account."""
        return self._make_request('GET', '/api/v1/cvms')

    def create_cvm(self, 
                  name: str,
                  image: str,
                  resources: Dict[str, Union[int, str]],
                  env_vars: Optional[Dict[str, str]] = None) -> Dict:
        """Create a new CVM instance."""
        data = {
            'name': name,
            'image': image,
            'resources': resources,
            'env_vars': env_vars or {}
        }
        return self._make_request('POST', '/api/v1/cvms', data)

    def get_cvm(self, cvm_id: str) -> Dict:
        """Get details of a specific CVM."""
        return self._make_request('GET', f'/api/v1/cvms/{cvm_id}')

    def update_cvm(self, 
                  cvm_id: str,
                  resources: Optional[Dict[str, Union[int, str]]] = None,
                  env_vars: Optional[Dict[str, str]] = None) -> Dict:
        """Update an existing CVM configuration."""
        data = {}
        if resources:
            data['resources'] = resources
        if env_vars:
            data['env_vars'] = env_vars
        return self._make_request('PATCH', f'/api/v1/cvms/{cvm_id}', data)

    def delete_cvm(self, cvm_id: str) -> Dict:
        """Delete a CVM instance."""
        return self._make_request('DELETE', f'/api/v1/cvms/{cvm_id}')

    def start_cvm(self, cvm_id: str) -> Dict:
        """Start a CVM instance."""
        return self._make_request('POST', f'/api/v1/cvms/{cvm_id}/start')

    def stop_cvm(self, cvm_id: str) -> Dict:
        """Stop a CVM instance."""
        return self._make_request('POST', f'/api/v1/cvms/{cvm_id}/stop')

    def get_cvm_logs(self, cvm_id: str, lines: int = 100) -> Dict:
        """Get logs from a CVM instance."""
        return self._make_request('GET', f'/api/v1/cvms/{cvm_id}/logs', {'lines': lines})

    def get_cvm_metrics(self, cvm_id: str) -> Dict:
        """Get metrics for a CVM instance."""
        return self._make_request('GET', f'/api/v1/cvms/{cvm_id}/metrics') 