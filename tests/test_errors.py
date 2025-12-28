"""Tests for the structured error classes."""

import pytest

from foundry.errors import (
    FoundryError,
    DatasetNotFoundError,
    AuthenticationError,
    DownloadError,
    DataLoadError,
    ValidationError,
    PublishError,
    CacheError,
    ConfigurationError,
)


class TestFoundryError:
    """Tests for the base FoundryError class."""

    def test_foundry_error_has_required_fields(self):
        """Test that FoundryError has all required fields."""
        error = FoundryError(
            code="TEST_ERROR",
            message="Test error message",
            details={"key": "value"},
            recovery_hint="Try again"
        )

        assert error.code == "TEST_ERROR"
        assert error.message == "Test error message"
        assert error.details == {"key": "value"}
        assert error.recovery_hint == "Try again"

    def test_foundry_error_str_includes_code_and_hint(self):
        """Test that str() includes code and recovery hint."""
        error = FoundryError(
            code="TEST_ERROR",
            message="Test message",
            recovery_hint="Do this to fix"
        )

        error_str = str(error)
        assert "[TEST_ERROR]" in error_str
        assert "Test message" in error_str
        assert "Do this to fix" in error_str

    def test_foundry_error_to_dict(self):
        """Test serialization to dict for JSON responses."""
        error = FoundryError(
            code="TEST_ERROR",
            message="Test message",
            details={"foo": "bar"},
            recovery_hint="Fix it"
        )

        d = error.to_dict()
        assert d["code"] == "TEST_ERROR"
        assert d["message"] == "Test message"
        assert d["details"] == {"foo": "bar"}
        assert d["recovery_hint"] == "Fix it"

    def test_foundry_error_is_exception(self):
        """Test that FoundryError can be raised and caught."""
        with pytest.raises(FoundryError) as exc_info:
            raise FoundryError(code="TEST", message="Test")

        assert exc_info.value.code == "TEST"


class TestDatasetNotFoundError:
    """Tests for DatasetNotFoundError."""

    def test_dataset_not_found_error(self):
        """Test DatasetNotFoundError initialization."""
        error = DatasetNotFoundError("bandgap")

        assert error.code == "DATASET_NOT_FOUND"
        assert "bandgap" in error.message
        assert error.details["query"] == "bandgap"
        assert error.recovery_hint is not None

    def test_dataset_not_found_error_search_type(self):
        """Test DatasetNotFoundError with different search types."""
        error = DatasetNotFoundError("10.18126/abc", search_type="DOI")

        assert "DOI" in error.message
        assert error.details["search_type"] == "DOI"


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_authentication_error(self):
        """Test AuthenticationError initialization."""
        error = AuthenticationError("Globus", "Token expired")

        assert error.code == "AUTH_FAILED"
        assert "Globus" in error.message
        assert "Token expired" in error.message
        assert error.details["service"] == "Globus"
        assert error.recovery_hint is not None


class TestDownloadError:
    """Tests for DownloadError."""

    def test_download_error(self):
        """Test DownloadError initialization."""
        error = DownloadError(
            url="https://example.com/file.dat",
            reason="Connection timeout",
            destination="/tmp/file.dat"
        )

        assert error.code == "DOWNLOAD_FAILED"
        assert "https://example.com/file.dat" in error.message
        assert error.details["url"] == "https://example.com/file.dat"
        assert error.details["destination"] == "/tmp/file.dat"


class TestDataLoadError:
    """Tests for DataLoadError."""

    def test_data_load_error(self):
        """Test DataLoadError initialization."""
        error = DataLoadError(
            file_path="/data/dataset.json",
            reason="Invalid JSON",
            data_type="tabular"
        )

        assert error.code == "DATA_LOAD_FAILED"
        assert "/data/dataset.json" in error.message
        assert error.details["data_type"] == "tabular"


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error(self):
        """Test ValidationError initialization."""
        error = ValidationError(
            field_name="creators",
            error_msg="Field required",
            schema_type="datacite"
        )

        assert error.code == "VALIDATION_FAILED"
        assert "creators" in error.message
        assert error.details["schema_type"] == "datacite"


class TestPublishError:
    """Tests for PublishError."""

    def test_publish_error(self):
        """Test PublishError initialization."""
        error = PublishError(
            reason="Metadata validation failed",
            source_id="my_dataset_v1.0",
            status="failed"
        )

        assert error.code == "PUBLISH_FAILED"
        assert error.details["source_id"] == "my_dataset_v1.0"
        assert error.details["status"] == "failed"


class TestCacheError:
    """Tests for CacheError."""

    def test_cache_error(self):
        """Test CacheError initialization."""
        error = CacheError(
            operation="write",
            reason="Disk full",
            cache_path="/tmp/cache"
        )

        assert error.code == "CACHE_ERROR"
        assert "write" in error.message
        assert error.details["cache_path"] == "/tmp/cache"


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error(self):
        """Test ConfigurationError initialization."""
        error = ConfigurationError(
            setting="use_globus",
            reason="Invalid value",
            current_value="maybe"
        )

        assert error.code == "CONFIG_ERROR"
        assert "use_globus" in error.message
        assert error.details["current_value"] == "maybe"
