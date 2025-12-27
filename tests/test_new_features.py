"""Tests for new features: as_json, include_schema, get_schema, MCP tools."""

import pytest
from unittest import mock

from foundry import Foundry, FoundryDataset
from tests.test_data import datacite_data, valid_metadata


class TestAsJsonParameter:
    """Tests for the as_json parameter on search and list."""

    def test_dataset_to_dict_method(self):
        """Test that _dataset_to_dict converts a dataset to dict properly."""
        # Create a mock dataset
        mock_ds = mock.Mock()
        mock_ds.dataset_name = "test_dataset"
        mock_ds.dc.titles = [mock.Mock(title="Test Dataset")]
        mock_ds.dc.identifier = mock.Mock()
        mock_ds.dc.identifier.identifier = "10.18126/test"
        mock_ds.dc.descriptions = [mock.Mock(description="A test dataset")]
        mock_ds.dc.publicationYear = 2024
        mock_ds.foundry_schema.keys = []
        mock_ds.foundry_schema.splits = []
        mock_ds.foundry_schema.data_type = "tabular"

        # Test the _dataset_to_dict method directly
        from foundry.foundry import Foundry
        result = Foundry._dataset_to_dict(None, mock_ds)

        assert isinstance(result, dict)
        assert result["name"] == "test_dataset"
        assert result["title"] == "Test Dataset"
        assert result["doi"] == "10.18126/test"
        assert result["data_type"] == "tabular"

    def test_dataset_to_dict_includes_fields_and_splits(self):
        """Test that _dataset_to_dict includes fields and splits."""
        mock_key = mock.Mock()
        mock_key.key = ["band_gap"]

        mock_split = mock.Mock()
        mock_split.label = "train"

        mock_ds = mock.Mock()
        mock_ds.dataset_name = "test_dataset"
        mock_ds.dc.titles = [mock.Mock(title="Test")]
        mock_ds.dc.identifier = mock.Mock()
        mock_ds.dc.identifier.identifier = "10.18126/test"
        mock_ds.dc.descriptions = []
        mock_ds.dc.publicationYear = 2024
        mock_ds.foundry_schema.keys = [mock_key]
        mock_ds.foundry_schema.splits = [mock_split]
        mock_ds.foundry_schema.data_type = "tabular"

        from foundry.foundry import Foundry
        result = Foundry._dataset_to_dict(None, mock_ds)

        assert result["fields"] == ["band_gap"]
        assert result["splits"] == ["train"]
        assert result["data_type"] == "tabular"


class TestGetSchema:
    """Tests for the get_schema method on FoundryDataset."""

    def test_get_schema_returns_dict(self):
        """Test that get_schema returns a dictionary with expected fields."""
        ds = FoundryDataset(
            dataset_name='test_dataset',
            foundry_schema=valid_metadata,
            datacite_entry=datacite_data
        )

        schema = ds.get_schema()

        assert isinstance(schema, dict)
        assert schema["name"] == "test_dataset"
        assert "title" in schema
        assert "doi" in schema
        assert "data_type" in schema
        assert "splits" in schema
        assert "fields" in schema

    def test_get_schema_includes_field_details(self):
        """Test that get_schema includes field descriptions and units."""
        ds = FoundryDataset(
            dataset_name='test_dataset',
            foundry_schema=valid_metadata,
            datacite_entry=datacite_data
        )

        schema = ds.get_schema()

        # Check that fields have the expected structure
        assert len(schema["fields"]) > 0
        field = schema["fields"][0]
        assert "name" in field
        assert "role" in field
        assert "description" in field
        assert "units" in field

    def test_get_schema_includes_splits(self):
        """Test that get_schema includes split information."""
        ds = FoundryDataset(
            dataset_name='test_dataset',
            foundry_schema=valid_metadata,
            datacite_entry=datacite_data
        )

        schema = ds.get_schema()

        assert len(schema["splits"]) == 2  # train and test from valid_metadata
        split_names = [s["name"] for s in schema["splits"]]
        assert "train" in split_names
        assert "test" in split_names


