"""SolvePuzzleUseCase Control orchestration — no Entity mocks."""

from __future__ import annotations

import pytest

from control.solve_puzzle_use_case import SolvePuzzleUseCase

# Report/02·D-T05 anchor — UC-D4 via Control (Grid.of → PuzzleSolver.solve)
PUZZLE_GRID = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]
# UC-D4: attempt B succeeds for this fixture (attempt A invalid)
EXPECTED_SOLUTION = [2, 2, 10, 3, 3, 7]


@pytest.mark.unit
class TestSolvePuzzleUseCaseExecute:
    """UC-D4 — Control delegates to Domain without mocks."""

    def test_execute_valid_puzzle_returns_six_element_solution(self) -> None:
        """IT-01 path — execute → Grid.of → PuzzleSolver.solve → int[6]."""
        # Given
        use_case = SolvePuzzleUseCase()

        # When
        result = use_case.execute(PUZZLE_GRID)

        # Then
        assert isinstance(result, list)
        assert len(result) == 6
        assert result == EXPECTED_SOLUTION
