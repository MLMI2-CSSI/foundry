---
description: Common pitfalls and issues and how to solve them
---

# Troubleshooting

## Issues with loading or publishing Keras or Tensorflow models

![A common error that arises when there is a Keras or Tensorflow version mismatch](../../.gitbook/assets/screen-shot-2021-07-15-at-10.05.40-am.png)

There is a difference between the older, plain Keras package installed via `import keras`, and the currently maintained and up-to-date Keras package installed via `from tensorflow import keras`. Currently, the DLHub SDK (which Foundry uses under-the-hood to publish, pull, and run models and functions) uses whichever version of Keras you have installed.

Errors can arise when `tf.keras` is used in one part of the model pipeline, but plain `keras` is used in another.

If you have both versions of Keras installed (which can be the case in common container environments, such as Google Colab), DLHub will default to the plain Keras version, in case the user wants to use that with the newest version of Tensorflow. To override this functionality and use the Tensorflow Keras instead when publishing your model, pass the `force_tf_keras = True`option to `publish_model()`.

```python
# Assume our fitted model is '7-fi-1.hdf5'.
# Create the metadata for the model
import os

options_keras = {
            "title": "Bandgap-7-fidelity-MP-JARVIS-1",
            "short_name": "7-fi-1",
            "authors": ["Scientist, Awesome"],
            "servable": {
                "type": "keras",
                "model_path": "7-fi-1.hdf5",
                "custom_objects": {"softplus2": softplus2, 
                                   "MEGNetLayer": MEGNetLayer,
                                   "Set2Set": Set2Set},
                "force_tf_keras": True
            }
}
res = f.publish_model(options_keras)
```

## Permission denied when downloading datasets from Globus

![A Globus PERMISSION\_DENIED error that occurs when a user tries to load() a dataset locally with globus=True.](<../.gitbook/assets/Screen Shot 2022-01-24 at 12.13.16 PM.png>)

When you call `f.load()` from a script or notebook on your local machine, Foundry by default downloads the dataset for you locally (unless you set `download=False`). Foundry can download data using either Globus or HTTPS -- the default is Globus (`globus=True`). Downloading a dataset via Globus uses Globus Connect Personal (GCP) installed on your local machine -- if you have not given GCP the proper permissions to write to the folder you are running your script or notebook from, then you will receive this `PERMISSION_DENIED` error.

To fix it, first make sure that GCP is running (it should be visible in your toolbar). Then, click on the icon and select **Preferences...**&#x20;

![Example of locating GCP in the toolbar and navigating to Preferences... on MacOS](<../.gitbook/assets/Screen Shot 2022-01-28 at 2.42.07 PM.png>)

From the **Preferences...** window you should be able to amend the access permissions. Be sure that you have the **Writable** column checked for your desired dataset destinations.

![Example Preferences... window with the Access tab selected to amend GCP permissions on MacOS. Add directory paths as needed to include destinations where you will be running code that uses Foundry. ](<../.gitbook/assets/Screen Shot 2022-01-28 at 2.39.02 PM.png>)

