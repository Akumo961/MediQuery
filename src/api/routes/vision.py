"""Image-analysis endpoints for uploaded medical images."""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import sys
from pathlib import Path
import shutil
from uuid import uuid4

sys.path.append(str(Path(__file__).parent.parent.parent))

from models.vision_models import MedicalVisionModel

router = APIRouter()

vision_model = MedicalVisionModel()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}


class VisionAnalysisResult(BaseModel):
    """Response schema for image-analysis requests."""

    analysis_type: str
    result: Dict[str, Any]
    image_path: str


def _save_upload(file: UploadFile) -> Path:
    """Persist an uploaded image with a safe generated filename."""
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    file_path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


@router.post("/analyze", response_model=VisionAnalysisResult)
async def analyze_medical_image(
        file: UploadFile = File(...),
        analysis_type: str = Form("classification")  # classification, vqa, anomaly
):
    """Analyze an uploaded image for modality classification or anomalies."""
    try:
        file_path = _save_upload(file)

        if analysis_type == "classification":
            result = vision_model.classify_medical_image(str(file_path))
        elif analysis_type == "anomaly":
            result = vision_model.detect_anomalies(str(file_path))
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")

        return VisionAnalysisResult(
            analysis_type=analysis_type,
            result=result,
            image_path=str(file_path)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/question-answering")
async def visual_question_answering(
        file: UploadFile = File(...),
        question: str = Form(...)
):
    """Answer a natural-language question about an uploaded medical image."""
    try:
        file_path = _save_upload(file)

        result = vision_model.answer_visual_question(str(file_path), question)

        return {
            "question": question,
            "answer": result["answer"],
            "confidence": result["confidence"],
            "image_path": str(file_path)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VQA failed: {str(e)}")


@router.get("/supported-formats")
async def get_supported_formats():
    """List supported upload formats and image-analysis modes."""
    return {
        "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
        "max_file_size": "10MB",
        "analysis_types": ["classification", "anomaly_detection", "visual_qa"]
    }
