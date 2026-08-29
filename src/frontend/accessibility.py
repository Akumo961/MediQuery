"""Small, testable accessibility contracts for the commercial UI surface."""

REQUIRED_INTERACTIVE_FIELDS = ("label", "name", "description")


def validate_interactive_metadata(metadata: dict[str, str]) -> None:
    """Require accessible names and descriptions for generated UI controls."""
    missing = [
        field
        for field in REQUIRED_INTERACTIVE_FIELDS
        if not metadata.get(field, "").strip()
    ]
    if missing:
        raise ValueError(
            "Accessible interactive control metadata missing: " + ", ".join(missing)
        )


def validate_status_message(message: str, role: str = "status") -> None:
    """Validate non-empty user-facing status text and an appropriate ARIA role."""
    if not message.strip():
        raise ValueError("Status message must not be empty")
    if role not in {"status", "alert"}:
        raise ValueError("Status messages must use role='status' or role='alert'")
