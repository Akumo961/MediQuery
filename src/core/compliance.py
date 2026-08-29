"""Compliance-readiness controls; these are not certifications."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ComplianceControl:
    control_id: str
    area: str
    required_evidence: str
    external_owner: str


CONTROLS = (
    ComplianceControl(
        "PRIV-01",
        "privacy",
        "data map and retention policy",
        "privacy/legal",
    ),
    ComplianceControl(
        "SEC-01",
        "security",
        "independent assessment and remediation record",
        "security",
    ),
    ComplianceControl(
        "AI-01",
        "medical AI safety",
        "evaluation set, safety tests, and review record",
        "AI/clinical",
    ),
    ComplianceControl(
        "IP-01",
        "intellectual property",
        "contributor and dependency licence inventory",
        "legal",
    ),
    ComplianceControl(
        "OPS-01",
        "operations",
        "backup/restore and incident-response evidence",
        "operations",
    ),
    ComplianceControl(
        "PROD-01",
        "production",
        "deployment configuration and environment evidence",
        "engineering",
    ),
)


def required_control_ids() -> tuple[str, ...]:
    """Return stable control identifiers for diligence checklists and release gates."""
    return tuple(control.control_id for control in CONTROLS)


def validate_evidence_map(evidence: dict[str, str]) -> None:
    """Require evidence references without claiming that evidence itself is certification."""
    missing = [
        control.control_id
        for control in CONTROLS
        if not evidence.get(control.control_id, "").strip()
    ]
    if missing:
        raise ValueError(
            "Compliance-readiness evidence missing: " + ", ".join(missing)
        )
