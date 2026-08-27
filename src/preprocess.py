import logging
from typing import Any, Dict, List

import cv2
import numpy as np
import torch
from PIL import Image
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)


class MedicalPreprocessor:
    """Preprocessing pipeline for medical text and images."""

    def __init__(self):
        self.text_encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.bio_tokenizer = AutoTokenizer.from_pretrained(
            "dmis-lab/biobert-base-cased-v1.1"
        )

    def preprocess_text(self, texts: List[str]) -> Dict[str, Any]:
        """Preprocess medical texts for embedding."""
        processed_texts = []
        embeddings = []
        for text in texts:
            cleaned_text = self._clean_medical_text(text)
            processed_texts.append(cleaned_text)
            embedding = self.text_encoder.encode(cleaned_text)
            embeddings.append(embedding)
        return {
            "processed_texts": processed_texts,
            "embeddings": np.array(embeddings),
            "original_texts": texts,
        }

    def _clean_medical_text(self, text: str) -> str:
        """Clean medical text data."""
        text = " ".join(text.split())
        abbreviations = {
            "pt": "patient",
            "dx": "diagnosis",
            "tx": "treatment",
            "hx": "history",
        }
        for abbr, full in abbreviations.items():
            text = text.replace(f" {abbr} ", f" {full} ")
        return text

    def preprocess_medical_image(self, image_path: str) -> Dict[str, Any]:
        """Preprocess medical images."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(image_rgb, (224, 224))
            normalized = resized / 255.0
            tensor_image = torch.from_numpy(normalized).float().permute(2, 0, 1)
            return {
                "original_shape": image.shape,
                "processed_image": tensor_image,
                "path": image_path,
            }
        except Exception as exc:
            logger.error("Error preprocessing image %s: %s", image_path, exc)
            return {}
