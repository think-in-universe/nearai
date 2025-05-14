"""
Integration tests for CVM commands.
"""

import pytest
from cvm_runner.phala.tasks.cvms.list import list_cvms
from cvm_runner.phala.tasks.cvms.get import get_cvm
from cvm_runner.phala.tasks.cvms.create import create_new_cvm
from cvm_runner.phala.tasks.cvms.start import start_cvm_instance
from cvm_runner.phala.tasks.cvms.stop import stop_cvm_instance
from cvm_runner.phala.tasks.cvms.restart import restart_cvm_instance
from cvm_runner.phala.tasks.cvms.resize import resize_cvm_instance
from cvm_runner.phala.tasks.cvms.delete import delete_cvm_instance
from cvm_runner.phala.tasks.cvms.attestation import get_cvm_attestation_info


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

@pytest.mark.integration
def test_start_cvm(app_id):
    """Integration test for starting a CVM."""
    try:
        # First stop the CVM
        stop_cvm_instance(app_id)
        
        # Then start it
        response = start_cvm_instance(app_id)
        
        assert isinstance(response, dict), "Should return a dictionary"
        assert response["app_id"] == app_id, "App ID should match"
        assert response["status"] == "starting", "Status should be starting"
        
        print("\n=== Started CVM ===")
        print(f"App ID: {response.get('app_id')}")
        print(f"Status: {response.get('status')}")
        print("==================")
        
    except Exception as e:
        pytest.fail(f"Failed to start CVM: {str(e)}")

@pytest.mark.integration
def test_stop_cvm(app_id):
    """Integration test for stopping a CVM."""
    try:
        # First ensure it's running
        start_cvm_instance(app_id)
        
        # Then stop it
        response = stop_cvm_instance(app_id)
        
        assert isinstance(response, dict), "Should return a dictionary"
        assert response["app_id"] == app_id, "App ID should match"
        assert response["status"] == "stopped", "Status should be stopped"

        print("\n=== Stopped CVM ===")
        print(f"App ID: {response.get('app_id')}")
        print(f"Status: {response.get('status')}")
        print("==================")
        
    except Exception as e:
        pytest.fail(f"Failed to stop CVM: {str(e)}")

@pytest.mark.integration
def test_restart_cvm(app_id):
    """Integration test for restarting a CVM."""
    try:
        # First ensure it's running
        start_cvm_instance(app_id)
        
        # Then restart it
        response = restart_cvm_instance(app_id)
        
        assert isinstance(response, dict), "Should return a dictionary"
        assert response["app_id"] == app_id, "App ID should match"
        assert response["status"] == "stopped", "Status should be stopped"

        print("\n=== Restarted CVM ===")
        print(f"App ID: {response.get('app_id')}")
        print(f"Status: {response.get('status')}")
        print("=====================")
        
    except Exception as e:
        pytest.fail(f"Failed to restart CVM: {str(e)}")

@pytest.mark.integration
def test_resize_cvm(app_id):
    """Integration test for resizing a CVM."""
    try:
        new_vcpu = 4
        new_memory = 8192
        
        response = resize_cvm_instance(
            app_id=app_id,
            vcpu=new_vcpu,
            memory=new_memory
        )
        
        assert isinstance(response, dict), "Should return a dictionary"
        assert response["app_id"] == app_id, "App ID should match"
        assert response["vcpu"] == new_vcpu, "vCPU should be updated"
        assert response["memory"] == new_memory, "Memory should be updated"
        
        print("\n=== Resized CVM ===")
        print(f"App ID: {response.get('app_id')}")
        print(f"vCPU: {response.get('vcpu')}")
        print(f"Memory: {response.get('memory')} MB")
        print("===================")
        
    except Exception as e:
        pytest.fail(f"Failed to resize CVM: {str(e)}")

@pytest.mark.integration
def test_delete_cvm(app_id):
    """Integration test for deleting a CVM."""
    try:
        response = delete_cvm_instance(app_id)
        
        assert isinstance(response, dict), "Should return a dictionary"
        assert response["success"] is True, "Delete operation should be successful"
        
        print("\n=== Deleted CVM ===")
        print(f"Success: {response.get('success')}")
        print("===================")
        
    except Exception as e:
        pytest.fail(f"Failed to delete CVM: {str(e)}")

