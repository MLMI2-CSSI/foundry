"""Private utility methods to upload files and/or folders to Globus using HTTPS instead of Globus Transfer.
"""

import logging
import os
import urllib
from requests import put, Response
from typing import Any, Tuple, Dict, List
from uuid import uuid4

from globus_sdk import AuthClient, TransferClient, TransferAPIError

from .auth import PubAuths


logger = logging.getLogger(__name__)


def upload_to_endpoint(auths: PubAuths, local_data_path: str, endpoint_id: str = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                       dest_parent: str = None, dest_child: str = None) -> Tuple[str, str]:
    """Upload local data to a Globus endpoint using HTTPS PUT requests. Data can be a folder or an individual file.
    Args:
        auths (PubAuths): Dataclass of authorizers needed for upload. Includes `transfer_client`, `auth_client_openid`,
            and `endpoint_auth_clients`, which is a Dict of `endpoint_id`:AuthClient mappings.
        local_data_path (str): Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT
            request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is
            transferred to MDF.
        endpoint_id (str): Globus endpoint ID to upload the data to. Default is NCSA endpoint. Must match the
            `endpoint_id` auth'd in `auths.auth_client_gcs`.

    Returns
    -------
    (str) Globus data source URL: URL pointing to the data on the Globus endpoint
    """
    # define upload destination
    dest_path = _create_dest_folder(auths.transfer_client, endpoint_id, parent_dir=dest_parent, child_dir=dest_child)
    # upload data to endpoint
    globus_data_source = _https_upload(auths.transfer_client, auths.endpoint_auth_clients, local_data_path=local_data_path,
                                       dest_path=dest_path, endpoint_id=endpoint_id)
    return globus_data_source


def _create_dest_folder(transfer_client: TransferClient, endpoint_id: str, parent_dir: str = None,
                        child_dir: str = None) -> str:
    """Create a destination folder for the data on a Globus endpoint
    Args:
        transfer_client (TransferClient): Globus client authorized for Globus Transfers (ie moving data on endpoint,
            adding/removing folders, etc).
        endpoint_id (str): A UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK.
        parent_dir (str): Set to "/tmp" when default is None. The parent directory that all publications via HTTPS
            will be written to.
        child_dir (str): Set to a random UUID when default is None. The child directory that the data will be
            written to.
    Returns
    -------
        (str): Path on Globus endpoint to write to
    """
    # use a random UUID for each dataset publication, unless specified otherwise
    if child_dir is None:
        child_dir = uuid4()  # the publication ID forms the name of the child directory
    if parent_dir is None:
        parent_dir = "/tmp"
    dest_path = os.path.join(parent_dir, str(child_dir))  # NOTE: must start and end with "/"

    try:
        transfer_client.operation_mkdir(endpoint_id=endpoint_id, path=dest_path)
    except TransferAPIError as e:
        raise IOError(f"Error from Globus API while creating destination folder: {e.message}") from e
    return dest_path


