"""Data ingestion helpers for external medical literature and local images."""

import os
import json
import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import re
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class MedicalDataLoader:
    """Load raw medical data from APIs and local directories."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"

        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def fetch_pubmed_papers(self, query: str, max_results: int = 100) -> List[Dict]:
        """Fetch PubMed papers and cache the parsed response under data/raw."""
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

        # Search for paper IDs
        search_url = f"{base_url}esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }

        try:
            response = requests.get(search_url, params=search_params, timeout=15)
            response.raise_for_status()
            search_data = response.json()

            paper_ids = search_data.get("esearchresult", {}).get("idlist", [])

            if not paper_ids:
                return []

            # Fetch paper details
            fetch_url = f"{base_url}efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(paper_ids),
                "retmode": "xml"
            }

            papers_response = requests.get(fetch_url, params=fetch_params, timeout=30)
            papers_response.raise_for_status()

            # Parse XML and extract relevant information
            papers = self._parse_pubmed_xml(papers_response.text)

            # Save to file
            safe_query = re.sub(r"[^A-Za-z0-9_.-]+", "_", query).strip("_") or "query"
            output_file = self.raw_dir / f"pubmed_{safe_query}.json"
            with open(output_file, 'w') as f:
                json.dump(papers, f, indent=2)

            return papers

        except Exception as e:
            logger.error(f"Error fetching PubMed papers: {e}")
            return []

    def _parse_pubmed_xml(self, xml_content: str) -> List[Dict]:
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
            papers.append({
                "title": title or "Unknown Title",
                "abstract": " ".join(abstract_parts) or "No abstract available",
                "authors": authors,
                "journal": journal,
                "year": year,
            })

        return papers

    def load_medical_images(self, image_dir: str) -> List[Dict]:
        """Discover supported medical image files in a local directory."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.dcm', '.nii']
        images = []

        image_path = Path(image_dir)
        if not image_path.exists():
            return images

        for ext in image_extensions:
            for img_file in image_path.glob(f"*{ext}"):
                images.append({
                    "path": str(img_file),
                    "filename": img_file.name,
                    "size": img_file.stat().st_size,
                    "type": ext[1:]  # Remove dot
                })

        return images
