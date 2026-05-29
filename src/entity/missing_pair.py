"""Ordered missing-number pair from a puzzle grid."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MissingPair:
    """Two missing values with ``m1 < m2``.

    Attributes:
        m1: Smaller missing value.
        m2: Larger missing value.
    """

    m1: int
    m2: int

    def __post_init__(self) -> None:
        """Enforce ascending order."""
        if self.m1 >= self.m2:
            msg = "m1 must be less than m2"
            raise ValueError(msg)
