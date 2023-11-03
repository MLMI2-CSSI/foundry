import logging
import os

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm

from foundry.foundry_dataset import FoundryDataset
from foundry.https_download import recursive_ls, download_file

logger = logging.getLogger(__name__)


class FoundryCache():
    """The FoundryCache manages the local storage of FoundryDataset objects"""

    def __init__(self):

        self.local_cache_dir = os.environ.get("FOUNDRY_LOCAL_CACHE_DIR", "./data")

    def download_to_cache(self, dataset: FoundryDataset, globus: bool = True, interval: int = 20, parallel_https: int = 4, verbose: bool = False):
        # TODO: Adapt to living in the FoundryCache (originated from Foundry object)
        """Downloads the data from source to local storage

        Args:
            globus: if True, use Globus to download the data else try HTTPS
            interval: How often to wait before checking Globus transfer status
            parallel_https: Number of files to download in parallel if using HTTPS
            verbose: Produce more debug messages to screen

        """
        # Check if the dir already exists

        if not self.dataset_present(dataset):

            # query for mdf data representation
            res = self.forge_client.search(
                f"mdf.source_id:{dataset.source_id}", advanced=True
            )

            # download with globus
            if globus:
                self.forge_client.globus_download(
                    res,
                    dest=self.local_cache_dir,
                    # dest_ep=self.destination_endpoint, # never actually used anywhere I can find? -SW
                    interval=interval,
                    download_datasets=True,
                )

            # download via http
            else:
                self.download_via_http(self, dataset, parallel_https, verbose)

        self.validate_local_storage(self.local_cache_dir, dataset)

        return self

    def validate_local_storage(self, dataset: FoundryDataset):
        # TODO: fix path creation - I don't think 'dataset['name']' is a valid reference
        path = self.local_cache_dir + dataset['name']

        # after download check making sure directory exists, contains all indicated files
        if os.path.isdir(path):
            # checking all necessary files are present
            if dataset.splits:
                missing_files = []
                for split in dataset.splits:
                    if split.path[0] == '/':  # if absolute path, make it a relative path
                        split.path = split.path[1:]
                    if not os.path.isfile(os.path.join(path, split.path)):
                        # keeping track of all files not downloaded
                        missing_files.append(split.path)
                if len(missing_files) > 0:
                    raise FileNotFoundError(f"Downloaded directory does not contain the following files: {missing_files}")

            else:
                if len(os.listdir(path)) < 1:
                    raise FileNotFoundError("Downloaded directory does not contain the expected file")
        else:
            raise NotADirectoryError("Unable to create directory to download data")

    def download_via_http(self, dataset: FoundryDataset, parallel_https: int, verbose: bool):
        https_config = {
            "source_ep_id": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
            "base_url": "https://data.materialsdatafacility.org",
            "folder_to_crawl": f"/foundry/{dataset.source_id}/",
            "source_id": dataset.source_id
        }

        # Begin finding files to download
        task_generator = recursive_ls(self.transfer_client,
                                      https_config['source_ep_id'],
                                      https_config['folder_to_crawl'])
        with ThreadPoolExecutor(parallel_https) as executor:
            # First submit all files
            futures = [executor.submit(lambda x: download_file(x, https_config), f)
                       for f in tqdm(task_generator, disable=not verbose, desc="Finding files")]

            # Check that they completed successfully
            for result in tqdm(as_completed(futures), disable=not verbose, desc="Downloading files"):
                if result.exception() is not None:
                    for f in futures:
                        f.cancel()
                    raise result.exception()

    def dataset_present(self, dataset: FoundryDataset):
        path = os.path.join(self.local_cache_dir, dataset.source_id)
        if os.path.isdir(path):
            # if directory is present, but doesn't have the correct number of files inside,
            # dataset will attempt to redownload
            if dataset.splits:
                # array to keep track of missing files
                missing_files = []
                for split in dataset.splits:
                    if split.path[0] == '/':
                        split.path = split.path[1:]
                    if not os.path.isfile(os.path.join(path, split.path)):
                        missing_files.append(split.path)
                # if number of missing files is greater than zero, redownload with informative message
                if len(missing_files) > 0:
                    logger.info(f"Dataset will be redownloaded, following files are missing: {missing_files}")
                    return False
                else:
                    logger.info("Dataset has already been downloaded and contains all the desired files")
                    return True
            else:
                # in the case of no splits, ensure the directory contains at least one file
                if len(os.listdir(path)) >= 1:
                    logger.info("Dataset has already been downloaded and contains all the desired files")
                    return True
                else:
                    logger.info("Dataset will be redownloaded, expected file is missing")
                    return False

    def clear_cache(self):
        """Deletes all of the locally stored datasets"""
        ...
