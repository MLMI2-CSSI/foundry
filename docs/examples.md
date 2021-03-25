# Examples

## [See Scientific Examples](https://github.com/MLMI2-CSSI/foundry/tree/master/examples)

## Basic Usage

The Foundry client can be used to access datasets using a `source_id`, e.g. here "\_test\_foundry\_fashion\_mnist\_v1.1":

```python
from foundry import Foundry
f = Foundry()
f = f.load("_test_foundry_fashion_mnist_v1.1")
```

This will remotely load the necessary metadata \(e.g., data location, data keys, etc.\) as well as download the data to local storage if it is not already present. Data can be downloaded via HTTPS without additional setup or more optimally with a Globus endpoint [set up](https://www.globus.org/globus-connect-personal) on your machine.

 Once the data are accessible locally, load the data into the client:

```python
X, y = f.load_data()
```

The data are then usable:

```python
n_cols = 6
display_shape = (28,28)
fig, ax = plt.subplots(1,n_cols)

for i in range(0, n_cols):
    ax[i].imshow(X[i].reshape(display_shape), cmap='gray')
```

This example can be found in `/examples/fashion-mnist/`.

#### Other uses

To just download the data without loading the additional metadata:

```python
f = Foundry().download("_test_foundry_fashion_mnist_v1.1")
```

## Using Foundry on Cloud Computing Resources

Foundry works with common cloud computing providers like the NSF sponsored Jetstream and Google Colab. When instantiating the Foundry client, simple add the following arguments to use a compatible authentication flow.

```python
f = Foundry(no_browser=True, no_local_server=True)
```

When downloading data, add the following argument to download contents by HTTPS. This method may be non-performant for large datasets

```python
f.download(globus=False)
```

