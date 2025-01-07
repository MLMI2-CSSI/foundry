from .io import _read_csv, _read_json, _read_excel
from .validation import is_doi, is_pandas_pytable
from importlib import import_module
from typing import Optional, Any

def optional_import(module_name: str, package_name: Optional[str] = None) -> Any:
    """Attempt to import an optional module"""
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

__all__ = [
    'optional_import',
    'require_package',
    '_read_csv',
    '_read_json',
    '_read_excel',
    'is_doi',
    'is_pandas_pytable'
] 