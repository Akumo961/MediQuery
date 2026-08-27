"""Data ingestion helpers for external medical literature and local images."""

from functools import lru_cache
import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

PUBMED_CACHE_TTL_SECONDS = 300
PUBMED_CACHE_SIZE = 128


class MedicalDataLoader:
    """Load raw medical data from APIs and local directories."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def fetch_pubmed_papers(self, query: str, max_results: int = 100) -> list[dict]:
        """Fetch PubMed papers with a bounded five-minute in-process cache."""
        normalized_query = " ".join(query.split())
        if not normalized_query:
            return []
        max_results = min(max(int(max_results), 1), 100)
        bucket = int(time.time() // PUBMED_CACHE_TTL_SECONDS)
        papers = _fetch_pubmed_cached(normalized_query, max_results, bucket)
        return [dict(paper) for paper in papers]

    def _fetch_pubmed_papers_uncached(
        self, query: str, max_results: int = 100
    ) -> list[dict]:
        """Fetch and persist a PubMed response; failures return an empty result."""
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
        }
        try:
            response = requests.get(search_url, params=search_params, timeout=15)
            response.raise_for_status()
            paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
            if not paper_ids:
                return []

            fetch_url = f"{base_url}efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(paper_ids),
                "retmode": "xml",
            }
            papers_response = requests.get(fetch_url, params=fetch_params, timeout=30)
            papers_response.raise_for_status()
            papers = self._parse_pubmed_xml(papers_response.text)
            safe_query = re.sub(r"[^A-Za-z0-9_.-]+", "_", query).strip("_") or "query"
            output_file = self.raw_dir / f"pubmed_{safe_query}.json"
            with open(output_file, "w") as file:
                json.dump(papers, file, indent=2)
            return papers
        except Exception as exc:
            logger.error("Error fetching PubMed papers: %s", exc)
            return []

    def _parse_pubmed_xml(self, xml_content: str) -> list[dict]:
        """Parse the PubMed efetch XML fields used by search responses."""
        papers = []
        root = ET.fromstring(xml_content)
        for article in root.findall(".//PubmedArticle"):
            medline = article.find("MedlineCitation")
            article_node = medline.find("Article") if medline is not None else None
            if article_node is None:
                continue
            title = "".join(article_node.findtext("ArticleTitle", default="").split())
            abstract_parts = [
                "".join(part.itertext()).strip()
                for part in article_node.findall(".//AbstractText")
            ]
            authors = []
            for author in article_node.findall(".//Author"):
                last_name = author.findtext("LastName", default="")
                initials = author.findtext("Initials", default="")
                full_name = " ".join(part for part in [last_name, initials] if part)
                if full_name:
                    authors.append(full_name)
            journal = article_node.findtext(".//Journal/Title", default="Unknown")
            year = article_node.findtext(".//PubDate/Year", default="Unknown")
            papers.append(
                {
                    "title": title or "Unknown Title",
                    "abstract": " ".join(abstract_parts) or "No abstract available",
                    "authors": authors,
                    "journal": journal,
                    "year": year,
                }
            )
        return papers

    def load_medical_images(self, image_dir: str) -> list[dict]:
        """Discover supported medical image files in a local directory."""
        image_extensions = [".jpg", ".jpeg", ".png", ".dcm", ".nii"]
        images = []
        image_path = Path(image_dir)
        if not image_path.exists():
            return images
        for ext in image_extensions:
            for img_file in image_path.glob(f"*{ext}"):
                images.append(
                    {
                        "path": str(img_file),
                        "filename": img_file.name,
                        "size": img_file.stat().st_size,
                        "type": ext[1:],
                    }
                )
        return images


@lru_cache(maxsize=PUBMED_CACHE_SIZE)
def _fetch_pubmed_cached(query: str, max_results: int, bucket: int) -> tuple[dict, ...]:
    """Cache PubMed responses for one bounded five-minute time bucket."""
    loader = MedicalDataLoader()
    return tuple(loader._fetch_pubmed_papers_uncached(query, max_results))
