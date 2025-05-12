import pytest
import os
from dotenv import load_dotenv
from cvm_runner.phala.cvms import PhalaConfig, PhalaClient, PhalaAPIError

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def config():
    return PhalaConfig(
        base_url=os.getenv('PHALA_BASE_URL', 'https://cloud-api.phala.network'),
        api_key=os.getenv('PHALA_API_KEY', 'test_api_key')
    )

@pytest.fixture
def client(config):
    return PhalaClient(config)

def test_client_initialization(config):
    client = PhalaClient(config)
    assert client.config == config
    assert client.session.headers["Content-Type"] == "application/json"
    assert client.session.headers["X-API-Key"] == config.api_key

@pytest.mark.integration
def test_list_cvms(client):
    """Integration test to list CVMs from Phala Cloud."""
    try:
        cvms = client.list_cvms(user_id="robertyan")
        print("\n=== CVM List ===")
        print(f"Found {len(cvms)} CVMs")
        
        for cvm in cvms:
            data = cvm.get('hosted')
            print(f"- CVM ID: {data.get('id')}")
            print(f"  Name: {data.get('name')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Uptime: {data.get('uptime')}")
            print(f"  App URL: {data.get('app_url')}")
            print(f"  App ID: {data.get('app_id')}")
            print(f"  Instance ID: {data.get('instance_id')}")
            print(f"  Image Version: {data.get('image_version')}")
            print("---")

        print("================")
        
    except PhalaAPIError as e:
        pytest.fail(f"Failed to list CVMs: {str(e)}")
