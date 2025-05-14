"""
Integration tests for CVM commands.
"""

import pytest
import json
from pathlib import Path
from cvm_runner.phala.commands.list import list_cvms
from cvm_runner.phala.commands.get import get_cvm
from cvm_runner.phala.commands.create import create_new_cvm

@pytest.fixture
def app_id():
    """Fixture to provide a test app_id."""
    return "8fb563b65a0bc7e3f00e7951e2f0595068b3949b"

@pytest.fixture
def compose_file(tmp_path):
    """Fixture to provide a test docker-compose file."""
    compose_content = """version: '3.8'
services:
  app:
    image: test-image:latest
    container_name: test-app
    volumes:
      - /var/run/tappd.sock:/var/run/tappd.sock
    restart: always
"""
    compose_path = tmp_path / "docker-compose.yml"
    compose_path.write_text(compose_content)
    return str(compose_path)

@pytest.mark.integration
def test_list_cvms():
    """Integration test for listing CVMs."""
    try:
        # Test regular output
        cvms = list_cvms()
        assert isinstance(cvms, list), "Should return a list"
        
        if cvms:  # If there are any CVMs
            cvm = cvms[0]
            assert isinstance(cvm, dict), "Each CVM should be a dictionary"
            
            # Check required fields
            assert "name" in cvm, "CVM should have a name"
            assert "status" in cvm, "CVM should have a status"
            assert "hosted" in cvm, "CVM should have hosted data"
            
            hosted = cvm["hosted"]
            assert isinstance(hosted, dict), "Hosted data should be a dictionary"
            assert "app_id" in hosted, "Hosted data should have app_id"
            assert "app_url" in hosted, "Hosted data should have app_url"
            assert "instance_id" in hosted, "Hosted data should have instance_id"
            assert "image_version" in hosted, "Hosted data should have image_version"
            
            # Print CVM details for inspection
            print("\n=== CVM List ===")
            print(f"Found {len(cvms)} CVMs")
            for cvm in cvms:
                hosted = cvm.get("hosted", {})
                print(f"- CVM ID: {hosted.get('id')}")
                print(f"  Name: {cvm.get('name')}")
                print(f"  Status: {cvm.get('status')}")
                print(f"  App URL: {hosted.get('app_url')}")
                print(f"  App ID: {hosted.get('app_id')}")
                print(f"  Instance ID: {hosted.get('instance_id')}")
                print(f"  Image Version: {hosted.get('image_version')}")
                print("---")
            print("================")
        
        # Test JSON output
        cvms_json = list_cvms(json_output=True)
        assert isinstance(cvms_json, list), "JSON output should return a list"
        
        # Verify JSON output matches regular output
        assert len(cvms_json) == len(cvms), "JSON output should have same length as regular output"
        
    except Exception as e:
        pytest.fail(f"Failed to list CVMs: {str(e)}")

@pytest.mark.integration
def test_get_cvm(app_id):
    """Integration test for getting a specific CVM."""
    try:
        # Test regular output
        cvm = get_cvm(app_id)
        assert isinstance(cvm, dict), "Should return a dictionary"
        
        # Check required fields
        assert "id" in cvm, "CVM should have an ID"
        assert "name" in cvm, "CVM should have a name"
        assert "status" in cvm, "CVM should have a status"
        assert "app_id" in cvm, "CVM should have app_id"
        assert "vm_uuid" in cvm, "CVM should have vm_uuid"
        assert "instance_id" in cvm, "CVM should have instance_id"
        assert "vcpu" in cvm, "CVM should have vcpu"
        assert "memory" in cvm, "CVM should have memory"
        assert "disk_size" in cvm, "CVM should have disk_size"
        assert "base_image" in cvm, "CVM should have base_image"
        assert "dapp_dashboard_url" in cvm, "CVM should have dapp_dashboard_url"
        
        # Print CVM details for inspection
        print("\n=== CVM Details ===")
        print(f"ID: {cvm.get('id')}")
        print(f"Name: {cvm.get('name')}")
        print(f"Status: {cvm.get('status')}")
        print(f"App ID: {cvm.get('app_id')}")
        print(f"VM UUID: {cvm.get('vm_uuid')}")
        print(f"Instance ID: {cvm.get('instance_id')}")
        print(f"vCPU: {cvm.get('vcpu')}")
        print(f"Memory: {cvm.get('memory')} MB")
        print(f"Disk Size: {cvm.get('disk_size')} GB")
        print(f"Base Image: {cvm.get('base_image')}")
        print(f"Dashboard URL: {cvm.get('dapp_dashboard_url')}")
        print(f"System Log Endpoint: {cvm.get('syslog_endpoint')}")
        print("==================")

        # Test JSON output
        cvm_json = get_cvm(app_id, json_output=True)
        assert isinstance(cvm_json, dict), "JSON output should return a dictionary"

        # Verify JSON output matches regular output
        assert cvm_json == cvm, "JSON output should match regular output"

    except Exception as e:
        pytest.fail(f"Failed to get CVM: {str(e)}")

@pytest.mark.integration
def test_create_cvm(compose_file):
    """Integration test for creating a new CVM."""
    try:
        # Test creating a new CVM
        cvm = create_new_cvm(
            name="test-cvm",
            compose_file=compose_file,
            vcpu=2,
            memory=4096,
            disk_size=40,
            debug=True
        )

        assert isinstance(cvm, dict), "Should return a dictionary"
        
        # Check required fields
        assert "id" in cvm, "CVM should have an ID"
        assert "name" in cvm, "CVM should have a name"
        assert cvm["name"] == "test-cvm", "CVM name should match"
        assert "status" in cvm, "CVM should have a status"
        assert "app_id" in cvm, "CVM should have app_id"
        assert "vm_uuid" in cvm, "CVM should have vm_uuid"
        assert "instance_id" in cvm, "CVM should have instance_id"
        assert "vcpu" in cvm, "CVM should have vcpu"
        assert cvm["vcpu"] == 2, "vCPU should match"
        assert "memory" in cvm, "CVM should have memory"
        assert cvm["memory"] == 4096, "Memory should match"
        assert "disk_size" in cvm, "CVM should have disk_size"
        assert cvm["disk_size"] == 40, "Disk size should match"

        # Print CVM details for inspection
        print("\n=== Created CVM Details ===")
        print(f"ID: {cvm.get('id')}")
        print(f"Name: {cvm.get('name')}")
        print(f"Status: {cvm.get('status')}")
        print(f"App ID: {cvm.get('app_id')}")
        print(f"VM UUID: {cvm.get('vm_uuid')}")
        print(f"Instance ID: {cvm.get('instance_id')}")
        print(f"vCPU: {cvm.get('vcpu')}")
        print(f"Memory: {cvm.get('memory')} MB")
        print(f"Disk Size: {cvm.get('disk_size')} GB")
        print(f"Base Image: {cvm.get('base_image')}")
        print(f"Dashboard URL: {cvm.get('dapp_dashboard_url')}")
        print(f"System Log Endpoint: {cvm.get('syslog_endpoint')}")
        print("=========================")

    except Exception as e:
        pytest.fail(f"Failed to create CVM: {str(e)}")
