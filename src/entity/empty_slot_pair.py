"""Row-major ordered empty-cell slot pair."""

from __future__ import annotations

from dataclasses import dataclass

from entity.cell_position import CellPosition


@dataclass(frozen=True, slots=True)
class EmptySlotPair:
    """First and second empty slots found in row-major order.

    Attributes:
        first: First ``0`` cell (1-index).
        second: Second ``0`` cell (1-index).
    """

    first: CellPosition
    second: CellPosition