def _https_upload(transfer_client: TransferClient, endpoint_auth_clients: Dict[str, AuthClient], local_data_path: str,
                  dest_path: str = "/tmp", endpoint_id: str = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec") -> str:
    """Upload a dataset via HTTPS to a Globus endpoint
    Args:
        transfer_client (TransferClient): Globus client authorized for Globus Transfers (ie moving data on endpoint,
            adding/removing folders, etc).
        endpoint_auth_clients (Dict[str, AuthClient]): Dict of `endpoint_id` : `AuthClient` keypairs. AuthClients used
            for Globus Auth functionality within endpoint-specific scopes using Globus Connect Server (ie accessing
            or altering data on a specific endpoint).
        local_data_path (str): The path to the local data to upload. Can be relative or absolute.
        dest_path (str): The path to the destination folder on the Globus endpoint. Default is "/tmp".
        endpoint_id (str): A UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK. Default is the NCSA UUID "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec".
    Returns
    -------
        (str): Globus data source URL (ie the URL that points to the data on a Globus endpoint)
    """

    # get URL for Globus endpoint location
    endpoint = transfer_client.get_endpoint(endpoint_id)  # gets info for NCSA endpoint
    https_base_url = endpoint["https_server"]

    # Submit data (folders of files or an independent file) to be written to endpoint
    if os.path.isdir(local_data_path):
        _upload_folder(transfer_client, endpoint_auth_clients, local_data_path, https_base_url, dest_path, endpoint_id)
    elif os.path.isfile(local_data_path):
        _upload_file(endpoint_auth_clients[endpoint_id], local_data_path, https_base_url, dest_path)
    else:
        raise IOError(f"Data path '{local_data_path}' is of unknown type")

    # return the data source URL for publication to MDF
    return _make_globus_link(endpoint_id, dest_path)


def _upload_folder(transfer_client: TransferClient, endpoint_auth_clients: Dict[str, AuthClient], local_data_path: str,
                   https_base_url: str, parent_dest_path: str, endpoint_id: str) -> List[Dict[str, Any]]:
    """Upload a folder to a Globus endpoint using HTTPS
    Args:
        transfer_client (TransferClient): Globus client authorized for Globus Transfers (ie moving data on endpoint,
            adding/removing folders, etc).
        endpoint_auth_clients (Dict[str, AuthClient]): Dict of `endpoint_id` : `AuthClient` keypairs. AuthClients used
            for Globus Auth functionality within endpoint-specific scopes using Globus Connect Server (ie accessing
            or altering data on a specific endpoint).
        local_data_path (str): The path to the local data to upload. Can be relative or absolute.
        https_base_url (str): The URL for a given Globus endpoint.
        parent_dest_path (str): The path to the parent folder to be written to on the given endpoint. The contents
            of "local_data_path" will be written here, including subdirectories.
        endpoint_id (str): The UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK. This must be the same endpoint pointed to by the https_base_url.
    Returns
    -------
        (list): A list of Response objects (the `requests` HTTPS response object from a PUT request)
    """
    results = []
    # initialize destination path as the parent destination path
    dest_path = parent_dest_path

    # walk through each child directory in the designated local data folder
    for root, _, files in os.walk(local_data_path):
        # update destination path if we have walked into a child directory
        if root != local_data_path:
            # get the child directory relative path
            subpath = os.path.relpath(root, local_data_path)
            # update destination path to include child directories (ie subpaths)
            dest_path = os.path.join(parent_dest_path, subpath)
            # create child directories on endpoint
            try:
                transfer_client.operation_mkdir(endpoint_id=endpoint_id, path=dest_path)
            except TransferAPIError as e:
                raise IOError(f"Error while creating child directory {dest_path}: {e.message}") from e
        # get local path to file to upload
        for filename in files:
            filepath = os.path.join(root, filename)
            # upload file to destination path on endpoint
            result = _upload_file(endpoint_auth_clients[endpoint_id], filepath, https_base_url, dest_path)
            results.append(result)
    return results


def _upload_file(auth_client_gcs: AuthClient, filepath: str, https_base_url: str, dest_path: str) -> Response:
    """Upload an individual file to a Globus endpoint specified in 'auth_client_gcs' using HTTPS PUT
    Args:
        auth_client_gcs (AuthClient): Globus client authorized for Globus Auth functionality within an endpoint-specific
            scope using Globus Connect Server (ie accessing or altering data on a specific endpoint).
        filepath (str): The path to the local file to upload.
        https_base_url (str): The URL for a given Globus endpoint.
        dest_path (str): The path to the folder to be written to on the given endpoint.
    Returns
    -------
        (Response): The `requests` HTTPS response object from a PUT request
    """
    # Get the authorization header token (string for the headers dict) for HTTPS upload
    header = auth_client_gcs.authorizer.get_authorization_header()

    # get Globus endpoint path to write to
    filename = os.path.split(filepath)[1]
    # need to strip out leading "/" in dest_path for join to work
    endpoint_dest = os.path.join(https_base_url, dest_path.lstrip("/"), filename)

    # upload via HTTPS as arbitrary binary content type
    with open(filepath, "rb") as f:
        reply = put(
            endpoint_dest,
            data=f,
            headers={"Authorization": header, "Content-Type": "application/octet-stream"}
        )
    if reply.status_code != 200:
        raise IOError(f"Error on HTTPS PUT, got response {reply.status_code}: {reply.text}")
    # Return the response
    return reply


def _make_globus_link(endpoint_id: str, path: str) -> str:
    """Create the Globus data source URL for a given datapath on an endpoint
    Args:
        endpoint_id (str): The UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK.
        path (str): The path to the dataset folder on the given endpoint.
    Returns
    -------
        (str): The Globus data source URL (ie the URL that points to the data on a Globus endpoint)
    """
    # make sure the path has the "/"s encoded properly for a URL
    safe_path = urllib.parse.quote(path, safe="*")
    link = f"https://app.globus.org/file-manager?origin_id={endpoint_id}&origin_path={safe_path}"
    return link
