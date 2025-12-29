"""HTML paper parser.

Extracts structured information from HTML versions of scientific papers.
Works with common formats: PubMed Central, arXiv HTML, journal sites.
"""

import re
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup

from ..models import ParsedPaper


def parse_html(file_path: Path) -> ParsedPaper:
    """Parse an HTML file and extract paper metadata.

    Args:
        file_path: Path to HTML file

    Returns:
        ParsedPaper with extracted metadata
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    title = _extract_title(soup)
    authors = _extract_authors(soup)
    abstract = _extract_abstract(soup)
    doi = _extract_doi(soup, content)
    data_availability = _extract_data_availability(soup)
    supplementary_urls = _extract_data_urls(soup, content)
    license_info = _extract_license(soup)

    return ParsedPaper(
        title=title,
        authors=authors,
        abstract=abstract,
        doi=doi,
        data_availability=data_availability,
        supplementary_urls=supplementary_urls,
        license=license_info,
    )


def _extract_title(soup: BeautifulSoup) -> str:
    """Extract paper title."""
    # Try common title locations
    selectors = [
        'h1.title',
        'h1.article-title',
        'h1[class*="title"]',
        '.article-title',
        'meta[name="citation_title"]',
        'meta[property="og:title"]',
        'title',
    ]

    for selector in selectors:
        if selector.startswith('meta'):
            elem = soup.select_one(selector)
            if elem and elem.get('content'):
                return elem['content'].strip()
        else:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()

    return "Unknown Title"


def _extract_authors(soup: BeautifulSoup) -> list[str]:
    """Extract author names."""
    authors = []

    # Try meta tags first (works for most journals and arXiv)
    meta_authors = soup.select('meta[name="citation_author"]')
    if meta_authors:
        for meta in meta_authors:
            if meta.get('content'):
                authors.append(meta['content'].strip())
        if authors:
            return authors

    # arXiv-specific: look for ltx_authors
    arxiv_authors = soup.select('.ltx_authors .ltx_personname')
    if arxiv_authors:
        for elem in arxiv_authors:
            # Remove superscripts, footnotes, and affiliation text before extracting author name
            elem_copy = BeautifulSoup(str(elem), 'html.parser')
            for sup in elem_copy.select('sup'):
                sup.decompose()
            for note in elem_copy.select('.ltx_note'):
                note.decompose()
            # Remove inline affiliations (often in small font after <br/>)
            for br in elem_copy.select('br'):
                # Remove everything after the first <br> (usually affiliations)
                for sibling in list(br.next_siblings):
                    if hasattr(sibling, 'decompose'):
                        sibling.decompose()
                br.decompose()

            name = elem_copy.get_text().strip()
            name = re.sub(r'\s+', ' ', name)
            if name and len(name) > 2:
                authors.append(name)
        if authors:
            return authors[:20]

    # Try common author selectors
    selectors = [
        '.author-name',
        '.contrib-author',
        '.author',
    ]

    for selector in selectors:
        elems = soup.select(selector)
        if elems:
            for elem in elems:
                name = elem.get_text().strip()
                # Clean up common artifacts
                name = re.sub(r'\s+', ' ', name)
                name = re.sub(r'[\d,*†‡§]', '', name).strip()
                if name and len(name) > 2 and len(name) < 100:  # Reasonable name length
                    authors.append(name)
            if authors:
                return authors[:20]  # Cap at 20 authors

    return ["Unknown Author"]


def _extract_abstract(soup: BeautifulSoup) -> str:
    """Extract paper abstract."""
    selectors = [
        'section.abstract p',
        '.abstract p',
        '#abstract p',
        'div[class*="abstract"] p',
        'meta[name="description"]',
        'meta[property="og:description"]',
    ]

    for selector in selectors:
        if selector.startswith('meta'):
            elem = soup.select_one(selector)
            if elem and elem.get('content'):
                return elem['content'].strip()
        else:
            elems = soup.select(selector)
            if elems:
                text = ' '.join(e.get_text().strip() for e in elems)
                if len(text) > 100:  # Probably a real abstract
                    return text

    return ""


def _extract_doi(soup: BeautifulSoup, content: str) -> Optional[str]:
    """Extract DOI."""
    # Try meta tag
    meta = soup.select_one('meta[name="citation_doi"]')
    if meta and meta.get('content'):
        return meta['content'].strip()

    # Try regex in content
    doi_pattern = r'10\.\d{4,}/[^\s<>"\']+(?<![.,;])'
    match = re.search(doi_pattern, content)
    if match:
        return match.group(0)

    return None


def _extract_data_availability(soup: BeautifulSoup) -> Optional[str]:
    """Extract data availability statement."""
    # Look for data availability section
    selectors = [
        '#data-availability',
        '.data-availability',
        'section[id*="data"]',
        'h2:-soup-contains("Data Availability")',
        'h3:-soup-contains("Data Availability")',
    ]

    for selector in selectors:
        try:
            elem = soup.select_one(selector)
            if elem:
                # Get the section content
                if elem.name in ['h2', 'h3']:
                    # Get following paragraphs
                    paragraphs = []
                    for sibling in elem.find_next_siblings():
                        if sibling.name in ['h2', 'h3']:
                            break
                        if sibling.name == 'p':
                            paragraphs.append(sibling.get_text().strip())
                    return ' '.join(paragraphs)
                else:
                    return elem.get_text().strip()
        except Exception:
            continue

    # Fallback: search for keywords
    text = soup.get_text().lower()
    if 'data availability' in text or 'data and code availability' in text:
        # Try to find the section by searching paragraphs
        for p in soup.find_all('p'):
            p_text = p.get_text().lower()
            if 'data' in p_text and ('available' in p_text or 'repository' in p_text):
                return p.get_text().strip()

    return None


def _extract_data_urls(soup: BeautifulSoup, content: str) -> list[str]:
    """Extract URLs that likely point to data."""
    urls = []

    # Patterns for data repositories
    patterns = [
        r'https?://github\.com/[\w-]+/[\w.-]+',
        r'https?://zenodo\.org/record[s]?/\d+',
        r'https?://figshare\.com/[\w/.-]+',
        r'https?://osf\.io/[\w]+',
        r'https?://datadryad\.org/[\w/.-]+',
        r'https?://data\.mendeley\.com/[\w/.-]+',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        urls.extend(matches)

    # Extract Zenodo DOIs (format: 10.5281/zenodo.XXXXX)
    zenodo_doi_pattern = r'10\.5281/zenodo\.(\d+)'
    zenodo_matches = re.findall(zenodo_doi_pattern, content)
    for record_id in zenodo_matches:
        urls.append(f'https://zenodo.org/records/{record_id}')

    # Also check href attributes
    for a in soup.find_all('a', href=True):
        href = a['href']
        for pattern in patterns:
            if re.match(pattern, href):
                urls.append(href)

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        # Normalize zenodo URLs
        url = re.sub(r'zenodo\.org/record/', 'zenodo.org/records/', url)
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls


def _extract_license(soup: BeautifulSoup) -> Optional[str]:
    """Extract license information."""
    # Check meta tags
    meta = soup.select_one('meta[name="DC.rights"]')
    if meta and meta.get('content'):
        return meta['content'].strip()

    # Look for license links/text
    license_patterns = [
        r'CC[\s-]BY[\s-]?\d?\.?\d?',
        r'Creative Commons',
        r'MIT License',
        r'Apache[\s-]2\.0',
        r'GPL',
    ]

    text = soup.get_text()
    for pattern in license_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None
