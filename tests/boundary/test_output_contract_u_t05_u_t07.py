"""U-T05, U-T07 — output contract RED skeleton (Mock UseCase)."""

from __future__ import annotations

import pytest

from boundary.error_response import ErrorResponse
from boundary.puzzle_boundary import PuzzleBoundary
from control.solve_puzzle_use_case import SolvePuzzleUseCase

# ECB: PuzzleBoundary → SolvePuzzleUseCase only (no PuzzleSolver / Validator direct).


@pytest.mark.unit
class TestUt05OutputSuccessRed:
    """U-T05, AC-FR05-5 — valid input + Mock execute returns int[6] (skeleton)."""

    def test_u_t05_valid_input_returns_six_element_vector(self) -> None:
        """U-T05 — Mock execute → len(result)==6, execute 1회."""
        # Given — valid 4×4 grid, count(0)==2 (literals TBD per Report/02)
        # mock_use_case = Mock(spec=SolvePuzzleUseCase)
        # mock_use_case.execute.return_value = [1, 2, 3, 4, 5, 6]
        # boundary = PuzzleBoundary(use_case=mock_use_case)
        # When
        # result = boundary.receive(grid)
        # Then — len(result)==6, execute called once
        pytest.fail("RED: U-T05 — Mock execute → int[6]")


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
