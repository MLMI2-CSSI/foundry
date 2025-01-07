import re
from typing import Optional

def is_doi(identifier: str) -> bool:
    """Check if a string is a DOI"""
    doi_pattern = r'10.\d{4,9}/[-._;()/:\w]+'
    return bool(re.match(doi_pattern, identifier))

def is_pandas_pytable(h5_group) -> bool:
    """Check if an HDF5 group is a pandas PyTable"""
    return hasattr(h5_group, '_v_attrs') and 'pandas_type' in h5_group._v_attrs 