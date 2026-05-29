"""Six-element solution vector for puzzle output."""

from __future__ import annotations

from dataclasses import dataclass

from entity.cell_value_constants import CELL_MAX, CELL_MIN
from entity.grid_size import GRID_DIMENSION


@dataclass(frozen=True, slots=True)
class SolutionVector:
    """Contract output ``[r1,c1,n1,r2,c2,n2]`` with 1-index coordinates.

    Attributes:
        r1: First blank row (1-index).
        c1: First blank column (1-index).
        n1: Value placed at first blank.
        r2: Second blank row (1-index).
        c2: Second blank column (1-index).
        n2: Value placed at second blank.
    """

    r1: int
    c1: int
    n1: int
    r2: int
    c2: int
    n2: int

    def __post_init__(self) -> None:
        """Validate coordinate and value ranges."""
        for row, col in ((self.r1, self.c1), (self.r2, self.c2)):
            if not 1 <= row <= GRID_DIMENSION:
                msg = f"row must be between 1 and {GRID_DIMENSION}"
                raise ValueError(msg)
            if not 1 <= col <= GRID_DIMENSION:
                msg = f"col must be between 1 and {GRID_DIMENSION}"
                raise ValueError(msg)
        for value in (self.n1, self.n2):
            if not CELL_MIN <= value <= CELL_MAX:
                msg = f"value must be between {CELL_MIN} and {CELL_MAX}"
                raise ValueError(msg)

    def to_array(self) -> list[int]:
        """Return the contract ``int[6]`` representation."""
        return [self.r1, self.c1, self.n1, self.r2, self.c2, self.n2]
