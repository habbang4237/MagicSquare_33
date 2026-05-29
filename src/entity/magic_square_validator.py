"""Validates complete 4×4 magic squares."""

from __future__ import annotations

from entity.cell_value_constants import CELL_MAX, CELL_MIN
from entity.grid import Grid
from entity.grid_size import GRID_DIMENSION
from entity.magic_constant import MagicConstant


class MagicSquareValidator:
    """Checks I-D2~I-D7 for a fully filled grid."""

    def is_valid(self, grid: Grid) -> bool:
        """Return whether ``grid`` is a complete valid magic square.

        Args:
            grid: Fully filled ``Grid`` with values in ``CELL_MIN..CELL_MAX``.

        Returns:
            ``True`` when all domain invariants hold; otherwise ``False``.
        """
        values: list[int] = []
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                value = grid.cell(row, col)
                if value < CELL_MIN or value > CELL_MAX:
                    return False
                values.append(value)
        if len(set(values)) != GRID_DIMENSION * GRID_DIMENSION:
            return False
        target = MagicConstant.M
        for row in range(GRID_DIMENSION):
            if sum(grid.cell(row, col) for col in range(GRID_DIMENSION)) != target:
                return False
        for col in range(GRID_DIMENSION):
            if sum(grid.cell(row, col) for row in range(GRID_DIMENSION)) != target:
                return False
        main_diag = sum(grid.cell(i, i) for i in range(GRID_DIMENSION))
        anti_diag = sum(
            grid.cell(i, GRID_DIMENSION - 1 - i) for i in range(GRID_DIMENSION)
        )
        return main_diag == target and anti_diag == target
