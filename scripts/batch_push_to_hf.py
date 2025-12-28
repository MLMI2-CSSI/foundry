#!/usr/bin/env python3
"""
Batch Push Foundry Datasets to HuggingFace Hub
===============================================

This script exports all Foundry datasets to HuggingFace Hub, making them
discoverable in the broader ML ecosystem.

SETUP INSTRUCTIONS
------------------

1. CREATE A HUGGINGFACE ACCOUNT
   - Go to https://huggingface.co/join
   - Create an account

2. CREATE AN ORGANIZATION (Recommended)
   - Go to https://huggingface.co/organizations/new
   - Create organization named "foundry-ml" (or your preferred name)
   - This keeps all datasets under one namespace: foundry-ml/dataset-name

3. GET YOUR API TOKEN
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Name: "foundry-batch-upload"
   - Role: "Write" (required to create repos)
   - Copy the token (starts with "hf_...")

4. SET YOUR TOKEN (choose one method):

   Option A - Environment variable (recommended):
   ```bash
   export HF_TOKEN="hf_your_token_here"
   python scripts/batch_push_to_hf.py
   ```

   Option B - Login via CLI (persists across sessions):
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   # Paste your token when prompted
   python scripts/batch_push_to_hf.py
   ```

   Option C - Pass directly (not recommended for shared scripts):
   ```bash
   python scripts/batch_push_to_hf.py --token "hf_your_token_here"
   ```

5. INSTALL DEPENDENCIES
   ```bash
   pip install foundry-ml[huggingface]
   # or
   pip install datasets huggingface_hub
   ```

6. RUN THE SCRIPT
   ```bash
   python scripts/batch_push_to_hf.py --org foundry-ml
   ```

USAGE
-----
  python scripts/batch_push_to_hf.py [OPTIONS]

OPTIONS
-------
  --org ORG        HuggingFace organization name (default: foundry-ml)
  --token TOKEN    HuggingFace API token (or set HF_TOKEN env var)
  --private        Create private repositories
  --dry-run        List datasets without uploading
  --limit N        Only process first N datasets (for testing)
  --skip N         Skip first N datasets (for resuming)
  --dataset NAME   Process only this specific dataset
  --output FILE    Save results to JSON file

EXAMPLES
--------
  # Dry run - see what would be uploaded
  python scripts/batch_push_to_hf.py --dry-run

  # Upload all datasets to foundry-ml organization
  python scripts/batch_push_to_hf.py --org foundry-ml

  # Test with first 3 datasets
  python scripts/batch_push_to_hf.py --org foundry-ml --limit 3

  # Resume from dataset 10 (if previous run failed)
  python scripts/batch_push_to_hf.py --org foundry-ml --skip 10

  # Upload a single specific dataset
  python scripts/batch_push_to_hf.py --org foundry-ml --dataset "foundry_bandgap_oqmd"
"""

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class UploadResult:
    """Result of a single dataset upload."""
    dataset_name: str
    doi: str
    repo_id: str
    status: str  # 'success', 'failed', 'skipped'
    url: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: Optional[float] = None


def get_hf_token(args_token: Optional[str] = None) -> str:
    """Get HuggingFace token from args, env, or cached login."""
    # 1. Check command line argument
    if args_token:
        return args_token

    # 2. Check environment variable
    env_token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGINGFACE_TOKEN')
    if env_token:
        return env_token

    # 3. Check if logged in via huggingface-cli
    try:
        from huggingface_hub import HfFolder
        cached_token = HfFolder.get_token()
        if cached_token:
            return cached_token
    except Exception:
        pass

    # 4. No token found
    raise ValueError(
        "No HuggingFace token found. Please either:\n"
        "  1. Set HF_TOKEN environment variable\n"
        "  2. Run 'huggingface-cli login'\n"
        "  3. Pass --token argument\n"
        "\nGet your token at: https://huggingface.co/settings/tokens"
    )


