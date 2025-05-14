"""
Function to create a new Phala Confidential Virtual Machine (CVM).
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from ...api.cvms import create_cvm, get_pubkey_from_cvm
from ...api.teepods import get_teepods
from ...utils.encrypt import encrypt_env_vars
from ...utils.secrets import parse_env

# Default configurations
DEFAULT_VCPU = 2
DEFAULT_MEMORY = 4096  # MB
DEFAULT_DISK_SIZE = 40  # GB
DEFAULT_TEEPOD_ID = "3"
DEFAULT_IMAGE = "dstack-0.3.5"

def create_new_cvm(
    name: str,
    compose_file: str,
    vcpu: int = DEFAULT_VCPU,
    memory: int = DEFAULT_MEMORY,
    disk_size: int = DEFAULT_DISK_SIZE,
    teepod_id: Optional[str] = None,
    image: Optional[str] = None,
    env_file: Optional[str] = None,
    skip_env: bool = False,
    debug: bool = False
) -> Dict[str, Any]:
    """
    Create a new CVM.
    
    Args:
        name: Name of the CVM (3-20 chars, alphanumeric with _ and -)
        compose_file: Path to Docker Compose file
        vcpu: Number of vCPUs
        memory: Memory in MB
        disk_size: Disk size in GB
        teepod_id: TEEPod ID to use (defaults to DEFAULT_TEEPOD_ID)
        image: Version of dstack image to use (defaults to DEFAULT_IMAGE)
        env_file: Path to environment file
        skip_env: Skip environment variable processing
        debug: Enable debug mode
        
    Returns:
        Created CVM details
        
    Raises:
        ValueError: If input validation fails
        FileNotFoundError: If compose file or env file not found
        Exception: For other errors
    """
    try:
        # Validate name
        if not name or not isinstance(name, str):
            raise ValueError("CVM name is required")
        if len(name) > 20:
            raise ValueError("CVM name must be less than 20 characters")
        if len(name) < 3:
            raise ValueError("CVM name must be at least 3 characters")
        if not all(c.isalnum() or c in '_-' for c in name):
            raise ValueError("CVM name must contain only letters, numbers, underscores, and hyphens")

        # Validate compose file
        compose_path = Path(compose_file)
        if not compose_path.exists():
            raise FileNotFoundError(f"Docker Compose file not found: {compose_file}")
        compose_string = compose_path.read_text()

        # Validate resource configurations
        if not isinstance(vcpu, int) or vcpu <= 0:
            raise ValueError(f"Invalid number of vCPUs: {vcpu}")
        if not isinstance(memory, int) or memory <= 0:
            raise ValueError(f"Invalid memory: {memory}")
        if not isinstance(disk_size, int) or disk_size <= 0:
            raise ValueError(f"Invalid disk size: {disk_size}")

        # Get available TEEPods
        teepods = get_teepods()
        if not teepods:
            raise Exception("No TEEPods available")

        # Select TEEPod
        selected_teepod = None
        if teepod_id:
            selected_teepod = next((pod for pod in teepods if pod["teepod_id"] == int(teepod_id)), None)
            if not selected_teepod:
                raise ValueError(f"Failed to find selected TEEPod: {teepod_id}")
        else:
            selected_teepod = next((pod for pod in teepods if pod["teepod_id"] == int(DEFAULT_TEEPOD_ID)), None)
            if not selected_teepod:
                raise Exception("Failed to find default TEEPod")

        # Select image
        selected_image = None
        if image:
            selected_image = next((img for img in selected_teepod.get("images", []) if img["name"] == image), None)
            if not selected_image:
                raise ValueError(f"Failed to find selected image: {image}")
        else:
            selected_image = next((img for img in selected_teepod.get("images", []) if img["name"] == DEFAULT_IMAGE), None)
            if not selected_image:
                raise Exception(f"Failed to find default image {DEFAULT_IMAGE}")

        # Process environment variables
        envs = []
        if env_file:
            try:
                envs = parse_env([], env_file)
            except Exception as e:
                raise Exception(f"Failed to read environment file: {str(e)}")

        # Prepare VM configuration
        vm_config = {
            "teepod_id": selected_teepod["teepod_id"],
            "name": name,
            "image": selected_image["name"],
            "vcpu": vcpu,
            "memory": memory,
            "disk_size": disk_size,
            "compose_manifest": {
                "docker_compose_file": compose_string,
                "docker_config": {
                    "url": "",
                    "username": "",
                    "password": "",
                },
                "features": ["kms", "tproxy-net"],
                "kms_enabled": True,
                "manifest_version": 2,
                "name": name,
                "public_logs": True,
                "public_sysinfo": True,
                "tproxy_enabled": True,
            },
            "listed": False,
        }

        # Get public key from CVM
        pubkey = get_pubkey_from_cvm(vm_config)
        if not pubkey:
            raise Exception("Failed to get public key from CVM")

        # Encrypt environment variables
        encrypted_env = encrypt_env_vars(envs, pubkey["app_env_encrypt_pubkey"])

        if debug:
            print("Public key:", pubkey["app_env_encrypt_pubkey"])
            print("Encrypted environment variables:", encrypted_env)
            print("Environment variables:", json.dumps(envs))

        # Create the CVM
        response = create_cvm({
            **vm_config,
            "encrypted_env": encrypted_env,
            "app_env_encrypt_pubkey": pubkey["app_env_encrypt_pubkey"],
            "app_id_salt": pubkey["app_id_salt"],
        })

        if not response:
            raise Exception("Failed to create CVM")

        return response

    except Exception as e:
        raise Exception(f"Failed to create CVM: {str(e)}") 
