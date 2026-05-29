"""Domain-level error types."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    """Represents a domain rule violation.

    Attributes:
        code: Machine-readable error code (e.g. ``INVALID_USER_ID``).
        message: Human-readable explanation of the failure.
    """

    code: str
    message: str

    def __str__(self) -> str:
        """Return ``code: message`` representation."""
        return f"{self.code}: {self.message}"
