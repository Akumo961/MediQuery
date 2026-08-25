"""Search endpoints for medical literature discovery."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from data_loader import MedicalDataLoader

router = APIRouter()


class SearchQuery(BaseModel):
    """Request body for literature search."""

    query: str = Field(..., min_length=1)
    max_results: int = Field(10, ge=1, le=50)
    search_type: str = Field("semantic", pattern="^(semantic|keyword|hybrid)$")


class SearchResult(BaseModel):
    """Normalized literature search result returned to clients."""

    title: str
    content: str
    similarity: float
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


@router.post("/literature", response_model=List[SearchResult])
async def search_literature(search_query: SearchQuery):
    """Search PubMed and rank papers by semantic or keyword relevance."""
    try:
        papers = MedicalDataLoader().fetch_pubmed_papers(
            search_query.query,
            search_query.max_results
        )

        if not papers:
            return []

        documents = [f"{paper.get('title', '')} {paper.get('abstract', '')}" for paper in papers]

        if search_query.search_type in {"semantic", "hybrid"}:
            # Optional legacy dependency: import only when semantic search is requested.
            from models.text_models import MedicalTextModel
            similar_docs = MedicalTextModel().find_similar_documents(
                search_query.query,
                documents,
                top_k=search_query.max_results
            )

            results = []
            for doc_info in similar_docs:
                paper = papers[doc_info["index"]]
                results.append(SearchResult(
                    title=paper.get("title", "Unknown Title"),
                    content=paper.get("abstract", "No abstract available"),
                    similarity=doc_info["similarity"],
                    source="PubMed",
                    metadata={
                        "authors": paper.get("authors", []),
                        "journal": paper.get("journal", "Unknown"),
                        "year": paper.get("year", "Unknown")
                    }
                ))

            return results
        results = []
        query_terms = set(search_query.query.lower().split())
        for paper in papers[:search_query.max_results]:
            haystack = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
            overlap = sum(1 for term in query_terms if term in haystack)
            similarity = overlap / max(len(query_terms), 1)
            results.append(SearchResult(
                title=paper.get("title", "Unknown Title"),
                content=paper.get("abstract", "No abstract available"),
                similarity=similarity,
                source="PubMed",
                metadata={
                    "authors": paper.get("authors", []),
                    "journal": paper.get("journal", "Unknown"),
                    "year": paper.get("year", "Unknown")
                }
            ))
        return results

    except Exception:
        raise HTTPException(status_code=502, detail="Literature search is temporarily unavailable")


@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(..., description="Partial query")):
    """Return static medical-search suggestions filtered by a partial query."""
    suggestions = [
        "COVID-19 treatment protocols",
        "Machine learning in radiology",
        "Cancer immunotherapy research",
        "Diabetes management guidelines",
        "Cardiovascular disease prevention"
    ]

    # Filter suggestions based on query
    filtered = [s for s in suggestions if q.lower() in s.lower()]
    return {"suggestions": filtered[:5]}
