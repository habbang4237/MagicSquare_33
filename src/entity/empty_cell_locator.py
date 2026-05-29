"""Locates empty cells in row-major order."""

from __future__ import annotations

from entity.cell_position import CellPosition
from entity.domain_error_codes import INVALID_EMPTY_COUNT
from entity.empty_slot_pair import EmptySlotPair
from entity.errors import DomainError
from entity.grid import Grid
from entity.grid_size import GRID_DIMENSION

_REQUIRED_EMPTY_COUNT = 2


class EmptyCellLocator:
    """Finds the first two ``0`` cells in row-major scan order."""

    def locate(self, grid: Grid) -> EmptySlotPair:
        """Return ordered empty-slot coordinates for a puzzle grid.

        Args:
            grid: Puzzle ``Grid`` with exactly two empty cells.

        Returns:
            ``EmptySlotPair`` with 1-index positions.

        Raises:
            DomainError: When empty-cell count is not two.
        """
        blanks: list[CellPosition] = []
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                if grid.cell(row, col) == 0:
                    blanks.append(CellPosition(row=row + 1, col=col + 1))
        if len(blanks) != _REQUIRED_EMPTY_COUNT:
            raise DomainError(
                code=INVALID_EMPTY_COUNT,
                message="Grid must contain exactly 2 empty cells.",
            )
        return EmptySlotPair(first=blanks[0], second=blanks[1])
