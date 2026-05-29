"""Solves 2-blank magic square puzzles via attempt A/B."""

from __future__ import annotations

from entity.domain_error_codes import NO_VALID_COMPLETION
from entity.empty_cell_locator import EmptyCellLocator
from entity.errors import DomainError
from entity.grid import Grid
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solution_vector import SolutionVector


class PuzzleSolver:
    """Applies UC-D4: attempt A then attempt B."""

    def __init__(self) -> None:
        """Initialize domain collaborators."""
        self._locator = EmptyCellLocator()
        self._finder = MissingNumberFinder()
        self._validator = MagicSquareValidator()

    def solve(self, grid: Grid) -> SolutionVector:
        """Return the contract solution for a valid puzzle grid.

        Args:
            grid: Puzzle ``Grid`` with exactly two empty cells.

        Returns:
            ``SolutionVector`` for the first successful attempt (A before B).

        Raises:
            DomainError: When neither attempt yields a valid magic square.
        """
        slots = self._locator.locate(grid)
        missing = self._finder.find(grid)
        first_row = slots.first.row - 1
        first_col = slots.first.col - 1
        second_row = slots.second.row - 1
        second_col = slots.second.col - 1

        attempt_a = (
            grid.with_cell(first_row, first_col, missing.m1)
            .with_cell(second_row, second_col, missing.m2)
        )
        if self._validator.is_valid(attempt_a):
            return SolutionVector(
                r1=slots.first.row,
                c1=slots.first.col,
                n1=missing.m1,
                r2=slots.second.row,
                c2=slots.second.col,
                n2=missing.m2,
            )

        attempt_b = (
            grid.with_cell(first_row, first_col, missing.m2)
            .with_cell(second_row, second_col, missing.m1)
        )
        if self._validator.is_valid(attempt_b):
            return SolutionVector(
                r1=slots.first.row,
                c1=slots.first.col,
                n1=missing.m2,
                r2=slots.second.row,
                c2=slots.second.col,
                n2=missing.m1,
            )

        raise DomainError(
            code=NO_VALID_COMPLETION,
            message="No valid magic square completion exists.",
        )