@pytest.mark.integration
def test_resize_cvm_validation():
    """Integration test for resize CVM validation."""
    try:
        # Test no resource changes
        with pytest.raises(ValueError, match="At least one resource"):
            resize_cvm_instance("test-id")
            
        # Test invalid vCPU
        with pytest.raises(ValueError, match="Invalid number of vCPUs"):
            resize_cvm_instance("test-id", vcpu=0)
            
        # Test invalid memory
        with pytest.raises(ValueError, match="Invalid memory"):
            resize_cvm_instance("test-id", memory=-1)
            
        # Test invalid disk size
        with pytest.raises(ValueError, match="Invalid disk size"):
            resize_cvm_instance("test-id", disk_size=0)
            
        print("\n=== Resize Validation Tests Passed ===")
        
    except Exception as e:
        pytest.fail(f"Failed to validate resize CVM: {str(e)}")


@pytest.mark.integration
def test_get_cvm_attestation(app_id):
    """Integration test for getting CVM attestation information."""
    try:
        response = get_cvm_attestation_info(app_id)
        
        assert isinstance(response, dict), "Should return a dictionary"
        
        # Check required fields
        assert "is_online" in response, "Should have online status"
        assert "is_public" in response, "Should have public access status"
        assert "error" in response, "Should have error field"
        assert "app_certificates" in response, "Should have certificates"
        
        # Check certificate information if available
        if response["app_certificates"]:
            cert = response["app_certificates"][0]
            assert "subject" in cert, "Certificate should have subject"
            assert "issuer" in cert, "Certificate should have issuer"
            assert "serial_number" in cert, "Certificate should have serial number"
            assert "not_before" in cert, "Certificate should have validity start"
            assert "not_after" in cert, "Certificate should have validity end"
            assert "fingerprint" in cert, "Certificate should have fingerprint"
            assert "signature_algorithm" in cert, "Certificate should have signature algorithm"
            assert "is_ca" in cert, "Certificate should have CA flag"
            assert "position_in_chain" in cert, "Certificate should have chain position"
        
        # Check TCB info if available
        if "tcb_info" in response:
            tcb = response["tcb_info"]
            assert "mrtd" in tcb, "TCB should have MRTD"
            assert "rootfs_hash" in tcb, "TCB should have rootfs hash"
            assert "rtmr0" in tcb, "TCB should have RTMR0"
            assert "rtmr1" in tcb, "TCB should have RTMR1"
            assert "rtmr2" in tcb, "TCB should have RTMR2"
            assert "rtmr3" in tcb, "TCB should have RTMR3"
            assert "event_log" in tcb, "TCB should have event log"
            
            # Check event log entries if available
            if tcb["event_log"]:
                entry = tcb["event_log"][0]
                assert "imr" in entry, "Event log entry should have IMR"
                assert "event_type" in entry, "Event log entry should have event type"
                assert "digest" in entry, "Event log entry should have digest"
                assert "event" in entry, "Event log entry should have event"
                assert "event_payload" in entry, "Event log entry should have payload"
        
        print("\n=== CVM Attestation Information ===")
        print(f"Online Status: {'Online' if response.get('is_online') else 'Offline'}")
        print(f"Public Access: {'Enabled' if response.get('is_public') else 'Disabled'}")
        print(f"Error: {response.get('error') or 'None'}")
        print(f"Certificates: {len(response.get('app_certificates', []))} found")
        
        if response.get('tcb_info'):
            tcb = response['tcb_info']
            print("\nTCB Information:")
            print(f"MRTD: {tcb.get('mrtd')}")
            print(f"Rootfs Hash: {tcb.get('rootfs_hash')}")
            print(f"RTMR0: {tcb.get('rtmr0')}")
            print(f"RTMR1: {tcb.get('rtmr1')}")
            print(f"RTMR2: {tcb.get('rtmr2')}")
            print(f"RTMR3: {tcb.get('rtmr3')}")
            print(f"Event Log Entries: {len(tcb.get('event_log', []))}")
        
        print("=================================")
        
    except Exception as e:
        pytest.fail(f"Failed to get CVM attestation: {str(e)}")

@pytest.mark.integration
def test_get_cvm_attestation_error_handling():
    """Integration test for attestation error handling."""
    try:
        invalid_app_id = "invalid-app-id"
        
        with pytest.raises(Exception, match="Failed to get attestation information"):
            get_cvm_attestation_info(invalid_app_id)
            
        print("\n=== Attestation Error Handling Test Passed ===")
        
    except Exception as e:
        pytest.fail(f"Failed to test attestation error handling: {str(e)}") 
