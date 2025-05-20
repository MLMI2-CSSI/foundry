---
description: Common pitfalls and issues and how to solve them
---

# Troubleshooting

### Issues with loading or publishing Keras or Tensorflow models

![A common error that arises when there is a Keras or Tensorflow version mismatch](../.gitbook/assets/screen-shot-2021-07-15-at-10.05.40-am.png)

There is a difference between the older, plain Keras package installed via `import keras`, and the currently maintained and up-to-date Keras package installed via `from tensorflow import keras`. Currently, the DLHub SDK \(which Foundry uses under-the-hood to publish, pull, and run models and functions\) uses whichever version of Keras you have installed. 

Errors can arise when `tf.keras` is used in one part of the model pipeline, but plain `keras` is used in another.

If you have both versions of Keras installed \(which can be the case in common container environments, such as Google Colab\), DLHub will default to the plain Keras version, in case the user wants to use that with the newest version of Tensorflow. To override this functionality and use the Tensorflow Keras instead when publishing your model, pass the `force_tf_keras = True`option to `publish_model()`. 

```python
# Assume our fitted model is '7-fi-1.hdf5'.
# Create the metadata for the model
import os
# ... (rest of the Keras/Tensorflow example remains unchanged) ...
options_keras = {
            "title": "Bandgap-7-fidelity-MP-JARVIS-1",
            "short_name": "7-fi-1",
            "authors": ["Scientist, Awesome"],
            "servable": {
                "type": "keras",
                "model_path": "7-fi-1.hdf5",
                "custom_objects": {"softplus2": softplus2, # Make sure these are defined
                                   "MEGNetLayer": MEGNetLayer,
                                   "Set2Set": Set2Set},
                "force_tf_keras": True
            }
}
# res = f.publish_model(options_keras) # Assuming 'f' is a Foundry client instance
```

## Common Foundry Errors

Here are some common errors you might encounter when using Foundry and how to address them:

### Authentication Failures

*   **Error Message:** `RuntimeError: Foundry authentication failed. Please ensure you can authenticate with Globus. Original error: ...`
*   **Possible Causes:**
    *   Globus services might be temporarily unavailable.
    *   Network issues preventing connection to Globus.
    *   If using the manual authentication flow (`no_browser=True, no_local_server=True`), the authentication URL might have expired, or the pasted authorization code was incorrect.
    *   Very rarely, your stored Globus tokens might be irrevocably invalid, requiring a fresh login.
*   **Solutions:**
    *   Check the [Globus status page](https://status.globus.org/) for any ongoing incidents.
    *   Ensure your internet connection is stable.
    *   If using the manual flow, try re-initiating the `Foundry()` client to get a fresh URL and code prompt. Ensure you copy the complete URL and code.
    *   As a last resort, you might need to clear any cached Globus tokens if your environment stores them persistently outside of Foundry's typical session management, though this is uncommon for typical Foundry usage. Restarting your Python session/kernel will usually force a new login if tokens were only in memory.

### Dataset Not Found

*   **Error Message:** `foundry.foundry.DatasetNotFoundError: No results found for the query '...'` (or similar, if the exception class name changes slightly).
*   **Possible Causes:**
    *   The dataset identifier (DOI or `source_id`) is incorrect or contains typos.
    *   The dataset is not available in the search index you are targeting (e.g., searching for a test dataset in the production "mdf" index, or vice-versa).
    *   The dataset has not yet been published or has been retracted.
*   **Solutions:**
    *   Double-check the dataset identifier for accuracy.
    *   Ensure you are using the correct Foundry index. You can specify it during initialization: `f = Foundry(index="mdf")` (for production) or `f = Foundry(index="mdf-test")` (for test datasets).
    *   Verify the dataset's status on [Foundry-ML.org](https://foundry-ml.org/) or the relevant data repository.

### Pydantic Validation Errors

Foundry uses [Pydantic](https://docs.pydantic.dev/) models to define and validate metadata structures, such as `FoundryDatacite` (for DataCite information) and `FoundrySchema` (for dataset-specific configuration like splits and inputs/outputs). If you encounter a `pydantic.ValidationError`, it means the metadata you provided (e.g., when creating a `FoundryDataset` object for publication) does not conform to the expected schema.

*   **Error Message Example (from `FoundryDataset` initialization):**
    ```
    pydantic.error_wrappers.ValidationError: N validation errors for FoundryDatacite
    dc.titles.0.title
      Field required [type=missing, input_value={...}, input_type=dict]
    ```
*   **How to Interpret:**
    *   The error message will list each field that failed validation.
    *   `loc`: This tuple indicates the path to the problematic field. For example, `('dc', 'titles', 0, 'title')` means the error is within the `dc` (DataCite) part of your metadata, in the `titles` list, at the first item (index `0`), specifically in its `title` field.
    *   `msg`: This gives a human-readable description of the error, like "Field required", "value is not a valid integer", or "Input should be a valid string".
    *   `type`: A programmatic identifier for the error type (e.g., `missing`, `int_parsing`, `string_type`).
    *   `input_value`: Shows the value that caused the validation to fail for that specific field.
*   **Solutions:**
    *   Carefully examine the `loc` and `msg` for each error to understand which part of your metadata needs correction.
    *   Refer to the Foundry documentation on dataset publishing and the DataCite schema for the correct structure and required fields.
    *   The Pydantic models are defined in `foundry/models.py` and `foundry/jsonschema_models/`, which can serve as a reference for the expected schema.

### Publishing Errors

*   **Error Message:** `ValueError: Must add data to your FoundryDataset object (use the FoundryDataset.add_data() method) before publishing`
    *   **Cause:** You attempted to publish a `FoundryDataset` without specifying its data source.
    *   **Solution:** Call `dataset.add_data(local_data_path="/path/to/your/data")` or `dataset.add_data(globus_data_source="globus://endpoint/path/")` on your `FoundryDataset` object before passing it to `f.publish_dataset()`.

*   **Error Message:** `ValueError: Dataset cannot contain both local_data_path and globus_data_source attributes. Choose one by using the FoundryDataset.add_data() method.`
    *   **Cause:** You called `add_data` with both `local_data_path` and `globus_data_source` (or called `add_data` twice with different types).
    *   **Solution:** Ensure you only specify one data source for the dataset.

*   **Error Message:** `RuntimeError: Failed to submit dataset: ...` (followed by details from MDF Connect client)
    *   **Cause:** The Materials Data Facility (MDF) Connect service, which Foundry uses for publication, encountered an error during the submission process. The specific reason will be in the latter part of the error message.
    *   **Solution:** Review the detailed error message from MDF Connect. It might indicate issues with your metadata (even if it passed initial Pydantic validation, MDF Connect might have further checks), permissions, or the MDF Connect service itself.

### Data Loading Issues

*   **Error Message:** Can vary, e.g., `FileNotFoundError` if a local cache path is corrupted, or errors from underlying libraries like H5Py if a file is malformed.
*   **Possible Causes:**
    *   Incomplete or corrupted download of dataset files.
    *   Issues with the local cache directory (permissions, disk space).
    *   The dataset files themselves might be malformed.
*   **Solutions:**
    *   Try clearing the cache for that specific dataset: `dataset.clear_dataset_cache()` then try loading the data again. This will force a fresh download.
    *   Ensure the `local_cache_dir` (configured during `Foundry()` initialization, defaults to `./data`) is writable and has sufficient space.
    *   If the problem persists and seems to be with the dataset files themselves, please report it as an issue.

