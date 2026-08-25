"""Safe, deterministic PDF validation, extraction, and lab-value candidate parsing."""

from dataclasses import dataclass
from io import BytesIO
import re
from pathlib import Path
from pypdf import PdfReader


PDF_MAGIC = b"%PDF-"
MAX_EVIDENCE_CHARS = 500
LAB_PATTERN = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9 /()'\-]{1,80}?)\s*[:\t]+\s*"
    r"(?P<value>[<>]?\s*\d+(?:\.\d+)?)\s*"
    r"(?P<unit>[A-Za-zµμ/%^0-9.\-/]+)?\s*"
    r"(?:\(?\s*(?P<range>\d+(?:\.\d+)?\s*(?:-|–|to)\s*\d+(?:\.\d+)?|[<>]\s*\d+(?:\.\d+)?)\s*\)?)?\s*"
    r"(?P<flag>H|L|High|Low|Normal)?\b",
    re.IGNORECASE,
)


class ReportValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ExtractedFinding:
    name: str
    value: str
    unit: str | None
    reference_range: str | None
    flag: str
    page: int
    evidence: str


@dataclass(frozen=True)
class ExtractionResult:
    page_count: int
    findings: list[ExtractedFinding]
    note: str | None


def validate_pdf(
    filename: str | None, content_type: str | None, raw: bytes, max_bytes: int
) -> None:
    """Validate a bounded, real PDF before parsing. MIME is advisory, magic bytes are decisive."""
    if not filename or Path(filename).suffix.lower() != ".pdf":
        raise ReportValidationError("Only PDF reports are supported")
    if content_type and content_type not in {
        "application/pdf",
        "application/octet-stream",
    }:
        raise ReportValidationError("The uploaded file must have PDF content")
    if not raw:
        raise ReportValidationError("The uploaded file is empty")
    if len(raw) > max_bytes:
        raise ReportValidationError("The uploaded report exceeds the allowed size")
    if not raw.startswith(PDF_MAGIC):
        raise ReportValidationError("The uploaded file is not a valid PDF")


def extract_report(raw: bytes, max_pages: int) -> ExtractionResult:
    try:
        reader = PdfReader(BytesIO(raw), strict=False)
    except Exception as exc:
        raise ReportValidationError("The PDF could not be read") from exc
    if reader.is_encrypted:
        raise ReportValidationError("Password-protected PDFs are not supported")
    if len(reader.pages) > max_pages:
        raise ReportValidationError("The report has too many pages")

    findings: list[ExtractedFinding] = []
    extracted_any_text = False
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            extracted_any_text = True
            findings.extend(parse_findings(text, page_number))

    note = None
    if not extracted_any_text:
        note = "No selectable text was found. This may be a scanned report; OCR is not yet enabled."
    elif not findings:
        note = "Text was extracted, but no lab-value candidates could be safely identified. Review the original report."
    return ExtractionResult(page_count=len(reader.pages), findings=findings, note=note)


def parse_findings(text: str, page: int) -> list[ExtractedFinding]:
    """Extract conservative lab candidates; never infer a clinical result from missing fields."""
    findings: list[ExtractedFinding] = []
    seen: set[tuple[str, str, str | None]] = set()
    for line in text.splitlines():
        normalized = " ".join(line.split())
        if len(normalized) < 4 or len(normalized) > MAX_EVIDENCE_CHARS:
            continue
        match = LAB_PATTERN.search(normalized)
        if not match:
            continue
        name = match.group("name").strip(" :-")
        value = re.sub(r"\s+", "", match.group("value"))
        unit = (match.group("unit") or "").strip() or None
        reference_range = (match.group("range") or "").strip() or None
        if len(name) < 2 or name.lower() in {"page", "date", "patient", "result"}:
            continue
        key = (name.lower(), value, unit)
        if key in seen:
            continue
        seen.add(key)
        raw_flag = (match.group("flag") or "").lower()
        flag = {
            "h": "high",
            "high": "high",
            "l": "low",
            "low": "low",
            "normal": "normal",
        }.get(raw_flag, "unknown")
        findings.append(
            ExtractedFinding(name, value, unit, reference_range, flag, page, normalized)
        )
    return findings[:200]
