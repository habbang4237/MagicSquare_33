"""U-T05, U-T07 — output contract RED skeleton (Mock UseCase)."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from boundary.error_response import ErrorResponse
from boundary.puzzle_boundary import PuzzleBoundary
from control.solve_puzzle_use_case import SolvePuzzleUseCase

# ECB: PuzzleBoundary → SolvePuzzleUseCase only (no PuzzleSolver / Validator direct).

# Report/02·D-T03 anchor — FR-01 통과 + 성공 출력 (UX-1: 래퍼 없음)
VALID_GRID = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]
EXPECTED_SOLUTION = [2, 2, 7, 3, 3, 10]


@pytest.mark.unit
class TestUt05OutputSuccessRed:
    """U-T05, AC-FR05-5 — valid input + Mock execute returns int[6] (skeleton)."""

    def test_u_t05_valid_input_returns_six_element_vector(self) -> None:
        """U-T05 — Mock execute → len(result)==6, execute 1회."""
        # Given
        mock_use_case = Mock(spec=SolvePuzzleUseCase)
        mock_use_case.execute.return_value = EXPECTED_SOLUTION
        boundary = PuzzleBoundary(use_case=mock_use_case)

        # When
        result = boundary.receive(VALID_GRID)

        # Then
        assert not isinstance(result, ErrorResponse)
        assert isinstance(result, list)
        assert len(result) == 6
        assert result == EXPECTED_SOLUTION
        mock_use_case.execute.assert_called_once_with(VALID_GRID)


@pytest.mark.unit
class TestUt07OutputFormatRed:
    """U-T07, AC-FR05-6 — output format validation (skeleton)."""

    def test_u_t07_mock_r1_zero_returns_e_output_format(self) -> None:
        """U-T07 — Mock returns r1=0 → E_OUTPUT_FORMAT."""
        # Given — valid input grid + Mock(spec=SolvePuzzleUseCase)
        # mock_use_case.execute.return_value = [0, 1, 2, 3, 4, 5]
        # boundary = PuzzleBoundary(use_case=mock_use_case)
        # When
        # result = boundary.receive(grid)
        # Then — ErrorResponse code E_OUTPUT_FORMAT
        pytest.fail("RED: U-T07 — Mock r1=0 → E_OUTPUT_FORMAT")