def sanitize_repo_name(name: str) -> str:
    """Convert dataset name to valid HF repo name."""
    # HF repo names: lowercase, alphanumeric, hyphens, underscores
    # Max 96 characters
    import re
    name = name.lower()
    name = re.sub(r'[^a-z0-9_-]', '-', name)
    name = re.sub(r'-+', '-', name)  # Collapse multiple hyphens
    name = name.strip('-_')
    return name[:96]


def check_repo_exists(api, repo_id: str) -> bool:
    """Check if a repository already exists on HF Hub."""
    try:
        api.repo_info(repo_id=repo_id, repo_type="dataset")
        return True
    except Exception:
        return False


def push_dataset(
    dataset,
    org: str,
    token: str,
    private: bool = False,
) -> UploadResult:
    """Push a single dataset to HuggingFace Hub."""
    from foundry.integrations.huggingface import push_to_hub
    from huggingface_hub import HfApi

    dataset_name = dataset.dataset_name
    doi = str(dataset.dc.identifier.identifier) if dataset.dc.identifier else "unknown"
    repo_name = sanitize_repo_name(dataset_name)
    repo_id = f"{org}/{repo_name}"

    start_time = time.time()

    try:
        # Check if already exists
        api = HfApi(token=token)
        if check_repo_exists(api, repo_id):
            logger.info(f"  Repository {repo_id} already exists, skipping")
            return UploadResult(
                dataset_name=dataset_name,
                doi=doi,
                repo_id=repo_id,
                status='skipped',
                url=f"https://huggingface.co/datasets/{repo_id}",
                error="Repository already exists"
            )

        # Push to hub
        url = push_to_hub(
            dataset=dataset,
            repo_id=repo_id,
            token=token,
            private=private,
        )

        duration = time.time() - start_time
        logger.info(f"  Successfully pushed to {url} ({duration:.1f}s)")

        return UploadResult(
            dataset_name=dataset_name,
            doi=doi,
            repo_id=repo_id,
            status='success',
            url=url,
            duration_seconds=duration
        )

    except Exception as e:
        duration = time.time() - start_time
        error_msg = str(e)
        logger.error(f"  Failed: {error_msg}")

        return UploadResult(
            dataset_name=dataset_name,
            doi=doi,
            repo_id=repo_id,
            status='failed',
            error=error_msg,
            duration_seconds=duration
        )


