"""Foundry CLI - Beautiful command-line interface for materials science datasets.

Usage:
    foundry search "bandgap"           # Search datasets
    foundry get <doi>                  # Download a dataset
    foundry list                       # List available datasets
    foundry schema <doi>               # Show dataset schema
    foundry status <source_id>         # Check publication status
    foundry mcp start                  # Start MCP server for agent integration
"""

import json
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

app = typer.Typer(
    name="foundry",
    help="Foundry-ML: Materials science datasets for machine learning.",
    add_completion=False,
    no_args_is_help=True,
)
mcp_app = typer.Typer(help="MCP server commands for agent integration.")
app.add_typer(mcp_app, name="mcp")

console = Console()


def get_foundry(no_browser: bool = True):
    """Get a Foundry client instance."""
    from foundry import Foundry
    return Foundry(no_browser=no_browser, no_local_server=True)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query (e.g., 'bandgap', 'crystal structure')"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Search for datasets matching a query."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Searching datasets...", total=None)
        f = get_foundry()
        results = f.search(query, limit=limit)

    if len(results) == 0:
        console.print(f"[yellow]No datasets found matching '{query}'[/yellow]")
        raise typer.Exit(1)

    if output_json:
        # Output as JSON for programmatic use
        output = []
        for _, row in results.iterrows():
            ds = row.FoundryDataset
            output.append({
                "name": ds.dataset_name,
                "title": ds.dc.titles[0].title if ds.dc.titles else None,
                "doi": str(ds.dc.identifier.identifier) if ds.dc.identifier else None,
            })
        console.print(json.dumps(output, indent=2))
    else:
        # Pretty table output
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("DOI", style="dim")

        for _, row in results.iterrows():
            ds = row.FoundryDataset
            title = ds.dc.titles[0].title if ds.dc.titles else "N/A"
            doi = str(ds.dc.identifier.identifier) if ds.dc.identifier else "N/A"
            table.add_row(ds.dataset_name, title[:50] + "..." if len(title) > 50 else title, doi)

        console.print(table)
        console.print(f"\n[dim]Found {len(results)} dataset(s). Use 'foundry get <doi>' to download.[/dim]")


@app.command()
def list_datasets(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """List all available datasets."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Fetching dataset list...", total=None)
        f = get_foundry()
        results = f.list(limit=limit)

    if output_json:
        output = []
        for _, row in results.iterrows():
            ds = row.FoundryDataset
            output.append({
                "name": ds.dataset_name,
                "title": ds.dc.titles[0].title if ds.dc.titles else None,
                "doi": str(ds.dc.identifier.identifier) if ds.dc.identifier else None,
            })
        console.print(json.dumps(output, indent=2))
    else:
        table = Table(title="Available Datasets")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("DOI", style="dim")

        for _, row in results.iterrows():
            ds = row.FoundryDataset
            title = ds.dc.titles[0].title if ds.dc.titles else "N/A"
            doi = str(ds.dc.identifier.identifier) if ds.dc.identifier else "N/A"
            table.add_row(ds.dataset_name, title[:50] + "..." if len(title) > 50 else title, doi)

        console.print(table)
        console.print(f"\n[dim]Showing {len(results)} dataset(s).[/dim]")


# Alias for list
app.command(name="list")(list_datasets)


@app.command()
def get(
    doi: str = typer.Argument(..., help="DOI of the dataset to download"),
    split: Optional[str] = typer.Option(None, "--split", "-s", help="Specific split to download"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory"),
):
    """Download a dataset by DOI."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Connecting to Foundry...", total=None)
        f = get_foundry()

        progress.update(task, description=f"Fetching dataset {doi}...")
        try:
            dataset = f.get_dataset(doi)
        except Exception as e:
            console.print(f"[red]Error: Could not find dataset '{doi}'[/red]")
            console.print(f"[dim]{e}[/dim]")
            raise typer.Exit(1)

        progress.update(task, description="Downloading data...")
        try:
            data = dataset.get_as_dict(split=split)
        except Exception as e:
            console.print(f"[red]Error downloading data: {e}[/red]")
            raise typer.Exit(1)

    # Show summary
    console.print(Panel(
        f"[green]Successfully downloaded![/green]\n\n"
        f"[bold]Dataset:[/bold] {dataset.dataset_name}\n"
        f"[bold]Title:[/bold] {dataset.dc.titles[0].title if dataset.dc.titles else 'N/A'}\n"
        f"[bold]Splits:[/bold] {', '.join(data.keys()) if isinstance(data, dict) else 'N/A'}",
        title="Download Complete",
    ))


