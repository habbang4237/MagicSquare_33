"""D-T05 — MissingNumberFinder Domain RED skeleton (no mocks)."""

from __future__ import annotations

import pytest

from entity.grid import Grid
from entity.missing_number_finder import MissingNumberFinder
from entity.missing_pair import MissingPair

# Report/02·D-T03 anchor — 14 filled cells, missing 7 and 10
PUZZLE_GRID_D_T05 = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# I-D10: MissingPair always two values with m1 < m2.


@pytest.mark.unit
class TestDt05MissingPairRed:
    """D-T05, I-D10 — missing numbers from 14 filled cells (skeleton)."""

    def test_d_t05_fourteen_filled_cells_returns_ordered_missing_pair(
        self,
    ) -> None:
        """D-T05 — 14-cell fixture → (m1, m2) with m1 < m2."""
        # Given
        grid = Grid.of(PUZZLE_GRID_D_T05)
        finder = MissingNumberFinder()

        # When
        pair = finder.find(grid)

        # Then
        assert pair == MissingPair(m1=7, m2=10)
