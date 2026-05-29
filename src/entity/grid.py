"""4×4 puzzle grid entity."""

from __future__ import annotations

from dataclasses import dataclass

from entity.domain_error_codes import INVALID_GRID_SIZE
from entity.errors import DomainError
from entity.grid_size import GRID_DIMENSION


@dataclass(frozen=True, slots=True)
class Grid:
    """Immutable 4×4 cell snapshot.

    Attributes:
        _cells: Nested tuple of cell values (0-index rows and columns).
    """

    _cells: tuple[tuple[int, ...], ...]

    @classmethod
    def of(cls, raw: list[list[int]]) -> Grid:
        """Create a grid from a raw 4×4 array.

        Args:
            raw: ``int[4][4]`` cell values.

        Returns:
            Immutable ``Grid`` instance.

        Raises:
            DomainError: When the array is not 4×4.
        """
        if len(raw) != GRID_DIMENSION:
            raise DomainError(
                code=INVALID_GRID_SIZE,
                message="Grid must be 4x4.",
            )
        cells: list[tuple[int, ...]] = []
        for row in raw:
            if not isinstance(row, list) or len(row) != GRID_DIMENSION:
                raise DomainError(
                    code=INVALID_GRID_SIZE,
                    message="Grid must be 4x4.",
                )
            cells.append(tuple(row))
        return cls(_cells=tuple(cells))

    def cell(self, row: int, col: int) -> int:
        """Return cell value at 0-index coordinates.

        Args:
            row: Zero-based row index.
            col: Zero-based column index.

        Returns:
            Cell integer value.
        """
        return self._cells[row][col]

    def with_cell(self, row: int, col: int, value: int) -> Grid:
        """Return a copy with one cell replaced.

        Args:
            row: Zero-based row index.
            col: Zero-based column index.
            value: New cell value.

        Returns:
            New ``Grid`` with the updated cell.
        """
        rows: list[list[int]] = [list(r) for r in self._cells]
        rows[row][col] = value
        return Grid.of(rows)

    def rows(self) -> tuple[tuple[int, ...], ...]:
        """Return all rows as an immutable nested tuple."""
        return self._cells
