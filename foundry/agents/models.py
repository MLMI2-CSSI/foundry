"""Data models for the extraction pipeline."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ParsedPaper:
    """Extracted information from a scientific paper."""
    title: str
    authors: list[str]
    abstract: str
    doi: Optional[str] = None
    data_availability: Optional[str] = None
    supplementary_urls: list[str] = field(default_factory=list)
    license: Optional[str] = None


@dataclass
class DataSource:
    """A discovered data source from the paper."""
    url: str
    source_type: str  # 'github', 'zenodo', 'figshare', etc.
    confidence: float  # 0.0 to 1.0
    description: Optional[str] = None


@dataclass
class DataFile:
    """A downloaded data file."""
    path: Path
    original_url: str
    format: str  # 'csv', 'json', 'hdf5', etc.
    size_bytes: int


@dataclass
class MDFPackage:
    """MDF-ready metadata package."""
    title: str
    authors: list[str]
    description: str
    data_files: list[Path]
    license: str = "unknown"
    source_doi: Optional[str] = None
    organization: str = "MDF Open"


@dataclass
class ExtractionResult:
    """Complete result from extraction pipeline."""
    paper: ParsedPaper
    data_files: list[DataFile]
    profile: Optional[dict]  # Data profile/statistics
    mdf_package: Optional[MDFPackage]
    output_dir: Path
    confidence: float
    errors: list[str] = field(default_factory=list)
