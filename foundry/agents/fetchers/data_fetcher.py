"""Data fetching from various sources.

Handles downloading data from GitHub, Zenodo, Figshare, and other repositories.
Features: progress bars, selective download, caching, file size preview.
"""

import hashlib
import os
import re
import tarfile
import tempfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable
from urllib.parse import urlparse

import requests
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console
from rich.table import Table

from ..models import DataSource, DataFile


# Configuration
MAX_RETRIES = 5
BASE_DELAY = 2  # seconds
MAX_DELAY = 60  # seconds
CHUNK_SIZE = 64 * 1024  # 64KB chunks for better progress updates

console = Console()


@dataclass
class RemoteFile:
    """Information about a remote file before downloading."""
    name: str
    url: str
    size_bytes: int
    checksum: Optional[str] = None
    checksum_type: Optional[str] = None  # 'md5', 'sha256', etc.


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def fetch_data(
    sources: list[DataSource],
    output_dir: Path,
    interactive: bool = True,
    select_callback: Optional[Callable[[list[RemoteFile]], list[RemoteFile]]] = None,
) -> list[DataFile]:
    """Fetch data from multiple sources.

    Args:
        sources: List of DataSource objects to fetch from
        output_dir: Directory to save downloaded files
        interactive: If True, prompt user to select files
        select_callback: Optional callback for file selection (for testing)

    Returns:
        List of DataFile objects for successfully downloaded files
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []

    # Sort by confidence, try highest first
    sorted_sources = sorted(sources, key=lambda s: s.confidence, reverse=True)

    # First, process all local files (supplementary)
    local_sources = [s for s in sorted_sources if Path(s.url).exists()]
    remote_sources = [s for s in sorted_sources if not Path(s.url).exists()]

    for source in local_sources:
        try:
            source_path = Path(source.url)
            downloaded = _copy_local_file(source_path, output_dir)
            if downloaded:
                files.append(downloaded)
        except Exception as e:
            console.print(f"  [red]Failed to copy {source.url}: {e}[/red]")

    # If we have local files, don't try remote sources
    if files:
        return files

    # Try remote sources, stop after first successful download
    for source in remote_sources:
        try:
            downloaded = fetch_from_source(
                source,
                output_dir,
                interactive=interactive,
                select_callback=select_callback,
            )
            if downloaded:
                files.extend(downloaded)
                break
        except Exception as e:
            console.print(f"  [red]Failed to fetch from {source.url}: {e}[/red]")
            continue

    return files


def fetch_from_source(
    source: DataSource,
    output_dir: Path,
    interactive: bool = True,
    select_callback: Optional[Callable[[list[RemoteFile]], list[RemoteFile]]] = None,
) -> list[DataFile]:
    """Fetch data from a single source with file selection.

    Args:
        source: DataSource to fetch from
        output_dir: Directory to save files
        interactive: If True, prompt user to select files
        select_callback: Optional callback for file selection

    Returns:
        List of DataFile objects
    """
    url = source.url
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Get file listing first
    if 'zenodo.org' in domain:
        remote_files = _list_zenodo_files(url)
    elif 'figshare.com' in domain:
        remote_files = _list_figshare_files(url)
    elif 'github.com' in domain:
        # GitHub doesn't have easy file listing, download as archive
        return _fetch_github(url, output_dir)
    else:
        # Generic - try direct download
        return _fetch_generic(url, output_dir)

    if not remote_files:
        console.print("  [yellow]No files found at source[/yellow]")
        return []

    # Show file preview
    _show_file_preview(remote_files, source.url)

    # Let user select files (or use callback for testing)
    if select_callback:
        selected = select_callback(remote_files)
    elif interactive:
        selected = _prompt_file_selection(remote_files)
    else:
        selected = remote_files  # Download all in non-interactive mode

    if not selected:
        console.print("  [yellow]No files selected[/yellow]")
        return []

    # Check cache and download
    return _download_files_with_cache(selected, output_dir)


def _list_zenodo_files(url: str) -> list[RemoteFile]:
    """Get file listing from Zenodo record."""
    match = re.search(r'/records?/(\d+)', url)
    if not match:
        return []

    record_id = match.group(1)
    api_url = f"https://zenodo.org/api/records/{record_id}"

    data = _request_with_retry(api_url)
    if data is None:
        return []

    files = []
    for file_info in data.get('files', []):
        checksum = file_info.get('checksum', '')
        checksum_type = None
        checksum_value = None
        if ':' in checksum:
            checksum_type, checksum_value = checksum.split(':', 1)

        files.append(RemoteFile(
            name=file_info.get('key', 'unknown'),
            url=file_info.get('links', {}).get('self', ''),
            size_bytes=file_info.get('size', 0),
            checksum=checksum_value,
            checksum_type=checksum_type,
        ))

    return files


def _list_figshare_files(url: str) -> list[RemoteFile]:
    """Get file listing from Figshare article."""
    match = re.search(r'/articles/[^/]+/(\d+)', url)
    if not match:
        return []

    article_id = match.group(1)
    api_url = f"https://api.figshare.com/v2/articles/{article_id}"

    response = requests.get(api_url, timeout=30)
    if response.status_code != 200:
        return []

    data = response.json()
    files = []
    for file_info in data.get('files', []):
        files.append(RemoteFile(
            name=file_info.get('name', 'unknown'),
            url=file_info.get('download_url', ''),
            size_bytes=file_info.get('size', 0),
            checksum=file_info.get('computed_md5'),
            checksum_type='md5' if file_info.get('computed_md5') else None,
        ))

    return files


def _show_file_preview(files: list[RemoteFile], source_url: str) -> None:
    """Display file listing with sizes."""
    total_size = sum(f.size_bytes for f in files)

    table = Table(title=f"Files available from {source_url[:60]}...")
    table.add_column("#", style="dim", width=4)
    table.add_column("Filename", style="cyan")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Type", style="dim")

    for i, f in enumerate(files, 1):
        ext = Path(f.name).suffix.lower()
        table.add_row(
            str(i),
            f.name[:50] + ("..." if len(f.name) > 50 else ""),
            format_size(f.size_bytes),
            ext or "unknown",
        )

    console.print(table)
    console.print(f"\n  [bold]Total: {len(files)} files, {format_size(total_size)}[/bold]")


def _prompt_file_selection(files: list[RemoteFile]) -> list[RemoteFile]:
    """Prompt user to select which files to download."""
    console.print("\n  [dim]Enter file numbers to download (e.g., '1,3,5' or 'all' or 'none'):[/dim]")

    try:
        choice = input("  > ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return []

    if choice == 'none' or choice == 'n':
        return []
    if choice == 'all' or choice == 'a' or choice == '':
        return files

    # Parse selection
    selected = []
    try:
        for part in choice.split(','):
            part = part.strip()
            if '-' in part:
                # Range like "1-5"
                start, end = map(int, part.split('-'))
                for i in range(start, end + 1):
                    if 1 <= i <= len(files):
                        selected.append(files[i - 1])
            else:
                idx = int(part)
                if 1 <= idx <= len(files):
                    selected.append(files[idx - 1])
    except ValueError:
        console.print("  [yellow]Invalid selection, downloading all files[/yellow]")
        return files

    return selected


def _download_files_with_cache(
    files: list[RemoteFile],
    output_dir: Path,
) -> list[DataFile]:
    """Download files with caching and progress bars."""
    downloaded = []
    to_download = []

    # Check cache
    for f in files:
        cached_path = output_dir / f.name
        if cached_path.exists():
            # Verify size matches
            if cached_path.stat().st_size == f.size_bytes:
                console.print(f"  [dim]Using cached: {f.name}[/dim]")
                downloaded.append(DataFile(
                    path=cached_path,
                    original_url=f.url,
                    format=_detect_format(cached_path),
                    size_bytes=f.size_bytes,
                ))
                continue
            else:
                console.print(f"  [yellow]Cache size mismatch, re-downloading: {f.name}[/yellow]")

        to_download.append(f)

    if not to_download:
        return downloaded

    # Download with progress
    total_size = sum(f.size_bytes for f in to_download)
    console.print(f"\n  Downloading {len(to_download)} files ({format_size(total_size)})...")

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        for remote_file in to_download:
            result = _download_single_file(remote_file, output_dir, progress)
            if result:
                downloaded.extend(result)

    return downloaded


def _download_single_file(
    remote_file: RemoteFile,
    output_dir: Path,
    progress: Progress,
) -> list[DataFile]:
    """Download a single file with progress tracking."""
    task = progress.add_task(
        f"  {remote_file.name[:30]}...",
        total=remote_file.size_bytes,
    )

    delay = BASE_DELAY
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(remote_file.url, stream=True, timeout=300)

            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) if retry_after else min(delay * (2 ** attempt), MAX_DELAY)
                progress.update(task, description=f"  [yellow]Rate limited, waiting {wait_time}s...[/yellow]")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            file_path = output_dir / remote_file.name
            size = 0
            hasher = hashlib.md5() if remote_file.checksum_type == 'md5' else None

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
                    size += len(chunk)
                    if hasher:
                        hasher.update(chunk)
                    progress.update(task, advance=len(chunk))

            # Verify checksum if available
            if hasher and remote_file.checksum:
                if hasher.hexdigest() != remote_file.checksum:
                    console.print(f"  [red]Checksum mismatch for {remote_file.name}[/red]")
                    file_path.unlink()
                    return []

            progress.update(task, description=f"  [green]✓[/green] {remote_file.name[:30]}")

            # Handle archives
            format_type = _detect_format(file_path)
            if format_type == 'zip':
                files = _extract_zip(file_path, output_dir, remote_file.url)
                file_path.unlink()
                return files
            elif remote_file.name.endswith('.tar.gz') or remote_file.name.endswith('.tgz'):
                files = _extract_tarball(file_path, output_dir, remote_file.url)
                file_path.unlink()
                return files

            return [DataFile(
                path=file_path,
                original_url=remote_file.url,
                format=format_type,
                size_bytes=size,
            )]

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                wait_time = min(delay * (2 ** attempt), MAX_DELAY)
                progress.update(task, description=f"  [yellow]Retry in {wait_time}s...[/yellow]")
                time.sleep(wait_time)
            else:
                progress.update(task, description=f"  [red]✗[/red] {remote_file.name[:30]}")
                return []

    return []


def _copy_local_file(source_path: Path, output_dir: Path) -> Optional[DataFile]:
    """Copy a local file to the output directory."""
    import shutil

    dest_path = output_dir / source_path.name
    shutil.copy2(source_path, dest_path)

    return DataFile(
        path=dest_path,
        original_url=str(source_path),
        format=_detect_format(dest_path),
        size_bytes=dest_path.stat().st_size,
    )


def _fetch_github(url: str, output_dir: Path) -> list[DataFile]:
    """Fetch data from GitHub repository."""
    if not url.endswith('.zip'):
        for branch in ['main', 'master']:
            zip_url = f"{url.rstrip('/')}/archive/refs/heads/{branch}.zip"
            try:
                return _download_and_extract_zip(zip_url, output_dir)
            except Exception:
                continue
        return _fetch_generic(url, output_dir)

    return _download_and_extract_zip(url, output_dir)


def _fetch_generic(url: str, output_dir: Path) -> list[DataFile]:
    """Generic file download with progress."""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or 'data'

    # Try to get file size first
    try:
        head_resp = requests.head(url, timeout=10, allow_redirects=True)
        size = int(head_resp.headers.get('Content-Length', 0))
    except Exception:
        size = 0

    remote_file = RemoteFile(name=filename, url=url, size_bytes=size)

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        console=console,
    ) as progress:
        return _download_single_file(remote_file, output_dir, progress)


def _request_with_retry(url: str) -> Optional[dict]:
    """Make a GET request with exponential backoff for rate limiting."""
    delay = BASE_DELAY

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=30)

            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) if retry_after else min(delay * (2 ** attempt), MAX_DELAY)
                console.print(f"  [yellow]Rate limited. Waiting {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})...[/yellow]")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                wait_time = min(delay * (2 ** attempt), MAX_DELAY)
                console.print(f"  [yellow]Request failed: {e}. Retrying in {wait_time}s...[/yellow]")
                time.sleep(wait_time)
            else:
                raise

    return None


def _download_and_extract_zip(url: str, output_dir: Path) -> list[DataFile]:
    """Download and extract a ZIP file with progress."""
    # Get file size
    try:
        head_resp = requests.head(url, timeout=10, allow_redirects=True)
        size = int(head_resp.headers.get('Content-Length', 0))
    except Exception:
        size = 0

    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
        tmp_path = Path(tmp.name)

        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("  Downloading archive...", total=size or None)

            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                tmp.write(chunk)
                progress.update(task, advance=len(chunk))

    try:
        return _extract_zip(tmp_path, output_dir, url)
    finally:
        tmp_path.unlink()


def _extract_zip(zip_path: Path, output_dir: Path, original_url: str) -> list[DataFile]:
    """Extract data files from a ZIP archive."""
    files = []
    data_extensions = {'.csv', '.json', '.xlsx', '.xls', '.hdf5', '.h5', '.parquet', '.tsv'}

    with zipfile.ZipFile(zip_path, 'r') as zf:
        for name in zf.namelist():
            if name.endswith('/') or '/.' in name or name.startswith('.'):
                continue

            ext = Path(name).suffix.lower()
            if ext in data_extensions:
                filename = Path(name).name
                target_path = output_dir / filename

                with zf.open(name) as source, open(target_path, 'wb') as target:
                    target.write(source.read())

                files.append(DataFile(
                    path=target_path,
                    original_url=original_url,
                    format=ext[1:],
                    size_bytes=target_path.stat().st_size,
                ))

    return files


def _extract_tarball(tar_path: Path, output_dir: Path, original_url: str) -> list[DataFile]:
    """Extract data files from a tar.gz archive."""
    files = []
    data_extensions = {'.csv', '.json', '.xlsx', '.xls', '.hdf5', '.h5', '.parquet', '.tsv'}

    with tarfile.open(tar_path, 'r:*') as tf:
        for member in tf.getmembers():
            if member.isdir() or '/.' in member.name or member.name.startswith('.'):
                continue

            ext = Path(member.name).suffix.lower()
            if ext in data_extensions:
                filename = Path(member.name).name
                target_path = output_dir / filename

                source = tf.extractfile(member)
                if source:
                    with open(target_path, 'wb') as target:
                        target.write(source.read())

                    files.append(DataFile(
                        path=target_path,
                        original_url=original_url,
                        format=ext[1:],
                        size_bytes=target_path.stat().st_size,
                    ))

    return files


def _detect_format(file_path: Path) -> str:
    """Detect file format from extension."""
    ext = file_path.suffix.lower()

    format_map = {
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.json': 'json',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.hdf5': 'hdf5',
        '.h5': 'hdf5',
        '.parquet': 'parquet',
        '.zip': 'zip',
    }

    return format_map.get(ext, 'unknown')
