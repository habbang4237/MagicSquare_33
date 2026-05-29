"""D-T05 — MissingNumberFinder Domain RED skeleton (no mocks)."""

from __future__ import annotations

import pytest

from entity.grid import Grid
from entity.missing_number_finder import MissingNumberFinder

# I-D10: MissingPair always two values with m1 < m2.


@pytest.mark.unit
class TestDt05MissingPairRed:
    """D-T05, I-D10 — missing numbers from 14 filled cells (skeleton)."""

    def test_d_t05_fourteen_filled_cells_returns_ordered_missing_pair(
        self,
    ) -> None:
        """D-T05 — 14-cell fixture → (m1, m2) with m1 < m2."""
        # Given — 4×4 puzzle grid with exactly two missing values in [1,16]
        # grid = Grid.of(...)  # TODO: lock literals per Report/02
        # finder = MissingNumberFinder()
        # When
        # pair = finder.find(grid)
        # Then — m1 < m2, fixed expected pair per fixture
        pytest.fail("RED: D-T05 — 14칸 픽스처 → MissingPair m1<m2")
