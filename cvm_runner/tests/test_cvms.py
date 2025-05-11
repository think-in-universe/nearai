import pytest
from unittest.mock import Mock, patch
import requests
import os
from dotenv import load_dotenv
from cvm_runner.phala.cvms import PhalaConfig, PhalaClient, PhalaAPIError

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def config():
    return PhalaConfig(
        base_url=os.getenv('PHALA_BASE_URL', 'https://api.phala.cloud'),
        api_key=os.getenv('PHALA_API_KEY', 'test_api_key')
    )

@pytest.fixture
def client(config):
    return PhalaClient(config)

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {"status": "success"}
    mock.raise_for_status = Mock()
    return mock

def test_client_initialization(config):
    print(f"\nDEBUG: Config API Key: {config.api_key}")  # Debug print
    client = PhalaClient(config)
    assert client.config == config
    assert client.session.headers["Content-Type"] == "application/json"
    assert client.session.headers["X-API-Key"] == config.api_key

@patch('requests.Session.request')
def test_list_cvms(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.list_cvms()
    mock_request.assert_called_once_with(
        method='GET',
        url='https://api.phala.cloud/api/v1/cvms',
        json=None
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_create_cvm(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    resources = {"cpu": 2, "memory": "4Gi"}
    env_vars = {"ENV_VAR1": "value1"}
    
    result = client.create_cvm(
        name="test-cvm",
        image="phala/cvm-base:latest",
        resources=resources,
        env_vars=env_vars
    )
    
    mock_request.assert_called_once_with(
        method='POST',
        url='https://api.phala.cloud/api/v1/cvms',
        json={
            'name': 'test-cvm',
            'image': 'phala/cvm-base:latest',
            'resources': resources,
            'env_vars': env_vars
        }
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_get_cvm(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.get_cvm("cvm-123")
    mock_request.assert_called_once_with(
        method='GET',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123',
        json=None
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_update_cvm(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    resources = {"cpu": 4, "memory": "8Gi"}
    env_vars = {"ENV_VAR2": "value2"}
    
    result = client.update_cvm(
        cvm_id="cvm-123",
        resources=resources,
        env_vars=env_vars
    )
    
    mock_request.assert_called_once_with(
        method='PATCH',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123',
        json={
            'resources': resources,
            'env_vars': env_vars
        }
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_delete_cvm(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.delete_cvm("cvm-123")
    mock_request.assert_called_once_with(
        method='DELETE',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123',
        json=None
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_start_cvm(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.start_cvm("cvm-123")
    mock_request.assert_called_once_with(
        method='POST',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123/start',
        json=None
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_stop_cvm(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.stop_cvm("cvm-123")
    mock_request.assert_called_once_with(
        method='POST',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123/stop',
        json=None
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_get_cvm_logs(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.get_cvm_logs("cvm-123", lines=50)
    mock_request.assert_called_once_with(
        method='GET',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123/logs',
        json={'lines': 50}
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_get_cvm_metrics(mock_request, client, mock_response):
    mock_request.return_value = mock_response
    result = client.get_cvm_metrics("cvm-123")
    mock_request.assert_called_once_with(
        method='GET',
        url='https://api.phala.cloud/api/v1/cvms/cvm-123/metrics',
        json=None
    )
    assert result == {"status": "success"}

@patch('requests.Session.request')
def test_api_error_handling(mock_request, client):
    mock_request.side_effect = requests.exceptions.RequestException("API Error")
    with pytest.raises(PhalaAPIError) as exc_info:
        client.list_cvms()
    assert "API request failed: API Error" in str(exc_info.value)

@patch('requests.Session.request')
def test_http_error_handling(mock_request, client):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_request.return_value = mock_response
    
    with pytest.raises(PhalaAPIError) as exc_info:
        client.list_cvms()
    assert "API request failed: 404 Not Found" in str(exc_info.value)
