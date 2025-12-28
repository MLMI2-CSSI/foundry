"""Tests for https_download module."""

import os
import pytest
from unittest import mock

import requests

from foundry.https_download import download_file, DownloadError


class TestDownloadFile:
    """Tests for the download_file function."""

    def test_download_file_success(self, tmp_path):
        """Test successful file download."""
        item = {
            "path": "/data",
            "name": "example_file.txt"
        }
        https_config = {
            "base_url": "https://example.com/",
            "source_id": "test_dataset"
        }

        # Mock successful response
        mock_response = mock.Mock()
        mock_response.iter_content = mock.Mock(return_value=[b"Example file content"])
        mock_response.raise_for_status = mock.Mock()
        mock_response.__enter__ = mock.Mock(return_value=mock_response)
        mock_response.__exit__ = mock.Mock(return_value=False)

        with mock.patch.object(requests, "get", return_value=mock_response):
            result = download_file(item, str(tmp_path), https_config)

        # Assert file was downloaded
        expected_path = tmp_path / "test_dataset" / "example_file.txt"
        assert os.path.exists(expected_path)
        assert result == str(expected_path)

    def test_download_file_request_error(self, tmp_path):
        """Test that RequestException raises DownloadError."""
        item = {
            "path": "/data",
            "name": "example_file.txt"
        }
        https_config = {
            "base_url": "https://example.com/",
            "source_id": "test_dataset"
        }

        # Mock request failure
        with mock.patch.object(requests, "get", side_effect=requests.exceptions.RequestException("Connection failed")):
            with pytest.raises(DownloadError) as exc_info:
                download_file(item, str(tmp_path), https_config)

        error = exc_info.value
        assert error.url == "https://example.com/data/example_file.txt"
        assert "Connection failed" in error.reason
        assert error.destination is not None

    def test_download_file_io_error(self, tmp_path):
        """Test that IOError raises DownloadError."""
        item = {
            "path": "/data",
            "name": "example_file.txt"
        }
        https_config = {
            "base_url": "https://example.com/",
            "source_id": "test_dataset"
        }

        # Mock successful response but write failure
        mock_response = mock.Mock()
        mock_response.iter_content = mock.Mock(return_value=[b"data"])
        mock_response.raise_for_status = mock.Mock()
        mock_response.__enter__ = mock.Mock(return_value=mock_response)
        mock_response.__exit__ = mock.Mock(return_value=False)

        with mock.patch.object(requests, "get", return_value=mock_response):
            with mock.patch("builtins.open", side_effect=IOError("Disk full")):
                with pytest.raises(DownloadError) as exc_info:
                    download_file(item, str(tmp_path), https_config)

        error = exc_info.value
        assert "Disk full" in error.reason

    def test_download_error_has_structured_info(self):
        """Test that DownloadError provides structured information."""
        error = DownloadError(
            url="https://example.com/file.txt",
            reason="Connection timeout",
            destination="/tmp/file.txt"
        )

        assert error.url == "https://example.com/file.txt"
        assert error.reason == "Connection timeout"
        assert error.destination == "/tmp/file.txt"
        assert "Connection timeout" in str(error)
