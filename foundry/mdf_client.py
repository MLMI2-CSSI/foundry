"""Minimal MDF client replacing mdf_forge dependency.

This provides the essential functionality needed by Foundry without
requiring the full mdf_forge package.

Also includes staging upload functionality for publishing local data to MDF
without requiring Globus Connect Personal.
"""

import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# MDF Public Staging Endpoint (NCSA)
STAGING_ENDPOINT_ID = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec"
STAGING_BASE_PATH = "/tmp"
TRANSFER_API_BASE = "https://transfer.api.globus.org/v0.10"

# Globus Search Index IDs
MDF_INDEX_ID = "1a57bbe5-5272-477f-9d31-343b8258b7a5"
MDF_TEST_INDEX_ID = "aeccc263-f083-45f5-ab1d-08ee702b3384"


class StagingUploader:
    """Handles uploading files to MDF staging endpoint.

    This allows users to publish local data to MDF without needing
    Globus Connect Personal running. Files are uploaded via HTTPS
    to a temporary staging location on the MDF public endpoint.

    Usage:
        uploader = StagingUploader(transfer_token)
        unique_id, remote_dir = uploader.create_staging_directory()
        uploader.upload_file(Path("data.csv"), remote_dir)
        # Then use globus://{STAGING_ENDPOINT_ID}{remote_dir}/ as data source
    """

    def __init__(self, transfer_token: str, https_token: Optional[str] = None):
        """Initialize uploader with Globus tokens.

        Args:
            transfer_token: Globus OAuth2 access token with transfer scope
            https_token: Globus OAuth2 access token with HTTPS scope for NCSA
                        (if None, uses transfer_token)
        """
        self.transfer_token = transfer_token
        self.https_token = https_token or transfer_token
        self.endpoint_id = STAGING_ENDPOINT_ID
        self.headers = {
            "Authorization": f"Bearer {transfer_token}",
            "Content-Type": "application/json",
        }
        self._https_server = None

    def _get_https_server(self) -> str:
        """Get the HTTPS server URL for the endpoint."""
        if self._https_server:
            return self._https_server

        # Query the endpoint to get its HTTPS server
        response = requests.get(
            f"{TRANSFER_API_BASE}/endpoint/{self.endpoint_id}",
            headers=self.headers,
        )

        if response.ok:
            data = response.json()
            self._https_server = data.get("https_server")
            if self._https_server:
                return self._https_server

        # Fallback: Use the standard NCSA HTTPS endpoint
        self._https_server = "https://g-b0c3f4.dd271.03c0.data.globus.org"
        return self._https_server

    def create_staging_directory(self) -> tuple[str, str]:
        """Create a unique directory on the staging endpoint.

        Returns:
            Tuple of (unique_id, full_path) for the created directory
        """
        unique_id = str(uuid.uuid4())
        dir_path = f"{STAGING_BASE_PATH}/{unique_id}"

        response = requests.post(
            f"{TRANSFER_API_BASE}/endpoint/{self.endpoint_id}/mkdir",
            headers=self.headers,
            json={
                "path": dir_path,
                "DATA_TYPE": "mkdir",
            },
        )

        if not response.ok:
            error_data = response.json()
            raise RuntimeError(
                f"Failed to create staging directory: {error_data.get('message', response.text)}"
            )

        return unique_id, dir_path

    def upload_file(self, local_path: Path, remote_dir: str, filename: Optional[str] = None) -> str:
        """Upload a single file to the staging endpoint via HTTPS.

        Args:
            local_path: Path to local file
            remote_dir: Remote directory path (e.g., /tmp/uuid)
            filename: Optional remote filename (defaults to local filename)

        Returns:
            Remote path to uploaded file
        """
        if filename is None:
            filename = local_path.name

        remote_path = f"{remote_dir}/{filename}"

        https_server = self._get_https_server()
        upload_url = f"{https_server}{remote_path}"

        with open(local_path, "rb") as f:
            response = requests.put(
                upload_url,
                headers={"Authorization": f"Bearer {self.https_token}"},
                data=f,
            )

        if not response.ok:
            raise RuntimeError(
                f"Failed to upload {local_path.name}: {response.status_code} {response.text}"
            )

        return remote_path

    def upload_directory(
        self,
        local_dir: Path,
        remote_dir: str,
        progress_callback=None,
    ) -> List[str]:
        """Upload all files from a local directory.

        Args:
            local_dir: Local directory containing files to upload
            remote_dir: Remote directory path
            progress_callback: Optional callback(filename, current, total)

        Returns:
            List of remote paths to uploaded files
        """
        files = list(local_dir.iterdir())
        files = [f for f in files if f.is_file()]
        uploaded = []

        for i, file_path in enumerate(files):
            if progress_callback:
                progress_callback(file_path.name, i + 1, len(files))

            remote_path = self.upload_file(file_path, remote_dir)
            uploaded.append(remote_path)

        return uploaded

    def get_globus_url(self, remote_dir: str) -> str:
        """Get the Globus file manager URL for a staged directory.

        This is the format expected by MDF Connect for data sources.

        Args:
            remote_dir: Remote directory path (e.g., /tmp/uuid)

        Returns:
            Globus file manager URL for use with MDF
        """
        from urllib.parse import quote
        encoded_path = quote(f"{remote_dir}/", safe="")
        return f"https://app.globus.org/file-manager?origin_id={self.endpoint_id}&origin_path={encoded_path}"


