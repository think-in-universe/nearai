"""
Function to stop a running CVM.
"""

from typing import Dict, Any
from ...api.cvms import stop_cvm

def stop_cvm_instance(app_id: str) -> Dict[str, Any]:
    """
    Stop a running CVM.
    
    Args:
        app_id: App ID of the CVM
        
    Returns:
        Updated CVM details
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = stop_cvm(app_id)
        if not response:
            raise Exception("Failed to stop CVM")
            
        return response
        
    except Exception as e:
        raise Exception(f"Failed to stop CVM: {str(e)}") 