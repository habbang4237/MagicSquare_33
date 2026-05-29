"""D-T01, D-T02, D-T13 — PuzzleSolver Domain RED skeleton (no mocks)."""

from __future__ import annotations

import pytest

from entity.errors import DomainError
from entity.grid import Grid
from entity.puzzle_solver import PuzzleSolver
from entity.solution_vector import SolutionVector

# Report/02·D-T01 anchor — attempt A only valid (classic 4×4, blanks at (2,1),(3,3))
SMALL_FIRST_SUCCESS_GRID = [
    [16, 3, 2, 13],
    [0, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]
EXPECTED_D_T01_SOLUTION = [2, 1, 5, 3, 3, 7]

# UC-D4: attempt A (m1 at first slot) before attempt B (m2 at first slot).


@pytest.mark.unit
class TestDt01SmallFirstSuccessRed:
    """D-T01, I-D4~I-D12, I-D11 — attempt A wins (skeleton)."""

    def test_d_t01_small_first_success_returns_solution_vector(
        self,
    ) -> None:
        """D-T01 — fixture small_first_success → [r1,c1,m1,r2,c2,m2]."""
        # Given
        grid = Grid.of(SMALL_FIRST_SUCCESS_GRID)
        solver = PuzzleSolver()

        # When
        solution = solver.solve(grid)

        # Then
        assert isinstance(solution, SolutionVector)
        assert solution.to_array() == EXPECTED_D_T01_SOLUTION


@pytest.mark.unit
class TestDt02ReverseOnlySuccessRed:
    """D-T02, I-D4~I-D7 — attempt B only succeeds (skeleton)."""

    def test_d_t02_reverse_only_success_returns_swapped_missing_order(
        self,
        reverse_only_success: None,
    ) -> None:
        """D-T02 — fixture reverse_only_success → [r1,c1,m2,r2,c2,m1]."""
        # Given — fixture: reverse_only_success (16 integers TBD in conftest)
        # grid = Grid.of(...)
        # solver = PuzzleSolver()
        # When
        # solution = solver.solve(grid)
        # Then — [r1,c1,m2,r2,c2,m1]
        pytest.fail("RED: D-T02 — reverse_only_success → swapped m1/m2")


@pytest.mark.unit
class TestDt13NoCompletionRed:
    """D-T13, I-D4~I-D7 — both attempts fail (skeleton)."""

    def test_d_t13_no_completion_raises_no_valid_completion(
        self,
        no_completion: None,
    ) -> None:
        """D-T13 — fixture no_completion → DomainError NO_VALID_COMPLETION."""
        # Given — fixture: no_completion
        # grid = Grid.of(...)
        # solver = PuzzleSolver()
        # When / Then — pytest.raises(DomainError) NO_VALID_COMPLETION
        pytest.fail("RED: D-T13 — no_completion → NO_VALID_COMPLETION")
