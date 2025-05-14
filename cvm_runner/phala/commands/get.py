"""
Function to get details of a specific Phala Confidential Virtual Machine (CVM).
"""

from typing import Dict, Any
from ..api.cvms import get_cvm_by_app_id

def get_cvm(app_id: str, json_output: bool = False) -> Dict[str, Any]:
    """
    Get details of a specific CVM by app ID.
    
    Args:
        app_id: The app ID of the CVM
        json_output: If True, returns raw JSON data
        
    Returns:
        CVM details including:
        - id: CVM ID
        - name: Name of the CVM
        - status: Current status (running/stopped)
        - app_id: Application ID
        - vm_uuid: VM UUID
        - instance_id: Instance ID
        - vcpu: Number of vCPUs
        - memory: Memory size in MB
        - disk_size: Disk size in GB
        - base_image: Base image name
        - encrypted_env_pubkey: Public key for encrypted environment
        - dapp_dashboard_url: Dashboard URL
        - syslog_endpoint: System log endpoint
    """
    try:
        cvm = get_cvm_by_app_id(app_id)
        
        if json_output:
            return cvm
            
        return cvm
        
    except Exception as e:
        raise Exception(f"Failed to get CVM: {str(e)}") 