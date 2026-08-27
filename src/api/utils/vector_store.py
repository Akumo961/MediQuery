"""Persistent FAISS-backed vector storage for medical document metadata."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import faiss
import numpy as np

logger = logging.getLogger(__name__)


class VectorStore:
    """Small vector database wrapper used by the API search layer."""

    def __init__(self, storage_path: str = "data/processed/vector_store"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index = None
        self.documents_metadata = []
        self.dimension = 384

    def initialize_index(self, dimension: int = 384):
        """Initialize an inner-product index for normalized embeddings."""
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        logger.info("Initialized FAISS index with dimension %s", dimension)

    def add_documents(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """Add document embeddings and parallel metadata rows to the store."""
        if self.index is None:
            self.initialize_index(embeddings.shape[1])
        normalized_embeddings = embeddings.copy().astype("float32")
        faiss.normalize_L2(normalized_embeddings)
        self.index.add(normalized_embeddings)
        self.documents_metadata.extend(metadata)
        logger.info("Added %s documents to vector store", len(embeddings))

    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[Dict[str, Any]]:
        """Return the top-k metadata rows closest to a query embedding."""
        if self.index is None:
            return []
        query_normalized = query_embedding.copy().astype("float32")
        if len(query_normalized.shape) == 1:
            query_normalized = query_normalized.reshape(1, -1)
        faiss.normalize_L2(query_normalized)
        scores, indices = self.index.search(query_normalized, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self.documents_metadata):
                result = self.documents_metadata[idx].copy()
                result["similarity_score"] = float(score)
                results.append(result)
        return results

    def save(self):
        """Save the FAISS index, document metadata, and lightweight config."""
        if self.index is not None:
            faiss.write_index(self.index, str(self.storage_path / "index.faiss"))
            with open(self.storage_path / "metadata.json", "w") as f:
                json.dump(self.documents_metadata, f, indent=2)
            config = {
                "dimension": self.dimension,
                "total_documents": len(self.documents_metadata),
            }
            with open(self.storage_path / "config.json", "w") as f:
                json.dump(config, f, indent=2)
            logger.info(
                "Saved vector store with %s documents", len(self.documents_metadata)
            )

    def load(self):
        """Load a previously saved vector store from disk."""
        try:
            with open(self.storage_path / "config.json") as f:
                config = json.load(f)
            self.dimension = config["dimension"]
            self.index = faiss.read_index(str(self.storage_path / "index.faiss"))
            with open(self.storage_path / "metadata.json") as f:
                self.documents_metadata = json.load(f)
            logger.info(
                "Loaded vector store with %s documents", len(self.documents_metadata)
            )
            return True
        except Exception as exc:
            logger.error("Failed to load vector store: %s", exc)
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Expose operational stats for health checks and diagnostics."""
        return {
            "total_documents": len(self.documents_metadata),
            "dimension": self.dimension,
            "index_size": self.index.ntotal if self.index else 0,
            "storage_path": str(self.storage_path),
        }
