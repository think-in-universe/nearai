"""
Function to delete a CVM.
"""

from typing import Dict, Any
from ...api.cvms import delete_cvm

def delete_cvm_instance(app_id: str) -> Dict[str, Any]:
    """
    Delete a CVM.
    
    Args:
        app_id: App ID of the CVM
        
    Returns:
        Response from the delete operation
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = delete_cvm(app_id)
        if not response:
            raise Exception("Failed to delete CVM")
            
        return response
        
    except Exception as e:
        raise Exception(f"Failed to delete CVM: {str(e)}") 