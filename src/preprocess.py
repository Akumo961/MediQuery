import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch
from PIL import Image
import cv2
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class MedicalPreprocessor:
    """Preprocessing pipeline for medical text and images"""

    def __init__(self):
        # Load medical domain models
        self.text_encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.bio_tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')

    def preprocess_text(self, texts: List[str]) -> Dict[str, Any]:
        """Preprocess medical texts for embedding"""
        processed_texts = []
        embeddings = []

        for text in texts:
            # Clean text
            cleaned_text = self._clean_medical_text(text)
            processed_texts.append(cleaned_text)

            # Generate embeddings
            embedding = self.text_encoder.encode(cleaned_text)
            embeddings.append(embedding)

        return {
            "processed_texts": processed_texts,
            "embeddings": np.array(embeddings),
            "original_texts": texts
        }

    def _clean_medical_text(self, text: str) -> str:
        """Clean medical text data"""
        # Remove extra whitespace
        text = ' '.join(text.split())

        # Handle medical abbreviations (basic example)
        abbreviations = {
            'pt': 'patient',
            'dx': 'diagnosis',
            'tx': 'treatment',
            'hx': 'history'
        }

        for abbr, full in abbreviations.items():
            text = text.replace(f' {abbr} ', f' {full} ')

        return text

    def preprocess_medical_image(self, image_path: str) -> Dict[str, Any]:
        """Preprocess medical images"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")

            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Resize for model input
            resized = cv2.resize(image_rgb, (224, 224))

            # Normalize
            normalized = resized / 255.0

            # Convert to tensor format
            tensor_image = torch.from_numpy(normalized).float().permute(2, 0, 1)

            return {
                "original_shape": image.shape,
                "processed_image": tensor_image,
                "path": image_path
            }

        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            return {}