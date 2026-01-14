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
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

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
        except Exception:
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

        progress.update(task, description="Exporting to HuggingFace Hub...")
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
