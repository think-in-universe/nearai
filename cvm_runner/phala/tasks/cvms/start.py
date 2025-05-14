"""
Function to start a stopped CVM.
"""

from typing import Dict, Any
from ...api.cvms import start_cvm

def start_cvm_instance(app_id: str) -> Dict[str, Any]:
    """
    Start a stopped CVM.
    
    Args:
        app_id: App ID of the CVM
        
    Returns:
        Updated CVM details
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = start_cvm(app_id)
        if not response:
            raise Exception("Failed to start CVM")
            
        return response
        
    except Exception as e:
        raise Exception(f"Failed to start CVM: {str(e)}") 