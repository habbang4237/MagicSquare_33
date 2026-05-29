"""Control-layer failure payload for Boundary error mapping."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UseCaseError:
    """Domain failure surfaced by Control without leaking ``DomainError``.

    Attributes:
        code: Domain error code (e.g. ``NO_VALID_COMPLETION``).
    """

    code: str
