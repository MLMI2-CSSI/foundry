"""Methods to download files from a Globus endpoint
"""


import logging
import os
from collections import deque

import requests
from globus_sdk import TransferClient


logger = logging.getLogger(__name__)


def recursive_ls(tc: TransferClient, ep: str, path: str, max_depth: int = 3):
    """Find all files in a Globus directory recursively

    Args:
        tc: TransferClient authorized to access the directory
        ep: Endpoint on which the files reside
        path: Path to the files being downloaded
        max_depth: Maximum recurse depth

    Yields:
        Dictionaries describing the location of the files. Each includes at least
            "name": Name of the file
            "path": Absolute path to the file's location
    """
    queue = deque()
    queue.append((path, "", 0))
    yield from _get_files(tc, ep, queue, max_depth)


def _get_files(tc, ep, queue, max_depth):
    while queue:
        abs_path, rel_path, depth = queue.pop()
        path_prefix = rel_path + "/" if rel_path else ""

        res = tc.operation_ls(ep, path=abs_path)

        if depth < max_depth:
            queue.extend(
                (
                    res["path"] + item["name"],
                    path_prefix + item["name"],
                    depth + 1,
                )
                for item in res["DATA"]
                if item["type"] == "dir"
            )
        for item in res["DATA"]:
            if item["type"] == 'file':
                item["name"] = path_prefix + item["name"]
                item["path"] = abs_path.replace('/~/', '/')
                yield item


class DownloadError(Exception):
    """Raised when a file download fails."""

    def __init__(self, url: str, reason: str, destination: str = None):
        self.url = url
        self.reason = reason
        self.destination = destination
        super().__init__(f"Failed to download {url}: {reason}")


def download_file(item, base_directory, https_config, timeout=1800):
    """Download a file to disk

    Args:
        item: Dictionary defining the path to the file
        base_directory: Base directory for storing downloaded files
        https_config: Configuration defining the URL of the server and the name of the dataset
        timeout: Timeout for the download request in seconds (default: 1800)

    Returns:
        str: Path to the downloaded file

    Raises:
        DownloadError: If the download fails for any reason
    """
    base_url = https_config['base_url'].rstrip('/')
    path = item.get('path', '').strip('/')

    # Extracting the name and subdirectory from the item
    name = item.get('name', '')
    subdirectory = name.split('/')[0] if '/' in name else ''

    # Avoid duplication of subdirectory in path
    if subdirectory and path.endswith(subdirectory):
        full_path = f"{path}/{name.split('/', 1)[-1]}".strip('/')
    else:
        full_path = '/'.join([path, name]).strip('/')

    url = f"{base_url}/{full_path}"

    # build destination path for data file
    destination = os.path.join(base_directory, https_config['source_id'], item['name'])
    parent_path = os.path.split(destination)[0]

    # if parent directories don't exist, create them
    if not os.path.exists(parent_path):
        os.makedirs(parent_path, exist_ok=True)

    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            response.raise_for_status()

            downloaded_size = 0
            logger.info(f"Starting download: {url}")

            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

            logger.info(f"Downloaded {downloaded_size / (1 << 20):,.2f} MB to {destination}")
            return destination

    except requests.exceptions.RequestException as e:
        raise DownloadError(url, str(e), destination) from e
    except IOError as e:
        raise DownloadError(url, f"Failed to write to disk: {e}", destination) from e