class TestIncludeSchema:
    """Tests for the include_schema parameter on get_as_dict."""

    def test_include_schema_false_returns_data_only(self):
        """Test that include_schema=False returns just data."""
        ds = FoundryDataset(
            dataset_name='test_dataset',
            foundry_schema=valid_metadata,
            datacite_entry=datacite_data
        )
        ds._foundry_cache = mock.Mock()
        ds._foundry_cache.load_as_dict.return_value = {"train": ({"x": [1, 2]}, {"y": [0, 1]})}

        result = ds.get_as_dict(include_schema=False)

        assert "schema" not in result
        assert "train" in result

    def test_include_schema_true_returns_data_and_schema(self):
        """Test that include_schema=True returns data with schema."""
        ds = FoundryDataset(
            dataset_name='test_dataset',
            foundry_schema=valid_metadata,
            datacite_entry=datacite_data
        )
        ds._foundry_cache = mock.Mock()
        ds._foundry_cache.load_as_dict.return_value = {"train": ({"x": [1, 2]}, {"y": [0, 1]})}

        result = ds.get_as_dict(include_schema=True)

        assert "data" in result
        assert "schema" in result
        assert result["schema"]["name"] == "test_dataset"


class TestMCPTools:
    """Tests for MCP server tools."""

    def test_search_datasets_tool(self):
        """Test the search_datasets MCP tool."""
        from foundry.mcp.server import TOOLS

        search_tool = next(t for t in TOOLS if t["name"] == "search_datasets")

        assert search_tool["name"] == "search_datasets"
        assert "query" in search_tool["inputSchema"]["properties"]
        assert "limit" in search_tool["inputSchema"]["properties"]
        assert "query" in search_tool["inputSchema"]["required"]

    def test_get_dataset_schema_tool(self):
        """Test the get_dataset_schema MCP tool."""
        from foundry.mcp.server import TOOLS

        schema_tool = next(t for t in TOOLS if t["name"] == "get_dataset_schema")

        assert schema_tool["name"] == "get_dataset_schema"
        assert "doi" in schema_tool["inputSchema"]["properties"]
        assert "doi" in schema_tool["inputSchema"]["required"]

    def test_load_dataset_tool(self):
        """Test the load_dataset MCP tool."""
        from foundry.mcp.server import TOOLS

        load_tool = next(t for t in TOOLS if t["name"] == "load_dataset")

        assert load_tool["name"] == "load_dataset"
        assert "doi" in load_tool["inputSchema"]["properties"]
        assert "split" in load_tool["inputSchema"]["properties"]

    def test_list_all_datasets_tool(self):
        """Test the list_all_datasets MCP tool."""
        from foundry.mcp.server import TOOLS

        list_tool = next(t for t in TOOLS if t["name"] == "list_all_datasets")

        assert list_tool["name"] == "list_all_datasets"
        assert "limit" in list_tool["inputSchema"]["properties"]

    def test_create_server(self):
        """Test that create_server returns proper server config."""
        from foundry.mcp.server import create_server

        config = create_server()

        assert config["name"] == "foundry-ml"
        assert "version" in config
        assert "tools" in config
        assert len(config["tools"]) == 4


class TestCLI:
    """Tests for CLI commands."""

    def test_cli_app_exists(self):
        """Test that CLI app is properly configured."""
        from foundry.__main__ import app

        assert app is not None
        assert app.info.name == "foundry"

    def test_cli_has_search_command(self):
        """Test that CLI has search command."""
        from foundry.__main__ import search
        assert search is not None
        assert callable(search)

    def test_cli_has_get_command(self):
        """Test that CLI has get command."""
        from foundry.__main__ import get
        assert get is not None
        assert callable(get)

    def test_cli_has_schema_command(self):
        """Test that CLI has schema command."""
        from foundry.__main__ import schema
        assert schema is not None
        assert callable(schema)

    def test_cli_has_catalog_command(self):
        """Test that CLI has catalog command."""
        from foundry.__main__ import catalog
        assert catalog is not None
        assert callable(catalog)

    def test_cli_has_push_to_hf_command(self):
        """Test that CLI has push_to_hf command."""
        from foundry.__main__ import push_to_hf
        assert push_to_hf is not None
        assert callable(push_to_hf)

    def test_cli_has_version_command(self):
        """Test that CLI has version command."""
        from foundry.__main__ import version
        assert version is not None
        assert callable(version)

    def test_cli_has_mcp_start_command(self):
        """Test that CLI has MCP start command."""
        from foundry.__main__ import start
        assert start is not None
        assert callable(start)

    def test_cli_has_mcp_install_command(self):
        """Test that CLI has MCP install command."""
        from foundry.__main__ import install
        assert install is not None
        assert callable(install)
