"""
Function to get attestation information for a CVM.
"""

from typing import Dict, Any, Optional
from ...api.cvms import get_cvm_attestation
from ...api.types import CvmAttestationResponse

def get_cvm_attestation_info(app_id: str) -> CvmAttestationResponse:
    """
    Get attestation information for a CVM.
    
    Args:
        app_id: App ID of the CVM
        
    Returns:
        Attestation information including certificates and TCB info
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = get_cvm_attestation(app_id)
        if not response:
            raise Exception("Failed to get attestation information")
            
        return response
        
    except Exception as e:
        raise Exception(f"Failed to get attestation information: {str(e)}") 