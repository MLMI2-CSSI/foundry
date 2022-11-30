"""
https_upload.py

Private utility methods to upload files and/or folders to Globus using HTTPS instead of Globus Transfer.

Authors:
    Aristana Scourtas

Last modified 8/22/22 by Aristana Scourtas
"""

import logging
import os
import requests
from typing import Any, Tuple, Dict, List
from uuid import uuid4

from globus_sdk import AuthClient, TransferAPIError


logger = logging.getLogger(__name__)


def _upload_to_endpoint(self, local_data_path: str, endpoint_id: str = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                        dest_parent: str = None, dest_child: str = None) -> Tuple[str, str]:
    """Upload local data to a Globus endpoint using HTTPS PUT requests. Data can be a folder or an individual file.
        Note that the ACL rule created in this method must later be deleted after the dataset is submitted to MDF.
    Args:
        local_data_path (str): Path to the local dataset to publish to Foundry via HTTPS. Creates an HTTPS PUT
            request to upload the data specified to a Globus endpoint (default is NCSA endpoint) before it is
            transferred to MDF.
        endpoint_id (str): Globus endpoint ID to upload the data to. Default is NCSA endpoint.

    Returns
    -------
    (str) Globus data source URL: URL pointing to the data on the Globus endpoint
    (str) rule_id: Globus ACL rule ID for the uploaded data. Used to delete the rule after the dataset is submitted
        to MDF.
    """
    # define upload destination
    dest_path = self._create_dest_folder(endpoint_id, parent_dir=dest_parent, child_dir=dest_child)
    # create new ACL rule (ie permission) for user to read/write to endpoint and path
    rule_id = self._create_access_rule(endpoint_id, dest_path)
    # upload data to endpoint
    globus_data_source = self._https_upload(local_data_path=local_data_path, dest_path=dest_path,
                                            endpoint_id=endpoint_id)
    return globus_data_source, rule_id


