"""Machine-readable final release evidence contract for buyer handoff."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseManifest:
    commit: str
    tests: str
    quality: str
    phase_gates: tuple[str, ...]
    medical_safety_boundary: str
    external_diligence_required: bool = True

    def validate(self) -> None:
        """Fail closed when the release evidence is incomplete or unsafe."""
        if len(self.commit) < 7:
            raise ValueError("Release commit must identify the exact revision")
        if self.tests.lower() != "pass" or self.quality.lower() != "pass":
            raise ValueError("Release tests and quality checks must pass")
        required = {"17", "18", "19", "20", "21", "22", "23", "24"}
        if not required.issubset(set(self.phase_gates)):
            raise ValueError("All completed phase gates 17-24 must be represented")
        if "not a diagnostic service" not in self.medical_safety_boundary.lower():
            raise ValueError("Medical safety boundary must remain explicit")
        if not self.external_diligence_required:
            raise ValueError(
                "External diligence cannot be represented as complete by code alone"
            )


def release_is_candidate(manifest: ReleaseManifest) -> bool:
    """Return True only when the final repository evidence contract is satisfied."""
    try:
        manifest.validate()
    except ValueError:
        return False
    return True
