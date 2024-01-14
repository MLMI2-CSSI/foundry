"""Methods to download files from a Globus endpoint
"""


import os
from collections import deque

import requests
from globus_sdk import TransferClient


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


# TODO (wardlt): Avoid passing dictionaries, as documenting their content is tedious
def download_file(item, https_config, base_directory="data/"):
    """Download a file to disk

    Args:
        item: Dictionary defining the path to the file
        https_config: Configuration defining the URL of the server and the name of the dataset
    """
    print('download_file')
    base_url = https_config.get('base_url', '').rstrip('/')
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

    #url = f"{https_config['base_url']}{item['path']}{item['name']}"
    print(item['path'])
    print(item['name'])
    print(f'Full Path:{full_path}')
    print(f'URL: {url}')

    # build destination path for data file
    destination = os.path.join(base_directory, https_config['source_id'], item['name'])
    parent_path = os.path.split(destination)[0]

    # if parent directories don't exist, create them
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)

    response = requests.get(url)

    # write file to local destination
    with open(destination, "wb") as f:
        f.write(response.content)

    # TODO (wardlt): Should we just return the key?
    return {destination + " status": True}

# def download_file(item, https_config, base_directory="data/", timeout=1800):
#     """
#     Download a file to disk with progress feedback.

#     Args:
#         item (dict): Dictionary defining the path to the file.
#         https_config (dict): Configuration defining the URL of the server and the dataset name.
#         base_directory (str): Base directory for downloads. Default is "data/".
#         timeout (int): Timeout for the HTTPS request in seconds. Default is 30.

#     Returns:
#         str: The path to the downloaded file or None if the download failed.
#     """
#     print(https_config)

#     # Validate https_config and item
#     if 'base_url' not in https_config or 'source_id' not in https_config:
#         print("Error: Missing required keys in https_config")
#         return None
#     if 'path' not in item or 'name' not in item:
#         print("Error: Missing required keys in item")
#         return None

#     url = f"{https_config['base_url']}{item['path']}{item['name']}"
#     destination = os.path.join(base_directory, https_config['source_id'], item['name'])
#     parent_path = os.path.dirname(destination)

#     print(f"URL: {url}  \n Destination: {destination} \n Parent Path: {parent_path}")

#     os.makedirs(parent_path, exist_ok=True)

#     try:
#         with requests.get(url, stream=True, timeout=timeout) as response:
#             response.raise_for_status()

#             # Get the total file size from headers
#             total_size = int(response.headers.get('content-length', 0))
#             downloaded_size = 0

#             with open(destination, "wb") as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)
#                         downloaded_size += len(chunk)
#                         # Calculate and print the download progress
#                         progress = (downloaded_size / total_size) * 100
#                         print(f"\rDownloading... {progress:.2f}%", end="")
#             print("\nDownload complete.")
#             return destination
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading file: {e}")
#     except IOError as e:
#         print(f"Error writing file to disk: {e}")

#     return None

# import os
# import requests

# def download_file(item, https_config, base_directory="data/", timeout=30):
#     """
#     Download a file to disk with improved path handling.

#     Args:
#         item (dict): Dictionary defining the path to the file.
#         https_config (dict): Configuration defining the URL of the server and the dataset name.
#         base_directory (str): Base directory for downloads. Default is "data/".
#         timeout (int): Timeout for the HTTPS request in seconds. Default is 30.

#     Returns:
#         str: The path to the downloaded file or None if the download failed.
#     """
#     # Validate https_config and item
#     if 'base_url' not in https_config or 'source_id' not in https_config:
#         print("Error: Missing required keys in https_config")
#         return None
#     if 'path' not in item or 'name' not in item:
#         print("Error: Missing required keys in item")
#         return None

#     print(https_config)
#     print(item)
#     # Normalize URL and destination paths
#     base_url = https_config['base_url'].rstrip('/')  # Remove trailing slash if present
#     file_path = item['path'].strip('/')  # Remove leading/trailing slashes
#     file_name = item['name']

#     # Avoid duplication between file_path and file_name
#     if file_path.endswith(file_name):
#         file_name = ''  # If file_name is part of file_path, set file_name to empty


#     print(file_path)

#     url = f"{base_url}/{file_path}/{file_name}"
#     destination = os.path.join(base_directory, https_config['source_id'], file_path, file_name)
#     parent_path = os.path.dirname(destination)
#     print(f"URL: {url}  \n Destination: {destination} \n Parent Path: {parent_path}")


#     os.makedirs(parent_path, exist_ok=True)

#     try:
#         with requests.get(url, stream=True, timeout=timeout) as response:
#             response.raise_for_status()

#             total_size = int(response.headers.get('content-length', 0))
#             downloaded_size = 0

#             with open(destination, "wb") as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)
#                         downloaded_size += len(chunk)
#                         progress = (downloaded_size / total_size) * 100
#                         print(f"\rDownloading... {progress:.2f}%", end="")
#             print("\nDownload complete.")
#             return destination
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading file: {e}")
#     except IOError as e:
#         print(f"Error writing file to disk: {e}")

#     return None
