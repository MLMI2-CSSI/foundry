# Using with ML Frameworks

Foundry integrates with popular ML frameworks.

## PyTorch

### Load as PyTorch Dataset

```python
# Get PyTorch-compatible dataset
torch_dataset = dataset.get_as_torch(split='train')

# Use with DataLoader
from torch.utils.data import DataLoader

loader = DataLoader(torch_dataset, batch_size=32, shuffle=True)

for batch in loader:
    inputs, targets = batch
    # Train your model
```

### Full Training Example

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from foundry import Foundry

# Load data
f = Foundry()
ds = f.search("band gap", limit=1).iloc[0].FoundryDataset

train_dataset = ds.get_as_torch(split='train')
test_dataset = ds.get_as_torch(split='test')

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32)

# Define model
model = nn.Sequential(
    nn.Linear(input_size, 64),
    nn.ReLU(),
    nn.Linear(64, 1)
)

# Train
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.MSELoss()

for epoch in range(10):
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
```

## TensorFlow

### Load as tf.data.Dataset

```python
# Get TensorFlow-compatible dataset
tf_dataset = dataset.get_as_tensorflow(split='train')

# Batch and prefetch
tf_dataset = tf_dataset.batch(32).prefetch(1)

# Use in training
model.fit(tf_dataset, epochs=10)
```

### Full Training Example

```python
import tensorflow as tf
from foundry import Foundry

# Load data
f = Foundry()
ds = f.search("band gap", limit=1).iloc[0].FoundryDataset

train_ds = ds.get_as_tensorflow(split='train')
test_ds = ds.get_as_tensorflow(split='test')

train_ds = train_ds.batch(32).prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.batch(32)

# Define model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer='adam',
    loss='mse',
    metrics=['mae']
)

# Train
model.fit(train_ds, validation_data=test_ds, epochs=10)
```

## Scikit-learn

Use the dictionary format:

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import pandas as pd
from foundry import Foundry

# Load data
f = Foundry()
ds = f.search("band gap", limit=1).iloc[0].FoundryDataset
data = ds.get_as_dict()

X_train, y_train = data['train']
X_test, y_test = data['test']

# Convert to arrays
X_train_df = pd.DataFrame(X_train)
y_train_arr = list(y_train.values())[0]

# Train
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train_df, y_train_arr)

# Evaluate
X_test_df = pd.DataFrame(X_test)
y_test_arr = list(y_test.values())[0]
score = model.score(X_test_df, y_test_arr)
print(f"R² score: {score:.3f}")
```

## Generic Python

For any framework, use the dictionary format:

```python
data = dataset.get_as_dict()
X, y = data['train']

# X is a dict: {'feature1': [...], 'feature2': [...]}
# y is a dict: {'target': [...]}

# Convert as needed for your framework
import numpy as np
X_array = np.column_stack([X[k] for k in X.keys()])
y_array = np.array(list(y.values())[0])
```

## Tips

### Check Data Shape

```python
data = dataset.get_as_dict()
X, y = data['train']

print(f"Features: {list(X.keys())}")
print(f"Targets: {list(y.keys())}")
print(f"Samples: {len(list(X.values())[0])}")
```

### Handle Missing Values

```python
import pandas as pd

X, y = data['train']
df = pd.DataFrame(X)
print(df.isnull().sum())  # Check for missing values
df = df.fillna(0)  # Or handle as appropriate
```

### Feature Engineering

```python
# Get schema to understand features
schema = dataset.get_schema()

for field in schema['fields']:
    print(f"{field['name']}: {field['description']} ({field['units']})")
```
