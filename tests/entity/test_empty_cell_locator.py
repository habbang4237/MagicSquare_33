"""D-T03, D-T10, D-T11 — EmptyCellLocator Domain RED skeleton (no mocks)."""

from __future__ import annotations

import pytest

from entity.empty_cell_locator import EmptyCellLocator
from entity.errors import DomainError
from entity.grid import Grid

# Domain Track: no unittest.mock — real Grid / EmptyCellLocator instances only.


@pytest.mark.unit
class TestDt03RowMajorBlanksRed:
    """D-T03, AC-FR02-1 — row-major empty slot order (skeleton)."""

    def test_d_t03_row_major_blanks_returns_slots_two_three_and_three_one(
        self,
    ) -> None:
        """D-T03, I-D8, I-D11 — fixture row_major_blanks → (2,3), (3,1) 1-index."""
        # Given — fixture: row_major_blanks (1st blank (2,3), 2nd (3,1))
        # grid = Grid.of(...)  # TODO: lock 16 integers per Report/02
        # locator = EmptyCellLocator()
        # When
        # pair = locator.locate(grid)
        # Then — first slot (2,3), second (3,1)
        pytest.fail("RED: D-T03 — row_major_blanks → (2,3), (3,1)")


@pytest.mark.unit
class TestDt10Dt11InvalidEmptyCountRed:
    """D-T10, D-T11, I-D8 — invalid empty-cell count (skeleton)."""

    def test_d_t10_one_empty_cell_raises_invalid_empty_count(self) -> None:
        """D-T10 — exactly one zero → DomainError INVALID_EMPTY_COUNT."""
        # Given — 4×4 grid, count(0)==1
        # grid = Grid.of(...)
        # locator = EmptyCellLocator()
        # When / Then — pytest.raises(DomainError) INVALID_EMPTY_COUNT
        pytest.fail("RED: D-T10 — 빈칸 1개 → INVALID_EMPTY_COUNT")

    def test_d_t11_three_empty_cells_raises_invalid_empty_count(self) -> None:
        """D-T11 — three zeros → DomainError INVALID_EMPTY_COUNT."""
        # Given — 4×4 grid, count(0)==3
        # grid = Grid.of(...)
        # locator = EmptyCellLocator()
        # When / Then — pytest.raises(DomainError) INVALID_EMPTY_COUNT
        pytest.fail("RED: D-T11 — 빈칸 3개 → INVALID_EMPTY_COUNT")