def _create_dest_folder(self, endpoint_id: str, parent_dir: str = None, child_dir: str = None) -> str:
    """Create a destination folder for the data on a Globus endpoint
    Args:
        endpoint_id (str): A UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK.
        parent_dir (str): Set to '/tmp' when default is None. The parent directory that all publications via HTTPS
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
        self.transfer_client.operation_mkdir(endpoint_id=endpoint_id, path=dest_path)
    except TransferAPIError as e:
        raise IOError(f"Error from Globus API while creating destination folder: {e.message}") from e
    return dest_path


def _create_access_rule(self, endpoint_id: str, dest_path: str) -> str:
    """Create an ACL rule (ie permission) for the user to read/write to the given destination on a Globus endpoint
    Args:
        endpoint_id (str): A UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK.
        dest_path (str): The path to the existing folder on the given Globus endpoint.
    Returns
    -------
        (str): The ID for the ACL rule (necessary to delete it in the future)
    """
    # get user info
    res = self.auth_client.oauth2_userinfo()
    user_id = res.data["sub"]  # get the user primary ID (based on primary email set in Globus)
    # create data blob needed to set new rule with Globus
    rule_data = {
        "DATA_TYPE": "access",
        "principal_type": "identity",
        "principal": user_id,
        "path": dest_path,
        "permissions": "rw",
    }
    # create new ACL rule (eg permission) for user to read/write to endpoint and path
    rule_id = None
    try:
        ret = self.transfer_client.add_endpoint_acl_rule(endpoint_id, rule_data)
        rule_id = ret["access_id"]  # rule_id is needed to delete the rule later
    except TransferAPIError as e:
        logger.error(e.message)  # NOTE: known issue where user can still write to endpoint if this fails
    return rule_id


def _https_upload(self, local_data_path: str, dest_path: str = "/tmp",
                  endpoint_id: str = "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec") -> str:
    """Upload a dataset via HTTPS to a Globus endpoint
    Args:
        local_data_path (str): The path to the local data to upload. Can be relative or absolute.
        dest_path (str): The path to the destination folder on the Globus endpoint. Default is "/tmp".
        endpoint_id (str): A UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK. Default is the NCSA UUID '82f1b5c6-6e9b-11e5-ba47-22000b92c6ec'.
    Returns
    -------
        (str): Globus data source URL (ie the URL that points to the data on a Globus endpoint)
    """
    # get URL for Globus endpoint location
    endpoint = self.transfer_client.get_endpoint(endpoint_id)  # gets info for NCSA endpoint
    https_base_url = endpoint['https_server']

    # Submit data (folders of files or an independent file) to be written to endpoint
    if os.path.isdir(local_data_path):
        self._upload_folder(local_data_path, https_base_url, dest_path, endpoint_id)
    elif os.path.isfile(local_data_path):
        self._upload_file(local_data_path, https_base_url, dest_path, endpoint_id)
    else:
        raise IOError(f"Data path '{local_data_path}' is of unknown type")

    # return the data source URL for publication to MDF
    return self.make_globus_link(endpoint_id, dest_path)


def _upload_folder(self, local_data_path: str, https_base_url: str, parent_dest_path: str, endpoint_id: str) \
        -> List[Dict[str, Any]]:
    """Upload a folder to a Globus endpoint using HTTPS
    Args:
        local_data_path (str): The path to the local data to upload. Can be relative or absolute.
        https_base_url (str): The URL for a given Globus endpoint.
        parent_dest_path (str): The path to the parent folder to be written to on the given endpoint. The contents
            of 'local_data_path' will be written here, including subdirectories.
        endpoint_id (str): The UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK. This must be the same endpoint pointed to by the https_base_url.
    Returns
    -------
        (list): A list of all the HTTPS PUT request results (dicts) from the uploads
    """
    results = []
    # initialize destination path as the parent destination path
    dest_path = parent_dest_path

    # walk through each child directory in the designated local data folder
    for root, directories, files in os.walk(local_data_path):
        # update destination path if we have walked into a child directory
        if root != local_data_path:
            # get the child directory relative path
            subpath = os.path.relpath(root, local_data_path)
            # update destination path to include child directories (ie subpaths)
            dest_path = os.path.join(parent_dest_path, subpath)
            # create child directories on endpoint
            try:
                self.transfer_client.operation_mkdir(endpoint_id=endpoint_id, path=dest_path)
            except TransferAPIError as e:
                raise IOError(f"Error while creating child directory {dest_path}: {e.message}") from e
        # get local path to file to upload
        for filename in files:
            filepath = os.path.join(root, filename)
            # upload file to destination path on endpoint
            result = self._upload_file(filepath, https_base_url, dest_path, endpoint_id)
            results.append(result)
    return results


def _upload_file(self, filepath: str, https_base_url: str, dest_path: str, endpoint_id: str) -> Dict[str, Any]:
    """Upload an individual file to a Globus endpoint using HTTPS PUT
    Args:
        filepath (str): The path to the local file to upload.
        https_base_url (str): The URL for a given Globus endpoint.
        dest_path (str): The path to the folder to be written to on the given endpoint.
        endpoint_id (str): The UUID designating the exact Globus endpoint. Can be obtained via the Globus Web UI or
            the SDK. This must be the same endpoint pointed to by the https_base_url.
    Returns
    -------
        (dict): The HTTPS response dict from a PUT request
    """
    # lets you HTTPS to specific endpoint (NCSA endpoint by default)
    scope = f"https://auth.globus.org/scopes/{endpoint_id}/https"
    # Get the authorization header token (string for the headers dict) HTTPS upload
    auth_gcs = AuthClient(authorizer=self.auths[scope])
    header = auth_gcs.authorizer.get_authorization_header()

    # get Globus endpoint path to write to
    filename = os.path.split(filepath)[1]
    # need to strip out leading "/" in dest_path for join to work
    endpoint_dest = os.path.join(https_base_url, dest_path.lstrip("/"), filename)

    # upload via HTTPS as arbitrary binary content type
    with open(filepath, 'rb') as f:
        reply = requests.put(
            endpoint_dest,
            data=f,
            headers={"Authorization": header, "Content-Type": "application/octet-stream"}
        )
    if reply.status_code != 200:
        raise IOError(f"Error on HTTPS PUT, got response {reply.status_code}: {reply.text}")
    # Return the response
    return reply
