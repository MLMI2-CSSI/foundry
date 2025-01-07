from importlib import import_module
from typing import Optional, Any

def optional_import(module_name: str, package_name: Optional[str] = None) -> Any:
    """
    Attempt to import an optional module.
    
    Args:
        module_name: Name of the module to import
        package_name: Name of the package for error message (if different from module_name)
        
    Returns:
        The imported module if successful, None otherwise
    """
    try:
        return import_module(module_name)
    except ImportError:
        return None

def require_package(package_name: str, feature_name: str):
    """Raise informative error when an optional package is required but not installed"""
    raise ImportError(
        f"{feature_name} requires {package_name}. "
        f"Install with: pip install foundry_ml[{package_name}] "
        f"or pip install {package_name}"
    ) 