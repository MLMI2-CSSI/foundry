# Foundry Scripts

Utility scripts for managing Foundry datasets.

## batch_push_to_hf.py

Push all Foundry datasets to HuggingFace Hub for broader discoverability.

### Quick Start

```bash
# 1. Install dependencies
pip install foundry-ml[huggingface]

# 2. Set your HuggingFace token
export HF_TOKEN="hf_your_token_here"

# 3. Dry run (see what would be uploaded)
python scripts/batch_push_to_hf.py --dry-run

# 4. Upload all datasets
python scripts/batch_push_to_hf.py --org foundry-ml
```

### Setup

See the full setup instructions at the top of `batch_push_to_hf.py` or run:

```bash
python scripts/batch_push_to_hf.py --help
```
