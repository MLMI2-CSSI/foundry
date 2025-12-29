"""Main paper extraction orchestrator.

Coordinates the full pipeline from paper to MDF/Foundry dataset.
"""

from pathlib import Path
from typing import Optional

from .models import ParsedPaper, DataSource, DataFile, MDFPackage, ExtractionResult
from .parsers import parse_html
from .fetchers import fetch_data
from .generators import create_mdf_package


class PaperExtractor:
    """Orchestrates the paper-to-dataset extraction pipeline."""

    def __init__(self, output_dir: Optional[Path] = None, api_key: Optional[str] = None):
        """Initialize the extractor.

        Args:
            output_dir: Directory for extracted datasets (default: ./extracted_dataset)
            api_key: Anthropic API key for LLM features
        """
        self.output_dir = output_dir or Path("./extracted_dataset")
        self.api_key = api_key

    def extract(
        self,
        paper_path: Path,
        supplementary: Optional[list[Path]] = None,
        mdf_only: bool = False,
        interactive: bool = True,
    ) -> ExtractionResult:
        """Extract a dataset from a paper.

        Args:
            paper_path: Path to HTML or PDF paper file
            supplementary: Optional list of supplementary data files
            mdf_only: If True, only generate MDF package (skip Foundry schema)
            interactive: If True, prompt user to select files (default True)

        Returns:
            ExtractionResult with extracted data and metadata
        """
        errors = []

        # Step 1: Parse paper
        print(f"Parsing paper: {paper_path.name}...")
        paper = self._parse_paper(paper_path)
        print(f"  Title: {paper.title}")
        print(f"  Authors: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")

        # Step 2: Discover data sources
        print("\nSearching for data links...")
        sources = self._discover_sources(paper)
        if sources:
            for i, src in enumerate(sources, 1):
                print(f"  [{i}] {src.url} (confidence: {src.confidence:.2f})")
        else:
            print("  No data links found in paper")

        # Add supplementary files as sources
        # If supplementary files are provided, use ONLY those (skip slow remote fetching)
        if supplementary:
            print("\nUsing provided supplementary files (skipping remote sources)...")
            sources = []  # Clear remote sources
            for path in supplementary:
                sources.append(DataSource(
                    url=str(path),
                    source_type="supplementary",
                    confidence=1.0,
                    description="User-provided supplementary file",
                ))

        if not sources:
            errors.append("No data sources found")
            return ExtractionResult(
                paper=paper,
                data_files=[],
                profile=None,
                mdf_package=None,
                output_dir=self.output_dir,
                confidence=0.0,
                errors=errors,
            )

        # Step 3: Fetch data
        print("\nDownloading data...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        data_dir = self.output_dir / "data"
        data_dir.mkdir(exist_ok=True)

        data_files = fetch_data(sources, data_dir, interactive=interactive)

        if not data_files:
            errors.append("Failed to download any data files")
            return ExtractionResult(
                paper=paper,
                data_files=[],
                profile=None,
                mdf_package=None,
                output_dir=self.output_dir,
                confidence=0.0,
                errors=errors,
            )

        total_size = sum(f.size_bytes for f in data_files) / (1024 * 1024)
        print(f"  Downloaded {len(data_files)} files ({total_size:.1f} MB)")

        # Step 4: Create MDF package
        print("\nGenerating MDF package...")
        mdf_package = create_mdf_package(
            paper=paper,
            data_files=data_files,
            output_dir=self.output_dir,
            api_key=self.api_key,
        )
        print("  Done")

        # Calculate confidence
        confidence = self._calculate_confidence(paper, data_files, sources)

        return ExtractionResult(
            paper=paper,
            data_files=data_files,
            profile=None,  # TODO: Add data profiling
            mdf_package=mdf_package,
            output_dir=self.output_dir,
            confidence=confidence,
            errors=errors,
        )

    def _parse_paper(self, paper_path: Path) -> ParsedPaper:
        """Parse a paper file."""
        suffix = paper_path.suffix.lower()

        if suffix in ['.html', '.htm']:
            return parse_html(paper_path)
        elif suffix == '.pdf':
            # TODO: Implement PDF parsing
            raise NotImplementedError("PDF parsing not yet implemented. Please use HTML.")
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def _discover_sources(self, paper: ParsedPaper) -> list[DataSource]:
        """Discover data sources from parsed paper."""
        sources = []

        for url in paper.supplementary_urls:
            source_type = self._classify_url(url)
            confidence = self._estimate_confidence(url, source_type)

            sources.append(DataSource(
                url=url,
                source_type=source_type,
                confidence=confidence,
            ))

        # Sort by confidence
        sources.sort(key=lambda s: s.confidence, reverse=True)
        return sources

    def _classify_url(self, url: str) -> str:
        """Classify a URL by repository type."""
        url_lower = url.lower()

        if 'github.com' in url_lower:
            return 'github'
        elif 'zenodo.org' in url_lower:
            return 'zenodo'
        elif 'figshare.com' in url_lower:
            return 'figshare'
        elif 'osf.io' in url_lower:
            return 'osf'
        elif 'dryad' in url_lower:
            return 'dryad'
        else:
            return 'unknown'

    def _estimate_confidence(self, url: str, source_type: str) -> float:
        """Estimate confidence that URL contains useful data."""
        base_confidence = {
            'zenodo': 0.95,  # Highest - dedicated data repository
            'figshare': 0.90,
            'dryad': 0.90,
            'osf': 0.85,
            'github': 0.60,  # Lower - often code, not data
            'unknown': 0.50,
        }

        confidence = base_confidence.get(source_type, 0.50)

        url_lower = url.lower()

        # Boost for data-specific patterns
        if any(ext in url_lower for ext in ['.csv', '.json', '.xlsx', '.hdf5']):
            confidence = min(confidence + 0.15, 1.0)
        if 'data' in url_lower or 'dataset' in url_lower:
            confidence = min(confidence + 0.10, 1.0)

        # Penalize GitHub repos that look like code/tools
        if source_type == 'github':
            # Common code/tool patterns
            code_patterns = ['sdk', 'api', 'client', 'lib', 'tool', 'package', 'framework']
            if any(p in url_lower for p in code_patterns):
                confidence = max(confidence - 0.20, 0.30)
            # SevenNet, QUESTS etc are ML packages, not data
            if any(p in url_lower for p in ['sevennet', 'quests', 'nequip', 'mace']):
                confidence = max(confidence - 0.30, 0.20)

        return confidence

    def _calculate_confidence(
        self,
        paper: ParsedPaper,
        data_files: list[DataFile],
        sources: list[DataSource],
    ) -> float:
        """Calculate overall extraction confidence."""
        scores = []

        # Metadata completeness
        if paper.title and paper.title != "Unknown Title":
            scores.append(1.0)
        else:
            scores.append(0.3)

        if paper.authors and paper.authors[0] != "Unknown Author":
            scores.append(1.0)
        else:
            scores.append(0.3)

        if paper.abstract and len(paper.abstract) > 100:
            scores.append(1.0)
        else:
            scores.append(0.5)

        # Data quality
        if data_files:
            scores.append(0.9)
            # Bonus for recognized formats
            known_formats = {'csv', 'json', 'excel', 'hdf5', 'parquet'}
            if any(f.format in known_formats for f in data_files):
                scores.append(1.0)
        else:
            scores.append(0.0)

        # Source confidence
        if sources:
            scores.append(max(s.confidence for s in sources))

        return sum(scores) / len(scores) if scores else 0.0
