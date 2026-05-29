"""Finds missing numbers in a partially filled puzzle grid."""

from __future__ import annotations

from entity.cell_value_constants import CELL_MAX, CELL_MIN
from entity.domain_error_codes import INVALID_MISSING_COUNT
from entity.errors import DomainError
from entity.grid import Grid
from entity.grid_size import GRID_DIMENSION
from entity.missing_pair import MissingPair

_REQUIRED_MISSING_COUNT = 2


class MissingNumberFinder:
    """Derives the two absent values from ``{CELL_MIN..CELL_MAX}``."""

    def find(self, grid: Grid) -> MissingPair:
        """Return sorted missing values for a puzzle grid.

        Args:
            grid: Partially filled puzzle ``Grid``.

        Returns:
            ``MissingPair`` with ``m1 < m2``.

        Raises:
            DomainError: When exactly two values are not missing.
        """
        present = {
            grid.cell(row, col)
            for row in range(GRID_DIMENSION)
            for col in range(GRID_DIMENSION)
            if grid.cell(row, col) != 0
        }
        missing = [
            value
            for value in range(CELL_MIN, CELL_MAX + 1)
            if value not in present
        ]
        if len(missing) != _REQUIRED_MISSING_COUNT:
            raise DomainError(
                code=INVALID_MISSING_COUNT,
                message="Grid must have exactly two missing numbers.",
            )
        return MissingPair(m1=missing[0], m2=missing[1])
