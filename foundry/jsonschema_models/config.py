from typing import Any, Dict
from pydantic import ConfigDict

def get_model_config(extra: str = 'forbid') -> Dict[str, Any]:
    """
    Get standardized model configuration for Pydantic v2
    
    Args:
        extra: How to handle extra attributes ('allow', 'forbid', or 'ignore')
        
    Returns:
        ConfigDict with standardized settings
    """
    return ConfigDict(
        extra=extra,
        validate_assignment=True,
        frozen=False
    ) 