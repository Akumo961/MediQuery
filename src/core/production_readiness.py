"""Production deployment contracts that fail closed without external infrastructure claims."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionRequirements:
    """Deployment evidence required before enabling real sensitive-data processing."""

    database_url: str
    jwt_secret: str
    cors_origins: tuple[str, ...]
    object_storage: bool
    secret_manager: bool
    tls: bool
    waf: bool
    malware_scanning: bool
    backups_restore_tested: bool
    asynchronous_processing: bool

    def validate(self) -> None:
        """Reject an incomplete production contract instead of silently downgrading."""
        if self.database_url.startswith("sqlite"):
            raise ValueError(
                "Production requires managed PostgreSQL or an equivalent managed database"
            )
        if len(self.jwt_secret) < 32:
            raise ValueError("Production JWT secret must contain at least 32 characters")
        if not self.cors_origins or any(
            not origin.startswith("https://") for origin in self.cors_origins
        ):
            raise ValueError("Production CORS origins must use HTTPS")
        missing = [
            name
            for name, enabled in (
                ("private object storage", self.object_storage),
                ("secret manager", self.secret_manager),
                ("TLS", self.tls),
                ("WAF", self.waf),
                ("malware scanning", self.malware_scanning),
                ("backup/restore testing", self.backups_restore_tested),
                ("asynchronous processing", self.asynchronous_processing),
            )
            if not enabled
        ]
        if missing:
            raise ValueError("Production controls missing: " + ", ".join(missing))


def production_contract_is_complete(requirements: ProductionRequirements) -> bool:
    """Return True only when every mandatory production control validates."""
    try:
        requirements.validate()
    except ValueError:
        return False
    return True
