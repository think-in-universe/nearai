"""
Utility functions for encrypting environment variables.
"""

from typing import List, Dict, Any
import json
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
import os

def hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes."""
    hex_str = hex_str[2:] if hex_str.startswith("0x") else hex_str
    return bytes.fromhex(hex_str)

def bytes_to_hex(data: bytes) -> str:
    """Convert bytes to hex string."""
    return data.hex()  # Remove the 0x prefix

def encrypt_env_vars(env_vars: List[Dict[str, str]], public_key_hex: str) -> str:
    """
    Encrypt environment variables using the provided public key.
    
    Args:
        env_vars: List of dictionaries with 'key' and 'value' fields
        public_key_hex: Hex encoded public key
        
    Returns:
        Hex encoded encrypted environment variables
        
    Raises:
        ValueError: If public key is invalid
    """
    try:
        # Prepare environment data
        envs_json = json.dumps({"env": env_vars})
        
        # Generate private key and derive public key
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Generate shared key
        remote_pubkey = hex_to_bytes(public_key_hex)
        shared_key = private_key.exchange(x25519.X25519PublicKey.from_public_bytes(remote_pubkey))
        
        # Create AES-GCM cipher
        cipher = AESGCM(shared_key)
        
        # Generate random IV
        iv = os.urandom(12)
        
        # Encrypt the data
        encrypted = cipher.encrypt(iv, envs_json.encode(), None)
        
        # Combine all components
        result = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ) + iv + encrypted
        
        # Return hex encoded result
        return bytes_to_hex(result)
        
    except Exception as e:
        raise ValueError(f"Failed to encrypt environment variables: {str(e)}") 