class MDFClient:
    """Minimal MDF client for dataset search and download."""

    def __init__(
        self,
        index: str = "mdf",
        services: Optional[Any] = None,
        search_client: Optional[Any] = None,
        transfer_client: Optional[Any] = None,
        data_mdf_authorizer: Optional[Any] = None,
        petrel_authorizer: Optional[Any] = None,
    ):
        """Initialize the MDF client."""
        self.index = index
        self.search_client = search_client
        self.transfer_client = transfer_client
        self.data_mdf_authorizer = data_mdf_authorizer
        self.petrel_authorizer = petrel_authorizer
        self._reset_query_state()

    def _reset_query_state(self):
        """Reset all query filters to their default state."""
        self._resource_types: List[str] = []
        self._organizations: List[str] = []
        self._source_names: List[str] = []
        self._dois: List[str] = []

    @property
    def _has_field_filters(self) -> bool:
        """Check if any field-specific filters are set.

        Field filters require advanced query mode in Globus Search
        for exact matching.
        """
        return bool(
            self._dois or
            self._source_names
        )

    def match_resource_types(self, resource_type: str) -> "MDFClient":
        """Filter by resource type."""
        self._resource_types = [resource_type]
        return self

    def match_organizations(self, organization: str) -> "MDFClient":
        """Filter by organization."""
        self._organizations = [organization]
        return self

    def match_source_names(self, source_name: str) -> "MDFClient":
        """Filter by source name or source ID.

        Args:
            source_name: The source_name or source_id of the dataset.
                If a source_id is provided (e.g., 'dataset_v1.1'),
                the version suffix is stripped automatically.
        """
        import re
        # Strip version suffix if present (e.g., _v1.1, _v2.0)
        match = re.search(r"_v[0-9]+\.[0-9]+$", source_name)
        if match:
            source_name = source_name[:match.start()]
        self._source_names = [source_name]
        return self

    def match_dois(self, doi: str) -> "MDFClient":
        """Filter by DOI."""
        self._dois = [doi]
        return self

    def search(
        self,
        q: Optional[str] = None,
        advanced: bool = False,
        limit: int = 10,
        **kwargs,
    ) -> List[Dict]:
        """Search for datasets.

        Args:
            q: Free-text search query
            advanced: Force advanced query mode. Automatically enabled
                when field-specific filters (DOI, source_name) are used.
            limit: Maximum number of results to return

        Returns:
            List of dataset metadata dictionaries
        """
        if self.search_client is None:
            raise RuntimeError("Search client not configured")

        # Use advanced mode for field-specific filters (exact matching)
        use_advanced = advanced or self._has_field_filters

        try:
            query_parts = []
            if q:
                query_parts.append(q)
            for rt in self._resource_types:
                query_parts.append(f'mdf.resource_type:"{rt}"')
            for org in self._organizations:
                query_parts.append(f'mdf.organizations:"{org}"')
            for source_name in self._source_names:
                query_parts.append(f'mdf.source_name:"{source_name}"')
            for doi in self._dois:
                query_parts.append(f'dc.identifier.identifier:"{doi}"')

            full_query = " AND ".join(query_parts) if query_parts else "*"
            index_id = MDF_INDEX_ID if self.index == "mdf" else MDF_TEST_INDEX_ID

            results = self.search_client.search(
                index_id, full_query, limit=limit, advanced=use_advanced
            )

            # Extract content from Globus Search response structure
            # Structure: gmeta[].entries[].content
            contents = []
            for gmeta_entry in results.get("gmeta", []):
                for entry in gmeta_entry.get("entries", []):
                    if "content" in entry:
                        contents.append(entry["content"])
            return contents
        finally:
            self._reset_query_state()

    def globus_download(
        self,
        results: List[Dict],
        dest: str = ".",
        dest_ep: Optional[str] = None,
        download_datasets: bool = True,
        **kwargs,
    ) -> Dict:
        """Download data using Globus Transfer."""
        if self.transfer_client is None:
            raise RuntimeError("Transfer client not configured")

        transfer_items = []
        for result in results:
            if "data" in result:
                data = result["data"]
                if "endpoint_path" in data:
                    transfer_items.append({
                        "source_endpoint": data.get("endpoint_id"),
                        "source_path": data["endpoint_path"],
                        "destination_path": dest,
                    })

        if not transfer_items:
            return {"status": "no_data", "message": "No transferable data found"}

        return {"status": "pending", "items": transfer_items}
