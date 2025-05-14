"""
Function to restart a CVM.
"""

from typing import Dict, Any
from ...api.cvms import restart_cvm

def restart_cvm_instance(app_id: str) -> Dict[str, Any]:
    """
    Restart a CVM.
    
    Args:
        app_id: App ID of the CVM
        
    Returns:
        Updated CVM details
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = restart_cvm(app_id)
        if not response:
            raise Exception("Failed to restart CVM")
            
        return response
        
    except Exception as e:
        raise Exception(f"Failed to restart CVM: {str(e)}") 