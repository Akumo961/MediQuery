"""Legacy document-processing endpoints retained for compatibility."""

import PyPDF2
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from models.text_models import MedicalTextModel

router = APIRouter()
text_model = MedicalTextModel()


class DocumentAnalysis(BaseModel):
    """Summary and metadata returned after PDF upload."""

    filename: str
    content_preview: str
    summary: str
    key_findings: list[str]
    metadata: dict


class QuestionAnswer(BaseModel):
    """Answer payload for document question-answering."""

    question: str
    answer: str
    confidence: float
    context: str


@router.post("/upload", response_model=DocumentAnalysis)
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, extract text, summarize it, and surface key findings."""
    try:
        if not (file.filename or "").lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        content = ""
        pdf_reader = PyPDF2.PdfReader(file.file)
        for page in pdf_reader.pages:
            content += page.extract_text() or ""

        if not content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        summary = text_model.summarize_text(content)
        sentences = content.split(".")
        keywords = ["result", "conclusion", "finding", "significant"]
        key_findings = [
            sentence.strip()
            for sentence in sentences
            if any(keyword in sentence.lower() for keyword in keywords)
        ][:3]

        return DocumentAnalysis(
            filename=file.filename or "report.pdf",
            content_preview=content[:500] + "..." if len(content) > 500 else content,
            summary=summary,
            key_findings=key_findings,
            metadata={
                "pages": len(pdf_reader.pages),
                "word_count": len(content.split()),
                "char_count": len(content),
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Document analysis failed") from exc


@router.post("/question-answering", response_model=QuestionAnswer)
async def document_question_answering(
    file: UploadFile = File(...), question: str = Form(...)
):
    """Answer a question using text extracted from an uploaded PDF."""
    try:
        content = ""
        pdf_reader = PyPDF2.PdfReader(file.file)
        for page in pdf_reader.pages:
            content += page.extract_text() or ""

        if not content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        result = text_model.answer_question(question, content)
        start_idx = max(0, result.get("start", 0) - 200)
        end_idx = min(len(content), result.get("end", 0) + 200)

        return QuestionAnswer(
            question=question,
            answer=result["answer"],
            confidence=result["confidence"],
            context=content[start_idx:end_idx],
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Document QA failed") from exc


@router.get("/supported-types")
async def get_supported_document_types():
    """List supported document formats and processing features."""
    return {
        "supported_formats": [".pdf"],
        "max_file_size": "25MB",
        "features": [
            "text_extraction",
            "summarization",
            "question_answering",
            "key_findings",
        ],
    }
