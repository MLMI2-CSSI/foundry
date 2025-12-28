"""Structured error classes for Foundry.

These errors provide:
1. Error codes for programmatic handling
2. Human-readable messages
3. Recovery hints for agents and users
4. Structured details for debugging

This enables both humans and AI agents to understand and recover from errors.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class FoundryError(Exception):
    """Base error class with structured information for agents and users.

    Attributes:
        code: Machine-readable error code (e.g., "DATASET_NOT_FOUND")
        message: Human-readable error description
        details: Additional context for debugging
        recovery_hint: Actionable suggestion for resolving the error
    """

    code: str
    message: str
    details: Optional[Dict[str, Any]] = field(default=None)
    recovery_hint: Optional[str] = field(default=None)

    def __post_init__(self):
        super().__init__(self.message)

    def __str__(self) -> str:
        parts = [f"[{self.code}] {self.message}"]
        if self.recovery_hint:
            parts.append(f"Hint: {self.recovery_hint}")
        return " ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error to dictionary for JSON responses."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "recovery_hint": self.recovery_hint,
        }


class DatasetNotFoundError(FoundryError):
    """Raised when a dataset cannot be found."""

    def __init__(self, query: str, search_type: str = "query"):
        super().__init__(
            code="DATASET_NOT_FOUND",
            message=f"No dataset found matching {search_type}: '{query}'",
            details={"query": query, "search_type": search_type},
            recovery_hint=(
                "Try a broader search term, check the DOI format, "
                "or use foundry.list() to see available datasets."
            ),
        )


class AuthenticationError(FoundryError):
    """Raised when authentication fails."""

    def __init__(self, service: str, reason: str = None):
        msg = f"Authentication failed for {service}"
        if reason:
            msg += f": {reason}"
        super().__init__(
            code="AUTH_FAILED",
            message=msg,
            details={"service": service, "reason": reason},
            recovery_hint=(
                "Run Foundry(no_browser=False) to re-authenticate, "
                "or check your Globus credentials."
            ),
        )


class DownloadError(FoundryError):
    """Raised when a file download fails."""

    def __init__(self, url: str, reason: str, destination: str = None):
        super().__init__(
            code="DOWNLOAD_FAILED",
            message=f"Failed to download from {url}: {reason}",
            details={"url": url, "reason": reason, "destination": destination},
            recovery_hint=(
                "Check your network connection. "
                "Try use_globus=False for HTTPS fallback, or use_globus=True for Globus transfer."
            ),
        )


class DataLoadError(FoundryError):
    """Raised when loading data from a file fails."""

    def __init__(self, file_path: str, reason: str, data_type: str = None):
        super().__init__(
            code="DATA_LOAD_FAILED",
            message=f"Failed to load data from {file_path}: {reason}",
            details={"file_path": file_path, "reason": reason, "data_type": data_type},
            recovery_hint=(
                "Check that the file exists and is not corrupted. "
                "Try clearing the cache with dataset.clear_dataset_cache()."
            ),
        )


class ValidationError(FoundryError):
    """Raised when metadata validation fails."""

    def __init__(self, field_name: str, error_msg: str, schema_type: str = "metadata"):
        super().__init__(
            code="VALIDATION_FAILED",
            message=f"Validation failed for {schema_type} field '{field_name}': {error_msg}",
            details={"field_name": field_name, "error_msg": error_msg, "schema_type": schema_type},
            recovery_hint=(
                "Check the field value against the expected schema. "
                "See documentation for required metadata format."
            ),
        )


class PublishError(FoundryError):
    """Raised when publishing a dataset fails."""

    def __init__(self, reason: str, source_id: str = None, status: str = None):
        super().__init__(
            code="PUBLISH_FAILED",
            message=f"Failed to publish dataset: {reason}",
            details={"source_id": source_id, "status": status, "reason": reason},
            recovery_hint=(
                "Check your metadata is complete and valid. "
                "Use foundry.check_status(source_id) to monitor publication progress."
            ),
        )


class CacheError(FoundryError):
    """Raised when cache operations fail."""

    def __init__(self, operation: str, reason: str, cache_path: str = None):
        super().__init__(
            code="CACHE_ERROR",
            message=f"Cache {operation} failed: {reason}",
            details={"operation": operation, "reason": reason, "cache_path": cache_path},
            recovery_hint=(
                "Try clearing the cache directory manually, "
                "or check disk space and permissions."
            ),
        )


class ConfigurationError(FoundryError):
    """Raised when Foundry is misconfigured."""

    def __init__(self, setting: str, reason: str, current_value: Any = None):
        super().__init__(
            code="CONFIG_ERROR",
            message=f"Configuration error for '{setting}': {reason}",
            details={"setting": setting, "reason": reason, "current_value": current_value},
            recovery_hint=(
                "Check your Foundry initialization parameters. "
                "See documentation for valid configuration options."
            ),
        )
