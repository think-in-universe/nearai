from typing import Dict, List, Optional, Any
import logging
from .client import api_client
from .constants import API_ENDPOINTS
from .types import (
    CvmInstance,
    GetCvmByAppIdResponse,
    GetPubkeyFromCvmResponse,
    PostCvmResponse,
    UpgradeCvmResponse,
    CvmAttestationResponse,
    GetCvmNetworkResponse,
    VMConfig,
    UpdateCvmPayload,
    ResizeCvmPayload
)

logger = logging.getLogger(__name__)

def get_cvms() -> List[CvmInstance]:
    """
    Get all CVMs for the current user
    
    Returns:
        List[CvmInstance]: List of CVMs
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.get(API_ENDPOINTS.CVMS(0))
        return [CvmInstance(**cvm) for cvm in response]
    except Exception as error:
        raise Exception(f"Failed to get CVMs: {str(error)}")

def check_cvm_exists(app_id: str) -> str:
    """
    Check CVM exists for the current user and appId
    
    Args:
        app_id (str): App ID
        
    Returns:
        str: CVM appId string
        
    Raises:
        SystemExit: If CVM is not found
    """
    cvms = get_cvms()
    cvm = next(
        (cvm for cvm in cvms if 
         (cvm.hosted and cvm.hosted.get('app_id') == app_id) or 
         (cvm.hosted and f"app_{cvm.hosted.get('app_id')}" == app_id)),
        None
    )
    
    if not cvm:
        logger.error(f"CVM with App ID app_{app_id} not detected")
        raise SystemExit(1)
    else:
        logger.info(f"CVM with App ID app_{app_id} detected")
        return cvm.hosted.get('app_id', '') if cvm.hosted else ''

def get_cvm_by_app_id(app_id: str) -> GetCvmByAppIdResponse:
    """
    Get a CVM by App ID
    
    Args:
        app_id (str): App ID
        
    Returns:
        GetCvmByAppIdResponse: CVM details
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.get(API_ENDPOINTS.CVM_BY_APP_ID(app_id))
        return GetCvmByAppIdResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to get CVM by App ID: {str(error)}")

def get_pubkey_from_cvm(vm_config: VMConfig) -> GetPubkeyFromCvmResponse:
    """
    Get public key from CVM
    
    Args:
        vm_config (VMConfig): VM configuration
        
    Returns:
        GetPubkeyFromCvmResponse: Public key
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.post(API_ENDPOINTS.CVM_PUBKEY, vm_config)
        return GetPubkeyFromCvmResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to get pubkey from CVM: {str(error)}")

def get_cvm_network(app_id: str) -> GetCvmNetworkResponse:
    """
    Get network information for a CVM
    
    Args:
        app_id (str): App ID
        
    Returns:
        GetCvmNetworkResponse: Network information
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.get(API_ENDPOINTS.CVM_NETWORK(app_id))
        return GetCvmNetworkResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to get network information for CVM: {str(error)}")

def create_cvm(vm_config: VMConfig) -> PostCvmResponse:
    """
    Create a new CVM
    
    Args:
        vm_config (VMConfig): VM configuration
        
    Returns:
        PostCvmResponse: Created CVM details
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.post(API_ENDPOINTS.CVM_FROM_CONFIGURATION, vm_config)
        return PostCvmResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to create CVM: {str(error)}")

def start_cvm(app_id: str) -> PostCvmResponse:
    """
    Start a CVM
    
    Args:
        app_id (str): App ID
        
    Returns:
        PostCvmResponse: Success status
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.post(API_ENDPOINTS.CVM_START(app_id))
        return PostCvmResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to start CVM: {str(error)}")

def stop_cvm(app_id: str) -> PostCvmResponse:
    """
    Stop a CVM
    
    Args:
        app_id (str): App ID
        
    Returns:
        PostCvmResponse: Success status
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.post(API_ENDPOINTS.CVM_STOP(app_id))
        return PostCvmResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to stop CVM: {str(error)}")

def restart_cvm(app_id: str) -> PostCvmResponse:
    """
    Restart a CVM
    
    Args:
        app_id (str): App ID
        
    Returns:
        PostCvmResponse: Success status
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.post(API_ENDPOINTS.CVM_RESTART(app_id))
        return PostCvmResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to restart CVM: {str(error)}")

def upgrade_cvm(app_id: str, vm_config: VMConfig) -> UpgradeCvmResponse:
    """
    Upgrade a CVM
    
    Args:
        app_id (str): App ID
        vm_config (VMConfig): VM configuration
        
    Returns:
        UpgradeCvmResponse: Upgrade response
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.put(API_ENDPOINTS.CVM_UPGRADE(app_id), vm_config)
        return UpgradeCvmResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to upgrade CVM: {str(error)}")

def delete_cvm(app_id: str) -> bool:
    """
    Delete a CVM
    
    Args:
        app_id (str): App ID
        
    Returns:
        bool: Success status
        
    Raises:
        Exception: If the API request fails
    """
    try:
        api_client.delete(API_ENDPOINTS.CVM_BY_APP_ID(app_id))
        return True
    except Exception as error:
        raise Exception(f"Failed to delete CVM: {str(error)}")

def update_cvm(update_payload: UpdateCvmPayload) -> Any:
    """
    Update a CVM
    
    Args:
        update_payload (UpdateCvmPayload): Update payload
        
    Returns:
        Any: Updated CVM details
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.put(API_ENDPOINTS.CVM_BY_APP_ID(update_payload['app_id']), update_payload)
        return response
    except Exception as error:
        raise Exception(f"Failed to update CVM: {str(error)}")

def get_cvm_attestation(app_id: str) -> CvmAttestationResponse:
    """
    Get CVM attestation
    
    Args:
        app_id (str): App ID
        
    Returns:
        CvmAttestationResponse: Attestation response
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = api_client.get(API_ENDPOINTS.CVM_ATTESTATION(app_id))
        return CvmAttestationResponse(**response)
    except Exception as error:
        raise Exception(f"Failed to get CVM attestation: {str(error)}")

def resize_cvm(
    app_id: str,
    vcpu: Optional[int] = None,
    memory: Optional[int] = None,
    disk_size: Optional[int] = None,
    allow_restart: Optional[int] = None
) -> bool:
    """
    Resize a CVM
    
    Args:
        app_id (str): App ID
        vcpu (Optional[int]): Number of vCPUs
        memory (Optional[int]): Memory size in MB
        disk_size (Optional[int]): Disk size in GB
        allow_restart (Optional[int]): Whether to allow restart
        
    Returns:
        bool: Success status
        
    Raises:
        Exception: If the API request fails
    """
    try:
        payload: ResizeCvmPayload = {}
        if vcpu is not None:
            payload['vcpu'] = vcpu
        if memory is not None:
            payload['memory'] = memory
        if disk_size is not None:
            payload['disk_size'] = disk_size
        if allow_restart is not None:
            payload['allow_restart'] = allow_restart
            
        api_client.patch(API_ENDPOINTS.CVM_RESIZE(app_id), payload)
        return True
    except Exception as error:
        raise Exception(f"Failed to resize CVM: {str(error)}") 