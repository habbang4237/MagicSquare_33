"""1-index cell position value object."""

from __future__ import annotations

from dataclasses import dataclass

from entity.grid_size import GRID_DIMENSION


@dataclass(frozen=True, slots=True)
class CellPosition:
    """Immutable 1-index grid coordinate.

    Attributes:
        row: Row index in ``1..GRID_DIMENSION``.
        col: Column index in ``1..GRID_DIMENSION``.
    """

    row: int
    col: int

    def __post_init__(self) -> None:
        """Validate 1-index bounds."""
        if not 1 <= self.row <= GRID_DIMENSION:
            msg = f"row must be between 1 and {GRID_DIMENSION}"
            raise ValueError(msg)
        if not 1 <= self.col <= GRID_DIMENSION:
            msg = f"col must be between 1 and {GRID_DIMENSION}"
            raise ValueError(msg)
