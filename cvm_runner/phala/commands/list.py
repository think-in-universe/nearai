"""
Function to list Phala Confidential Virtual Machines (CVMs).
"""

from typing import List, Dict, Any, Optional
from ..api.cvms import get_cvms

def list_cvms(json_output: bool = False) -> List[Dict[str, Any]]:
    """
    List all CVMs.
    
    Args:
        json_output: If True, returns raw JSON data
        
    Returns:
        List of CVM instances. Each CVM instance contains:
        - name: Name of the CVM
        - status: Current status (running/stopped)
        - hosted: Dictionary containing:
            - app_id: Application ID
            - app_url: Node info URL
            - instance_id: Instance ID
            - image_version: Image version
    """
    try:
        cvms = get_cvms()
        
        if not cvms or len(cvms) == 0:
            return []
        
        if json_output:
            return cvms
            
        return cvms
        
    except Exception as e:
        raise Exception(f"Failed to list CVMs: {str(e)}") 