@app.command()
def schema(
    doi: str = typer.Argument(..., help="DOI of the dataset"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Show the schema of a dataset - what fields it contains."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Fetching schema...", total=None)
        f = get_foundry()
        try:
            dataset = f.get_dataset(doi)
        except Exception as e:
            console.print(f"[red]Error: Could not find dataset '{doi}'[/red]")
            raise typer.Exit(1)

    schema_info = {
        "name": dataset.dataset_name,
        "title": dataset.dc.titles[0].title if dataset.dc.titles else None,
        "doi": str(dataset.dc.identifier.identifier) if dataset.dc.identifier else None,
        "data_type": dataset.foundry_schema.data_type,
        "splits": [
            {"name": s.label, "type": s.type}
            for s in (dataset.foundry_schema.splits or [])
        ],
        "fields": [
            {
                "name": k.key[0] if k.key else None,
                "role": k.type,
                "description": k.description,
                "units": k.units,
            }
            for k in (dataset.foundry_schema.keys or [])
        ],
    }

    if output_json:
        console.print(json.dumps(schema_info, indent=2))
    else:
        # Pretty output
        console.print(Panel(
            f"[bold]{schema_info['title']}[/bold]\n"
            f"[dim]DOI: {schema_info['doi']}[/dim]\n"
            f"[dim]Type: {schema_info['data_type']}[/dim]",
            title=f"Dataset: {schema_info['name']}",
        ))

        if schema_info['splits']:
            console.print("\n[bold]Splits:[/bold]")
            for split in schema_info['splits']:
                console.print(f"  - {split['name']} ({split['type']})")

        if schema_info['fields']:
            console.print("\n[bold]Fields:[/bold]")
            table = Table(show_header=True)
            table.add_column("Name", style="cyan")
            table.add_column("Role", style="green")
            table.add_column("Description")
            table.add_column("Units", style="dim")

            for field in schema_info['fields']:
                table.add_row(
                    field['name'] or "N/A",
                    field['role'] or "N/A",
                    (field['description'] or "")[:40],
                    field['units'] or "",
                )
            console.print(table)


@app.command()
def status(
    source_id: str = typer.Argument(..., help="Source ID to check status for"),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Check the publication status of a dataset."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Checking status...", total=None)
        f = get_foundry()
        try:
            result = f.check_status(source_id)
        except Exception as e:
            console.print(f"[red]Error checking status: {e}[/red]")
            raise typer.Exit(1)

    if output_json:
        console.print(json.dumps(result, indent=2, default=str))
    else:
        console.print(Panel(str(result), title=f"Status: {source_id}"))


@app.command()
def catalog(
    output_json: bool = typer.Option(True, "--json", "-j", help="Output as JSON (default)"),
):
    """Dump all available datasets as JSON catalog."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Building catalog...", total=None)
        f = get_foundry()
        results = f.list(limit=1000)

    output = []
    for _, row in results.iterrows():
        ds = row.FoundryDataset
        output.append({
            "name": ds.dataset_name,
            "title": ds.dc.titles[0].title if ds.dc.titles else None,
            "doi": str(ds.dc.identifier.identifier) if ds.dc.identifier else None,
            "description": ds.dc.descriptions[0].description if ds.dc.descriptions else None,
        })

    console.print(json.dumps(output, indent=2))


@app.command(name="push-to-hf")
def push_to_hf(
    doi: str = typer.Argument(..., help="DOI of the dataset to export"),
    repo: str = typer.Option(..., "--repo", "-r", help="HuggingFace repo ID (e.g., 'org/dataset-name')"),
    token: Optional[str] = typer.Option(None, "--token", "-t", help="HuggingFace API token"),
    private: bool = typer.Option(False, "--private", "-p", help="Create a private repository"),
):
    """Export a Foundry dataset to Hugging Face Hub.

    This makes materials science datasets discoverable in the broader ML ecosystem.

    Example:
        foundry push-to-hf 10.18126/abc123 --repo my-org/bandgap-data
    """
    try:
        from foundry.integrations.huggingface import push_to_hub
    except ImportError:
        console.print(
            "[red]HuggingFace integration not installed.[/red]\n"
            "Install with: [cyan]pip install foundry-ml[huggingface][/cyan]"
        )
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Connecting to Foundry...", total=None)
        f = get_foundry()

        progress.update(task, description=f"Loading dataset {doi}...")
        try:
            dataset = f.get_dataset(doi)
        except Exception as e:
            console.print(f"[red]Error: Could not find dataset '{doi}'[/red]")
            console.print(f"[dim]{e}[/dim]")
            raise typer.Exit(1)

        progress.update(task, description=f"Exporting to HuggingFace Hub...")
        try:
            url = push_to_hub(dataset, repo, token=token, private=private)
        except Exception as e:
            console.print(f"[red]Error exporting to HuggingFace: {e}[/red]")
            raise typer.Exit(1)

    console.print(Panel(
        f"[green]Successfully exported to HuggingFace Hub![/green]\n\n"
        f"[bold]Dataset:[/bold] {dataset.dataset_name}\n"
        f"[bold]Repository:[/bold] {repo}\n"
        f"[bold]URL:[/bold] [link={url}]{url}[/link]",
        title="Export Complete",
    ))


# MCP subcommands
@mcp_app.command()
def start(
    host: str = typer.Option("localhost", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8765, "--port", "-p", help="Port to bind to"),
):
    """Start the MCP server for agent integration."""
    console.print(Panel(
        "[bold green]Starting Foundry MCP Server[/bold green]\n\n"
        f"Host: {host}\n"
        f"Port: {port}\n\n"
        "This server allows AI agents to discover and load materials science datasets.\n"
        "Connect using the Model Context Protocol.",
        title="MCP Server",
    ))

    try:
        from foundry.mcp.server import run_server
        run_server(host=host, port=port)
    except ImportError:
        console.print("[yellow]MCP server not yet implemented. Coming soon![/yellow]")
        raise typer.Exit(1)


@mcp_app.command()
def install():
    """Install Foundry as an MCP server in Claude Code."""
    console.print(Panel(
        "[bold]To install Foundry in Claude Code:[/bold]\n\n"
        "Add this to your Claude Code MCP configuration:\n\n"
        "[cyan]{\n"
        '  "mcpServers": {\n'
        '    "foundry": {\n'
        '      "command": "python",\n'
        '      "args": ["-m", "foundry", "mcp", "start"]\n'
        "    }\n"
        "  }\n"
        "}[/cyan]\n\n"
        "Then restart Claude Code.",
        title="MCP Installation",
    ))


@app.command()
def extract(
    paper_path: str = typer.Argument(..., help="Path to paper file (HTML or PDF)"),
    supplementary: Optional[list[str]] = typer.Option(None, "--supplementary", "-s", help="Supplementary data files"),
    output: str = typer.Option("extracted_dataset", "--output", "-o", help="Output directory"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="Anthropic API key for LLM description generation"),
    no_publish: bool = typer.Option(False, "--no-publish", help="Skip the publish prompt"),
    no_interactive: bool = typer.Option(False, "--no-interactive", "-y", help="Download all files without prompting"),
):
    """Extract a dataset from a scientific paper.

    Parses the paper, finds data links (Zenodo, GitHub, Figshare),
    downloads the data, and generates MDF-ready metadata.

    Features:
    - Shows file sizes before downloading
    - Lets you select which files to download
    - Progress bars for large downloads
    - Caches downloaded files

    Example:
        foundry extract paper.html --output my_dataset
        foundry extract paper.html -s data.csv -s extra.json
        foundry extract paper.html -y  # Download all without prompting
    """
    from pathlib import Path
    from foundry.agents import PaperExtractor

    paper = Path(paper_path)
    if not paper.exists():
        console.print(f"[red]Error: File not found: {paper_path}[/red]")
        raise typer.Exit(1)

    supp_paths = [Path(s) for s in (supplementary or [])]
    for s in supp_paths:
        if not s.exists():
            console.print(f"[red]Error: Supplementary file not found: {s}[/red]")
            raise typer.Exit(1)

    extractor = PaperExtractor(
        output_dir=Path(output),
        api_key=api_key,
    )

    try:
        result = extractor.extract(
            paper_path=paper,
            supplementary=supp_paths if supp_paths else None,
            interactive=not no_interactive,
        )
    except Exception as e:
        console.print(f"[red]Extraction failed: {e}[/red]")
        raise typer.Exit(1)

    # Show summary
    if result.errors:
        console.print(Panel(
            f"[yellow]Extraction completed with warnings:[/yellow]\n" +
            "\n".join(f"- {e}" for e in result.errors),
            title="Warnings",
        ))

    console.print(Panel(
        f"[green]Dataset extracted successfully![/green]\n\n"
        f"[bold]Title:[/bold] {result.paper.title}\n"
        f"[bold]Authors:[/bold] {', '.join(result.paper.authors[:3])}{'...' if len(result.paper.authors) > 3 else ''}\n"
        f"[bold]Files:[/bold] {len(result.data_files)}\n"
        f"[bold]Confidence:[/bold] {result.confidence*100:.0f}%\n"
        f"[bold]Output:[/bold] {result.output_dir}",
        title="Extraction Complete",
    ))

    if not no_publish:
        if typer.confirm("Publish to MDF?", default=False):
            console.print("[yellow]MDF publishing coming soon![/yellow]")


@app.command()
def publish(
    extraction_dir: str = typer.Argument(..., help="Path to extraction output directory"),
    source_name: Optional[str] = typer.Option(None, "--name", "-n", help="Short unique name for the dataset (e.g., 'compression_mlip_2025')"),
    test: bool = typer.Option(True, "--test/--production", help="Submit to test or production MDF"),
    update: Optional[str] = typer.Option(None, "--update", "-u", help="Source ID to update (for republishing)"),
):
    """Publish an extracted dataset to MDF.

    Takes the output from 'foundry extract' and submits it to the
    Materials Data Facility.

    Data is automatically staged to the MDF public endpoint before submission,
    so you don't need Globus Connect Personal running locally.

    Example:
        foundry publish ./extracted_dataset --name my_dataset_2025
        foundry publish ./extracted_dataset --name my_dataset --production
    """
    from pathlib import Path
    import yaml

    extraction_path = Path(extraction_dir)
    metadata_path = extraction_path / "mdf_metadata.yaml"
    data_dir = extraction_path / "data"

    # Validate extraction directory
    if not metadata_path.exists():
        console.print(f"[red]Error: No mdf_metadata.yaml found in {extraction_dir}[/red]")
        console.print("[dim]Run 'foundry extract' first to generate metadata.[/dim]")
        raise typer.Exit(1)

    if not data_dir.exists() or not any(data_dir.iterdir()):
        console.print(f"[red]Error: No data files found in {data_dir}[/red]")
        raise typer.Exit(1)

    # Load metadata
    with open(metadata_path) as f:
        meta = yaml.safe_load(f)

    # Count and size files
    data_files = list(data_dir.iterdir())
    data_files = [f for f in data_files if f.is_file()]
    total_size = sum(f.stat().st_size for f in data_files)
    size_str = f"{total_size / (1024*1024):.1f} MB" if total_size > 1024*1024 else f"{total_size / 1024:.1f} KB"

    console.print(Panel(
        f"[bold]Title:[/bold] {meta.get('title', 'N/A')}\n"
        f"[bold]Authors:[/bold] {', '.join(meta.get('authors', [])[:3])}{'...' if len(meta.get('authors', [])) > 3 else ''}\n"
        f"[bold]Files:[/bold] {len(data_files)} ({size_str})\n"
        f"[bold]License:[/bold] {meta.get('license', 'unknown')}",
        title="Dataset to Publish",
    ))

    # Get source name if not provided
    if not source_name:
        console.print("\n[bold]Enter a short unique name for this dataset[/bold]")
        console.print("[dim]Use lowercase, underscores, no spaces (e.g., 'bandgap_ml_2025')[/dim]")
        source_name = typer.prompt("Source name")

    # Validate source name
    import re
    if not re.match(r'^[a-z][a-z0-9_]*$', source_name):
        console.print("[red]Error: Source name must be lowercase, start with a letter, and contain only letters, numbers, and underscores[/red]")
        raise typer.Exit(1)

    # Confirm submission
    env = "TEST" if test else "PRODUCTION"
    if not typer.confirm(f"\nSubmit to MDF ({env})?", default=True):
        console.print("[yellow]Cancelled[/yellow]")
        raise typer.Exit(0)

    # Submit to MDF
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Authenticating with Globus...", total=None)

        try:
            # Use Foundry's auth flow which handles Globus login
            f = get_foundry(no_browser=False)

            # Stage data to MDF public endpoint
            progress.update(task, description="Creating staging directory...")

            from foundry.mdf_client import StagingUploader, STAGING_ENDPOINT_ID

            # Get transfer token from Foundry's auth
            transfer_client = f.auths.get("transfer")
            if hasattr(transfer_client, "authorizer") and hasattr(transfer_client.authorizer, "access_token"):
                transfer_token = transfer_client.authorizer.access_token
            else:
                raise RuntimeError("Could not get transfer token from Foundry auth")

            # Get NCSA HTTPS token for file uploads (different from transfer token)
            ncsa_https_scope = "https://auth.globus.org/scopes/82f1b5c6-6e9b-11e5-ba47-22000b92c6ec/https"
            ncsa_auth = f.auths.get(ncsa_https_scope)
            if ncsa_auth and hasattr(ncsa_auth, "access_token"):
                https_token = ncsa_auth.access_token
            elif hasattr(ncsa_auth, "authorizer") and hasattr(ncsa_auth.authorizer, "access_token"):
                https_token = ncsa_auth.authorizer.access_token
            else:
                # Fallback to transfer token (may not work)
                console.print("[yellow]Warning: NCSA HTTPS token not found, using transfer token[/yellow]")
                https_token = transfer_token

            uploader = StagingUploader(transfer_token, https_token=https_token)
            unique_id, remote_dir = uploader.create_staging_directory()

            console.print(f"  [dim]Staging directory: {remote_dir}[/dim]")

            # Upload files with progress
            progress.update(task, description=f"Uploading {len(data_files)} files to staging...")

            for i, file_path in enumerate(data_files, 1):
                progress.update(task, description=f"Uploading [{i}/{len(data_files)}] {file_path.name}...")
                uploader.upload_file(file_path, remote_dir)

            console.print(f"  [dim]Uploaded {len(data_files)} files[/dim]")

            # Get the authenticated connect client from Foundry
            progress.update(task, description="Creating dataset record...")

            from mdf_connect_client import MDFConnectClient
            client = MDFConnectClient(
                authorizer=f.auths["mdf_connect"],
                test=test
            )

            # Create DC block (Dublin Core metadata)
            client.create_dc_block(
                title=meta.get('title', 'Untitled Dataset'),
                authors=meta.get('authors', ['Unknown']),
                affiliations=[],  # TODO: Extract from paper
                publisher="Materials Data Facility",
                publication_year=2025,
                resource_type="Dataset",
            )

            # Add description
            if meta.get('description'):
                client.dc['descriptions'] = [{
                    'description': meta['description'],
                    'descriptionType': 'Abstract'
                }]

            # Add source DOI as related identifier
            if meta.get('source_doi'):
                client.dc['relatedIdentifiers'] = [{
                    'relatedIdentifier': meta['source_doi'],
                    'relatedIdentifierType': 'DOI',
                    'relationType': 'IsSupplementTo'
                }]

            # Set source name
            client.set_source_name(source_name)

            # Add staged data as data source (using Globus file manager URL format)
            progress.update(task, description="Configuring data source...")
            globus_url = uploader.get_globus_url(remote_dir)
            client.add_data_source(globus_url)

            # Set organization
            client.set_organization(meta.get('organization', 'MDF Open'))

            # Update existing or submit new
            progress.update(task, description="Submitting to MDF...")
            if update:
                result = client.submit_dataset(update=update)
            else:
                result = client.submit_dataset()

            progress.update(task, description="Done!")

        except ImportError as e:
            if "mdf_connect_client" in str(e):
                console.print("[red]Error: mdf_connect_client not installed[/red]")
                console.print("Install with: [cyan]pip install mdf_connect_client[/cyan]")
            else:
                console.print(f"[red]Import error: {e}[/red]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Error submitting to MDF: {e}[/red]")
            raise typer.Exit(1)

    # Show result
    if result.get('success'):
        source_id = result.get('source_id', 'unknown')
        console.print(Panel(
            f"[green]Successfully submitted to MDF![/green]\n\n"
            f"[bold]Source ID:[/bold] {source_id}\n"
            f"[bold]Environment:[/bold] {env}\n"
            f"[bold]Staged at:[/bold] {remote_dir}\n\n"
            f"[dim]Check status with: foundry status {source_id}[/dim]",
            title="Submission Complete",
        ))
    else:
        console.print(Panel(
            f"[yellow]Submission returned:[/yellow]\n{result}",
            title="MDF Response",
        ))


@app.command()
def version():
    """Show Foundry version."""
    try:
        from importlib.metadata import version as get_version
        v = get_version("foundry_ml")
    except Exception:
        v = "unknown"
    console.print(f"foundry-ml version {v}")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
