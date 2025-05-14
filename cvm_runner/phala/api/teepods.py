from typing import List, Optional
from dataclasses import dataclass
from .client import api_client
from .constants import API_ENDPOINTS

@dataclass
class Image:
    """Represents a TEEPod image"""
    image_id: int
    name: str
    tag: str
    # Add other image fields as needed

@dataclass
class TEEPod:
    """Represents a TEEPod with its images"""
    teepod_id: int
    name: str
    images: Optional[List[Image]] = None
    # Add other TEEPod fields as needed

async def get_teepods() -> List[TEEPod]:
    """
    Get all TEEPods with their images
    
    Returns:
        List[TEEPod]: List of TEEPods with embedded images
        
    Raises:
        Exception: If the API request fails
    """
    try:
        response = await api_client.get(API_ENDPOINTS.TEEPODS)
        # Parse the response into TEEPod objects
        # Note: You'll need to implement the actual parsing logic based on your API response structure
        return [TEEPod(**pod_data) for pod_data in response.get("nodes", [])]
    except Exception as error:
        raise Exception(f"Failed to get TEEPods: {str(error)}")

async def get_teepod_images(teepod_id: str) -> List[Image]:
    """
    Get images for a TEEPod
    This function is maintained for backwards compatibility.
    Images are now included directly in the TEEPod response.
    
    Args:
        teepod_id (str): TEEPod ID
        
    Returns:
        List[Image]: List of images for the TEEPod
        
    Raises:
        Exception: If the API request fails
    """
    try:
        # First try to get TEEPod with embedded images
        teepods = await get_teepods()
        teepod = next((pod for pod in teepods if pod.teepod_id == int(teepod_id)), None)
        
        # If we found the TEEPod and it has images, return them
        if teepod and teepod.images and len(teepod.images) > 0:
            return teepod.images
        
        # Fallback to the original implementation
        response = await api_client.get(API_ENDPOINTS.TEEPOD_IMAGES(teepod_id))
        # Parse the response into Image objects
        # Note: You'll need to implement the actual parsing logic based on your API response structure
        return [Image(**image_data) for image_data in response]
    except Exception as error:
        raise Exception(f"Failed to get TEEPod images: {str(error)}")
