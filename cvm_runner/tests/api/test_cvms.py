import pytest
import json
from dotenv import load_dotenv
from cvm_runner.phala.api.cvms import (
    get_cvms,
    get_cvm_by_app_id,
    get_cvm_network
)

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def app_id():
    return "8fb563b65a0bc7e3f00e7951e2f0595068b3949b"

@pytest.mark.integration
def test_list_cvms():
    """Integration test to list CVMs from Phala Cloud."""
    try:
        cvms = get_cvms()
        print("\n=== CVM List ===")
        print(f"Found {len(cvms)} CVMs")
        
        for cvm in cvms:
            hosted = cvm.get('hosted')
            if hosted:
                print(f"- CVM ID: {hosted.get('id')}")
                print(f"  Name: {hosted.get('name')}")
                print(f"  Status: {hosted.get('status')}")
                print(f"  Uptime: {hosted.get('uptime')}")
                print(f"  App URL: {hosted.get('app_url')}")
                print(f"  App ID: {hosted.get('app_id')}")
                print(f"  Instance ID: {hosted.get('instance_id')}")
                print(f"  Image Version: {hosted.get('image_version')}")
                print("---")

        print("================")
        
    except Exception as e:
        pytest.fail(f"Failed to list CVMs: {str(e)}")

@pytest.mark.integration
def test_get_cvm(app_id):
    """Integration test to get a specific CVM by app_id."""
    try:
        cvm = get_cvm_by_app_id(app_id)
        print(f"CVM with app_id ({app_id}): {json.dumps(cvm, indent=2)}")
    except Exception as e:
        pytest.fail(f"Failed to get CVM: {str(e)}")

@pytest.mark.integration
def test_get_cvm_network(app_id):
    """Integration test to get network information for a CVM."""
    try:
        network = get_cvm_network(app_id)
        print(f"CVM network with app_id ({app_id}): {json.dumps(network, indent=2)}")
    except Exception as e:
        pytest.fail(f"Failed to get CVM network: {str(e)}")
