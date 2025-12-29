"""MDF package generator."""

import os
from pathlib import Path
from typing import Optional

import yaml

from ..models import ParsedPaper, DataFile, MDFPackage


def create_mdf_package(
    paper: ParsedPaper,
    data_files: list[DataFile],
    output_dir: Path,
    api_key: Optional[str] = None,
) -> MDFPackage:
    """Create an MDF-ready package from extracted data.

    Args:
        paper: Parsed paper metadata
        data_files: List of downloaded data files
        output_dir: Output directory
        api_key: Optional Anthropic API key for LLM description generation

    Returns:
        MDFPackage with all metadata
    """
    # Generate description
    description = _generate_description(paper, data_files, api_key)

    # Create package
    package = MDFPackage(
        title=paper.title,
        authors=paper.authors,
        description=description,
        data_files=[f.path for f in data_files],
        license=paper.license or "unknown",
        source_doi=paper.doi,
    )

    # Write metadata file
    _write_metadata(package, output_dir)

    # Write extraction report
    _write_report(paper, data_files, package, output_dir)

    return package


def _generate_description(
    paper: ParsedPaper,
    data_files: list[DataFile],
    api_key: Optional[str] = None,
) -> str:
    """Generate a description for the dataset.

    Uses LLM if API key provided, otherwise generates from abstract.
    """
    if api_key:
        return _generate_description_llm(paper, data_files, api_key)
    else:
        return _generate_description_simple(paper, data_files)


def _generate_description_simple(paper: ParsedPaper, data_files: list[DataFile]) -> str:
    """Generate a simple description from paper metadata."""
    # Start with abstract or title-based description
    if paper.abstract:
        # Take first 2-3 sentences of abstract
        sentences = paper.abstract.split('. ')
        intro = '. '.join(sentences[:3]) + '.'
    else:
        intro = f"Dataset associated with the paper: {paper.title}."

    # Add file information
    file_types = list(set(f.format for f in data_files))
    file_info = f"Contains {len(data_files)} data file(s) in {', '.join(file_types)} format(s)."

    return f"{intro} {file_info}"


def _generate_description_llm(
    paper: ParsedPaper,
    data_files: list[DataFile],
    api_key: str,
) -> str:
    """Generate a description using Claude."""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        # Build context
        file_info = "\n".join([
            f"- {f.path.name} ({f.format}, {f.size_bytes/1024:.1f} KB)"
            for f in data_files
        ])

        prompt = f"""Based on this paper's abstract and data files, write a 2-3 sentence description suitable for a dataset catalog entry.

Paper Title: {paper.title}

Abstract:
{paper.abstract[:1500]}

Data Files:
{file_info}

Write a clear, informative description that:
1. Explains what data the dataset contains
2. Mentions the source/methodology if relevant
3. Suggests potential use cases

Keep it concise (2-3 sentences, ~100 words max). Do not include phrases like "This dataset..." at the start - dive right into the content."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text.strip()

    except Exception as e:
        print(f"  LLM description generation failed: {e}")
        return _generate_description_simple(paper, data_files)


def _write_metadata(package: MDFPackage, output_dir: Path) -> None:
    """Write MDF metadata to YAML file."""
    metadata = {
        'title': package.title,
        'authors': package.authors,
        'description': package.description,
        'data_files': [f.name for f in package.data_files],
        'license': package.license,
        'source_doi': package.source_doi,
        'organization': package.organization,
    }

    metadata_path = output_dir / 'mdf_metadata.yaml'
    with open(metadata_path, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)


def _write_report(
    paper: ParsedPaper,
    data_files: list[DataFile],
    package: MDFPackage,
    output_dir: Path,
) -> None:
    """Write an extraction report."""
    from datetime import datetime

    report = f"""# Extraction Report

**Source paper**: {paper.title}
**Paper DOI**: {paper.doi or 'Not found'}
**Extraction date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Output type**: MDF

## Authors Extracted

{chr(10).join('- ' + a for a in paper.authors)}

## Data Files Extracted

| File | Size | Source |
|------|------|--------|
"""

    for f in data_files:
        size_kb = f.size_bytes / 1024
        if size_kb > 1024:
            size_str = f"{size_kb/1024:.1f} MB"
        else:
            size_str = f"{size_kb:.1f} KB"
        source = f.original_url[:50] + "..." if len(f.original_url) > 50 else f.original_url
        report += f"| {f.path.name} | {size_str} | {source} |\n"

    report += f"""

## Data Availability Statement

{paper.data_availability or 'Not found in paper'}

## License

{package.license or 'Unknown - please verify before use'}
"""

    report_path = output_dir / 'extraction_report.md'
    with open(report_path, 'w') as f:
        f.write(report)
