# Error Handling

Foundry uses structured error classes that provide clear context for both humans and AI agents.

## Error Structure

All Foundry errors include:

```python
class FoundryError(Exception):
    code: str           # Machine-readable error code
    message: str        # Human-readable message
    details: dict       # Additional context
    recovery_hint: str  # How to fix the issue
```

## Error Types

### DatasetNotFoundError

Raised when a search or get operation returns no results.

```python
from foundry.errors import DatasetNotFoundError

try:
    dataset = f.get_dataset("nonexistent-doi")
except DatasetNotFoundError as e:
    print(e.code)           # "DATASET_NOT_FOUND"
    print(e.message)        # "No dataset found matching..."
    print(e.recovery_hint)  # "Try a broader search term..."
```

### AuthenticationError

Raised when authentication fails.

```python
from foundry.errors import AuthenticationError

try:
    f = Foundry(use_globus=True)
except AuthenticationError as e:
    print(e.code)           # "AUTH_FAILED"
    print(e.details)        # {"service": "Globus"}
    print(e.recovery_hint)  # "Run Foundry(no_browser=False)..."
```

### DownloadError

Raised when a file download fails.

```python
from foundry.errors import DownloadError

try:
    data = dataset.get_as_dict()
except DownloadError as e:
    print(e.code)           # "DOWNLOAD_FAILED"
    print(e.details)        # {"url": "...", "reason": "..."}
    print(e.recovery_hint)  # "Check network connection..."
```

### DataLoadError

Raised when data files cannot be parsed.

```python
from foundry.errors import DataLoadError

try:
    data = dataset.get_as_dict()
except DataLoadError as e:
    print(e.code)           # "DATA_LOAD_FAILED"
    print(e.details)        # {"file_path": "...", "data_type": "..."}
```

### ValidationError

Raised when metadata validation fails.

```python
from foundry.errors import ValidationError

try:
    f.publish(invalid_metadata, ...)
except ValidationError as e:
    print(e.code)           # "VALIDATION_FAILED"
    print(e.details)        # {"field_name": "creators", "schema_type": "datacite"}
```

### PublishError

Raised when dataset publication fails.

```python
from foundry.errors import PublishError

try:
    f.publish(metadata, data_path="./data", source_id="my_dataset")
except PublishError as e:
    print(e.code)           # "PUBLISH_FAILED"
    print(e.details)        # {"source_id": "...", "status": "..."}
```

### CacheError

Raised when local cache operations fail.

```python
from foundry.errors import CacheError

try:
    data = dataset.get_as_dict()
except CacheError as e:
    print(e.code)           # "CACHE_ERROR"
    print(e.details)        # {"operation": "write", "cache_path": "..."}
```

### ConfigurationError

Raised when configuration is invalid.

```python
from foundry.errors import ConfigurationError

try:
    f = Foundry(use_globus="maybe")  # Invalid value
except ConfigurationError as e:
    print(e.code)           # "CONFIG_ERROR"
    print(e.details)        # {"setting": "use_globus", "current_value": "maybe"}
```

## Error Codes Reference

| Code | Error Class | Common Causes |
|------|-------------|---------------|
| `DATASET_NOT_FOUND` | DatasetNotFoundError | Invalid DOI, no search results |
| `AUTH_FAILED` | AuthenticationError | Expired token, no credentials |
| `DOWNLOAD_FAILED` | DownloadError | Network issues, URL not found |
| `DATA_LOAD_FAILED` | DataLoadError | Corrupted file, wrong format |
| `VALIDATION_FAILED` | ValidationError | Missing required fields |
| `PUBLISH_FAILED` | PublishError | Server error, permission denied |
| `CACHE_ERROR` | CacheError | Disk full, permission denied |
| `CONFIG_ERROR` | ConfigurationError | Invalid parameter values |

## Handling Errors

### Basic Pattern

```python
from foundry import Foundry
from foundry.errors import DatasetNotFoundError, DownloadError

f = Foundry()

try:
    dataset = f.get_dataset("10.18126/abc123")
    data = dataset.get_as_dict()
except DatasetNotFoundError as e:
    print(f"Dataset not found: {e.message}")
    print(f"Try: {e.recovery_hint}")
except DownloadError as e:
    print(f"Download failed: {e.message}")
    print(f"URL: {e.details.get('url')}")
```

### Catch All Foundry Errors

```python
from foundry.errors import FoundryError

try:
    # Your code
    pass
except FoundryError as e:
    print(f"[{e.code}] {e.message}")
    if e.recovery_hint:
        print(f"Suggestion: {e.recovery_hint}")
```

### Serialization for APIs

Errors can be serialized for JSON responses:

```python
from foundry.errors import DatasetNotFoundError
import json

error = DatasetNotFoundError("missing-dataset")
error_dict = error.to_dict()

print(json.dumps(error_dict, indent=2))
# {
#   "code": "DATASET_NOT_FOUND",
#   "message": "No dataset found matching query: 'missing-dataset'",
#   "details": {"query": "missing-dataset", "search_type": "query"},
#   "recovery_hint": "Try a broader search term..."
# }
```

## For AI Agents

Structured errors are designed for programmatic handling:

```python
def handle_foundry_operation(operation):
    try:
        return operation()
    except FoundryError as e:
        return {
            "success": False,
            "error_code": e.code,
            "message": e.message,
            "recovery_action": e.recovery_hint
        }
```

The `recovery_hint` field is particularly useful for agents to suggest next steps to users.

## Custom Error Handling

### Retry Logic

```python
import time
from foundry.errors import DownloadError

def download_with_retry(dataset, max_retries=3):
    for attempt in range(max_retries):
        try:
            return dataset.get_as_dict()
        except DownloadError as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

### Fallback Strategies

```python
from foundry.errors import DownloadError

try:
    # Try HTTPS first (default)
    f = Foundry()
    data = dataset.get_as_dict()
except DownloadError:
    # Fall back to Globus
    f = Foundry(use_globus=True)
    data = dataset.get_as_dict()
```
