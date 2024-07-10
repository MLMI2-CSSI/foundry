# exceptions.py

class FoundryError(Exception):
    """Base exception class for Foundry-related errors."""
    pass


class DatasetNotFoundError(FoundryError):
    """Raised when a dataset is not found."""
    pass


class AuthenticationError(FoundryError):
    """Raised when there's an authentication issue."""
    pass


class InvalidQueryError(FoundryError):
    """Raised when an invalid query is provided."""
    pass
