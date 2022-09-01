import urllib3
import json
import time
import os
import multiprocessing
import requests
from collections import deque
from joblib import Parallel, delayed


def recursive_ls(tc, ep, path, max_depth=3):
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


def download_file(item, https_config):
    url = f"{https_config['base_url']}{item['path']}{item['name']}"

    # build destination path for data file
    destination = os.path.join("data/", https_config['source_id'], item['name'])

    parent_path = os.path.split(destination)[0]

    # if parent directories don't exist, create them
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)

    response = requests.get(url)

    # write file to local destination
    with open(destination, "wb") as f:
        f.write(response.content)

    return {destination + " status": True}


# NOTE: deprecated with deprecation of Xtract Aug 2022; saved for posterity
# TODO: reassess if there's a better way than passing self in
def xtract_https_download(foundryObj, verbose=False, **kwargs):
    source_id = foundryObj.mdf["source_id"]
    xtract_base_url = kwargs.get("xtract_base_url")
    # MDF Materials Data at NCSA
    source_ep_id = kwargs.get("source_ep_id")
    folder_to_crawl = kwargs.get("folder_to_crawl")

    # This only matters if you want files grouped together.
    grouper = kwargs.get("grouper")

    auth_token = foundryObj.xtract_tokens["auth_token"]
    transfer_token = foundryObj.xtract_tokens["transfer_token"]
    funcx_token = foundryObj.xtract_tokens["funcx_token"]

    headers = {
        "Authorization": auth_token,
        "Transfer": transfer_token,
        "FuncX": funcx_token,
        "Petrel": auth_token,
    }
    if verbose:
        print(f"Headers: {headers}")

    # Initialize the crawl. This kicks off the Globus EP crawling service on the backend.
    crawl_url = f"{xtract_base_url}/crawl"
    if verbose:
        print(f"Crawl URL is : {crawl_url}")

    first_ep_dict = {
        "repo_type": "GLOBUS",
        "eid": source_ep_id,
        "dir_paths": [folder_to_crawl],
        "grouper": grouper,
    }
    tokens = {"Transfer": transfer_token, "FuncX": funcx_token, "Authorization": auth_token}
    crawl_req = requests.post(
        f"{xtract_base_url}/crawl",
        json={"endpoints": [first_ep_dict], "tokens": tokens},
    )

    if verbose:
        print("Crawl response:", crawl_req)
    crawl_id = json.loads(crawl_req.content)["crawl_id"]
    if verbose:
        print(f"Crawl ID: {crawl_id}")

    # Wait for the crawl to finish before we can start fetching our metadata.
    while True:
        crawl_status = requests.get(
            f"{xtract_base_url}/get_crawl_status", json={"crawl_id": crawl_id}
        )
        if verbose:
            print(crawl_status)
        crawl_content = json.loads(crawl_status.content)
        if verbose:
            print(f"Crawl Status: {crawl_content}")

        if crawl_content["crawl_status"] == "complete":
            files_crawled = crawl_content["files_crawled"]
            if verbose:
                print("Our crawl has succeeded!")
            break
        else:
            if verbose:
                print("Sleeping before re-polling...")
            time.sleep(2)

    # Now we fetch our metadata. Here you can configure n to be maximum number of
    # messages you want at once.

    file_ls = []
    fetched_files = 0
    while fetched_files < files_crawled:
        fetch_mdata = requests.get(
            f"{xtract_base_url}/fetch_crawl_mdata",
            json={"crawl_id": crawl_id, "n": 2},
        )
        fetch_content = json.loads(fetch_mdata.content)

        for file_path in fetch_content["file_ls"]:
            file_ls.append(file_path)
            fetched_files += 1

        if fetch_content["queue_empty"]:
            if verbose:
                print("Queue is empty! Continuing...")
            time.sleep(2)

    source_path = os.path.join(
        foundryObj.config.local_cache_dir, foundryObj.mdf["source_id"]
    )

    if not os.path.exists(foundryObj.config.local_cache_dir):
        os.mkdir(foundryObj.config.local_cache_dir)
        os.mkdir(source_path)

    elif not os.path.exists(source_path):
        os.mkdir(source_path)

    num_cores = multiprocessing.cpu_count()

    @delayed
    def download_file(file):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        url = "https://data.materialsdatafacility.org" + file["path"]

        # removes data source (eg MDF) parent directories, leaving the split path only
        datasplit_subpath = file["path"].split(source_id + "/")[-1]

        # build destination path for data file
        destination = os.path.join("data/", source_id, datasplit_subpath)

        parent_path = os.path.split(destination)[0]

        # if parent directories don't exist, create them
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        response = requests.get(url, verify=False)

        # write file to local destination
        with open(destination, "wb") as f:
            f.write(response.content)

        return {file["path"] + " status": True}

    results = Parallel(n_jobs=num_cores)(
        download_file(file) for file in file_ls
    )

    print("Done curling.")
    print(results)
