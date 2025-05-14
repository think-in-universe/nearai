"""
Function to resize a CVM's resources.
"""

from typing import Dict, Any, Optional
from ...api.cvms import resize_cvm

def resize_cvm_instance(
    app_id: str,
    vcpu: Optional[int] = None,
    memory: Optional[int] = None,
    disk_size: Optional[int] = None
) -> Dict[str, Any]:
    """
    Resize a CVM's resources.
    
    Args:
        app_id: App ID of the CVM
        vcpu: New number of vCPUs (optional)
        memory: New memory in MB (optional)
        disk_size: New disk size in GB (optional)
        
    Returns:
        Updated CVM details
        
    Raises:
        ValueError: If no resource changes are specified
        Exception: If the API request fails
    """
    try:
        # Validate that at least one resource is being changed
        if vcpu is None and memory is None and disk_size is None:
            raise ValueError("At least one resource (vcpu, memory, or disk_size) must be specified")
            
        # Validate resource values if provided
        if vcpu is not None and (not isinstance(vcpu, int) or vcpu <= 0):
            raise ValueError(f"Invalid number of vCPUs: {vcpu}")
        if memory is not None and (not isinstance(memory, int) or memory <= 0):
            raise ValueError(f"Invalid memory: {memory}")
        if disk_size is not None and (not isinstance(disk_size, int) or disk_size <= 0):
            raise ValueError(f"Invalid disk size: {disk_size}")
            
        response = resize_cvm(app_id, vcpu, memory, disk_size)
        if not response:
            raise Exception("Failed to resize CVM")
            
        return response
        
    except Exception as e:
        raise Exception(f"Failed to resize CVM: {str(e)}") 