def main():
    parser = argparse.ArgumentParser(
        description="Batch push Foundry datasets to HuggingFace Hub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--org',
        default='foundry-ml',
        help='HuggingFace organization name (default: foundry-ml)'
    )
    parser.add_argument(
        '--token',
        help='HuggingFace API token (or set HF_TOKEN env var)'
    )
    parser.add_argument(
        '--private',
        action='store_true',
        help='Create private repositories'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='List datasets without uploading'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Only process first N datasets'
    )
    parser.add_argument(
        '--skip',
        type=int,
        default=0,
        help='Skip first N datasets'
    )
    parser.add_argument(
        '--dataset',
        help='Process only this specific dataset name'
    )
    parser.add_argument(
        '--output',
        help='Save results to JSON file'
    )

    args = parser.parse_args()

    # Import Foundry
    try:
        from foundry import Foundry
    except ImportError:
        logger.error("Foundry not installed. Run: pip install foundry-ml")
        sys.exit(1)

    # Check HF dependencies
    try:
        from datasets import Dataset
        from huggingface_hub import HfApi
    except ImportError:
        logger.error(
            "HuggingFace dependencies not installed.\n"
            "Run: pip install foundry-ml[huggingface]"
        )
        sys.exit(1)

    # Get token (skip for dry run)
    token = None
    if not args.dry_run:
        try:
            token = get_hf_token(args.token)
            logger.info(f"Using HuggingFace token: {token[:10]}...")
        except ValueError as e:
            logger.error(str(e))
            sys.exit(1)

    # Initialize Foundry
    logger.info("Connecting to Foundry...")
    f = Foundry()

    # List all datasets
    logger.info("Fetching dataset list...")
    datasets_df = f.list()
    total_datasets = len(datasets_df)
    logger.info(f"Found {total_datasets} datasets")

    # Apply filters
    if args.dataset:
        datasets_df = datasets_df[datasets_df['dataset_name'] == args.dataset]
        if len(datasets_df) == 0:
            logger.error(f"Dataset '{args.dataset}' not found")
            sys.exit(1)

    if args.skip:
        datasets_df = datasets_df.iloc[args.skip:]
        logger.info(f"Skipping first {args.skip} datasets")

    if args.limit:
        datasets_df = datasets_df.iloc[:args.limit]
        logger.info(f"Limiting to {args.limit} datasets")

    # Preview
    print("\n" + "=" * 60)
    print("DATASETS TO PROCESS")
    print("=" * 60)
    for i, (_, row) in enumerate(datasets_df.iterrows()):
        name = row.get('dataset_name', 'N/A')
        title = str(row.get('title', 'N/A'))[:50]
        repo_name = sanitize_repo_name(name)
        print(f"{i+1:3}. {args.org}/{repo_name}")
        print(f"     Title: {title}")
    print("=" * 60 + "\n")

    if args.dry_run:
        logger.info("Dry run complete. No datasets were uploaded.")
        return

    # Confirm
    response = input(f"Push {len(datasets_df)} datasets to {args.org}? [y/N] ")
    if response.lower() != 'y':
        logger.info("Aborted.")
        return

    # Process datasets
    results: List[UploadResult] = []
    success_count = 0
    failed_count = 0
    skipped_count = 0

    print("\n" + "=" * 60)
    print("UPLOADING")
    print("=" * 60)

    for i, (_, row) in enumerate(datasets_df.iterrows()):
        name = row.get('dataset_name', 'N/A')
        doi = row.get('DOI', 'N/A')
        # Use the pre-loaded FoundryDataset object if available
        foundry_dataset = row.get('FoundryDataset', None)

        logger.info(f"[{i+1}/{len(datasets_df)}] Processing: {name}")

        try:
            # Use pre-loaded dataset or fetch it
            if foundry_dataset is not None:
                dataset = foundry_dataset
            else:
                dataset = f.get_dataset(doi)

            # Push to HF
            result = push_dataset(
                dataset=dataset,
                org=args.org,
                token=token,
                private=args.private,
            )
            results.append(result)

            if result.status == 'success':
                success_count += 1
            elif result.status == 'skipped':
                skipped_count += 1
            else:
                failed_count += 1

        except Exception as e:
            logger.error(f"  Error loading dataset: {e}")
            results.append(UploadResult(
                dataset_name=name,
                doi=doi,
                repo_id=f"{args.org}/{sanitize_repo_name(name)}",
                status='failed',
                error=str(e)
            ))
            failed_count += 1

        # Brief pause to avoid rate limiting
        time.sleep(1)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total processed: {len(results)}")
    print(f"  Successful:    {success_count}")
    print(f"  Skipped:       {skipped_count}")
    print(f"  Failed:        {failed_count}")

    if failed_count > 0:
        print("\nFailed datasets:")
        for r in results:
            if r.status == 'failed':
                print(f"  - {r.dataset_name}: {r.error}")

    # Save results
    if args.output:
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'organization': args.org,
            'total': len(results),
            'success': success_count,
            'skipped': skipped_count,
            'failed': failed_count,
            'results': [asdict(r) for r in results]
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        logger.info(f"Results saved to {args.output}")

    # Print successful URLs
    if success_count > 0:
        print("\nSuccessfully uploaded:")
        for r in results:
            if r.status == 'success':
                print(f"  {r.url}")


if __name__ == '__main__':
    main()
