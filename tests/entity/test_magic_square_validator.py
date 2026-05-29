"""D-T04, D-T04-R/C/D — MagicSquareValidator Domain RED skeleton (no mocks)."""

from __future__ import annotations

import pytest

from entity.grid import Grid
from entity.magic_square_validator import MagicSquareValidator

# I-D4~I-D7: row, column, diagonal sums equal MagicConstant.M.


@pytest.mark.unit
class TestDt04ValidGridRed:
    """D-T04, I-D2~I-D7 — complete valid magic square (skeleton)."""

    def test_d_t04_complete_valid_grid_is_valid_true(self) -> None:
        """D-T04 — known complete 4×4 magic square → is_valid True."""
        # Given — complete valid 16-cell grid
        # grid = Grid.of(...)  # TODO: lock literals per Report/02
        # validator = MagicSquareValidator()
        # When
        # result = validator.is_valid(grid)
        # Then — result is True
        pytest.fail("RED: D-T04 — 완성 유효 격자 → is_valid True")


@pytest.mark.unit
class TestDt04RowColDiagonalRed:
    """D-T04-R/C/D — line-sum violations return false (skeleton)."""

    def test_d_t04_r_broken_row_sum_is_valid_false(self) -> None:
        """D-T04-R, I-D4 — at least one row sum ≠ M → is_valid False."""
        # Given — complete grid with one row sum broken
        # grid = Grid.of(...)
        # validator = MagicSquareValidator()
        # When
        # result = validator.is_valid(grid)
        # Then — result is False
        pytest.fail("RED: D-T04-R — 행 합 깨짐 → is_valid False")

    def test_d_t04_c_broken_column_sum_is_valid_false(self) -> None:
        """D-T04-C, I-D5 — at least one column sum ≠ M → is_valid False."""
        # Given — complete grid with one column sum broken
        pytest.fail("RED: D-T04-C — 열 합 깨짐 → is_valid False")

    def test_d_t04_d_broken_diagonal_sum_is_valid_false(self) -> None:
        """D-T04-D, I-D6~I-D7 — diagonal sum ≠ M → is_valid False."""
        # Given — complete grid with main or anti-diagonal broken
        pytest.fail("RED: D-T04-D — 대각 합 깨짐 → is_valid False")
