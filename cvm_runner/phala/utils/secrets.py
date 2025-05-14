"""
Utility functions for handling environment variables and secrets.
"""

from typing import List, Dict, Any
import os
from pathlib import Path

def parse_env(env_vars: List[str], env_file: str) -> List[Dict[str, str]]:
    """
    Parse environment variables from a file and command line arguments.
    
    Args:
        env_vars: List of environment variables in KEY=VALUE format
        env_file: Path to environment file
        
    Returns:
        List of dictionaries with 'key' and 'value' fields
        
    Raises:
        FileNotFoundError: If env_file doesn't exist
        ValueError: If env var format is invalid
    """
    result = []
    
    # Parse environment file
    if env_file:
        env_path = Path(env_file)
        if not env_path.exists():
            raise FileNotFoundError(f"Environment file not found: {env_file}")
            
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        key, value = line.split('=', 1)
                        result.append({
                            'key': key.strip(),
                            'value': value.strip()
                        })
                    except ValueError:
                        raise ValueError(f"Invalid environment variable format in file: {line}")
    
    # Parse command line environment variables
    for env_var in env_vars:
        try:
            key, value = env_var.split('=', 1)
            result.append({
                'key': key.strip(),
                'value': value.strip()
            })
        except ValueError:
            raise ValueError(f"Invalid environment variable format: {env_var}")
    
    return result
