"""Embedding utilities for semantic search experiments and API helpers."""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Owns sentence-transformer embedding generation and FAISS lookup."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.embeddings = None

    def create_embeddings(self, documents: List[str]) -> np.ndarray:
        """Encode raw document strings into dense vectors."""
        embeddings = self.model.encode(documents)
        return embeddings

    def build_index(self, documents: List[str], save_path: Optional[str] = None):
        """Build a normalized FAISS index for fast cosine-style search."""
        self.documents = documents
        self.embeddings = self.create_embeddings(documents)

        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product for cosine similarity

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings.astype('float32'))

        if save_path:
            self.save_index(save_path)

        logger.info(f"Built index with {len(documents)} documents")

    def search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """Search the built index and return ranked document matches."""
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")

        # Encode query
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)

        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), k)

        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if 0 <= idx < len(self.documents):
                results.append({
                    "document": self.documents[idx],
                    "score": float(score),
                    "rank": i + 1,
                    "index": int(idx)
                })

        return results

    def save_index(self, path: str):
        """Persist FAISS index and metadata sidecar files."""
        faiss.write_index(self.index, f"{path}.index")

        metadata = {
            "documents": self.documents,
            "embeddings": self.embeddings.tolist()
        }

        with open(f"{path}.metadata", 'wb') as f:
            pickle.dump(metadata, f)

    def load_index(self, path: str):
        """Load FAISS index and metadata sidecar files."""
        self.index = faiss.read_index(f"{path}.index")

        with open(f"{path}.metadata", 'rb') as f:
            metadata = pickle.load(f)

        self.documents = metadata["documents"]
        self.embeddings = np.array(metadata["embeddings"])
