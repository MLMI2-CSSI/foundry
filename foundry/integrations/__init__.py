"""Foundry integrations with external platforms.

This module provides bridges to other data ecosystems:
- Hugging Face Hub: Export datasets to HF for broader visibility

Usage:
    from foundry.integrations.huggingface import push_to_hub

    # Export a Foundry dataset to Hugging Face
    dataset = foundry.get_dataset("10.18126/abc123")
    push_to_hub(dataset, "my-org/dataset-name")
"""

try:
    from .huggingface import push_to_hub  # noqa: F401
    __all__ = ["push_to_hub"]
except ImportError:
    # huggingface extras not installed
    __all__ = []
