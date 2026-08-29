"""Deterministic evaluation utilities for extraction and retrieval quality."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ExpectedFinding:
    name: str
    value: str
    unit: str | None = None


@dataclass(frozen=True)
class EvaluationResult:
    expected: int
    matched: int
    precision: float
    recall: float


def evaluate_findings(
    actual: Iterable[ExpectedFinding], expected: Iterable[ExpectedFinding]
) -> EvaluationResult:
    """Compare normalized finding triples without making clinical accuracy claims."""
    actual_set = {_key(item) for item in actual}
    expected_set = {_key(item) for item in expected}
    matched = len(actual_set & expected_set)
    precision = matched / len(actual_set) if actual_set else 1.0 if not expected_set else 0.0
    recall = matched / len(expected_set) if expected_set else 1.0
    return EvaluationResult(
        expected=len(expected_set),
        matched=matched,
        precision=precision,
        recall=recall,
    )


def retrieval_grounding_coverage(source_ids: Iterable[str], cited_ids: Iterable[str]) -> float:
    """Measure citation coverage for retrieved source identifiers."""
    sources = {value for value in source_ids if value}
    cited = {value for value in cited_ids if value}
    if not sources:
        return 1.0
    return len(sources & cited) / len(sources)


def _key(finding: ExpectedFinding) -> tuple[str, str, str]:
    return (
        finding.name.strip().casefold(),
        finding.value.strip().casefold(),
        (finding.unit or "").strip().casefold(),
    )
