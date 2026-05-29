"""Boundary failure payload type."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErrorResponse:
    """Structured error returned by Boundary on contract violation.

    Attributes:
        code: Machine-readable error code (e.g. ``INVALID_SIZE``).
        message: Human-readable explanation matching PRD §8.1 wording.
    """

    code: str
    message: str
