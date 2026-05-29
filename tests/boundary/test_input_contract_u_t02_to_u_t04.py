"""U-T02a~b, U-T03a~b, U-T04, AC-FR01-5 — input contract RED skeleton."""

from __future__ import annotations

import pytest

from boundary.error_response import ErrorResponse
from boundary.input_contract_validator import InputContractValidator
from boundary.puzzle_boundary import PuzzleBoundary
from control.solve_puzzle_use_case import SolvePuzzleUseCase

# ECB: Boundary must not call PuzzleSolver / MagicSquareValidator directly.
# Invalid input → SolvePuzzleUseCase.execute 0회 (AC-FR01-5).


@pytest.mark.unit
class TestUt02EmptyCountRed:
    """U-T02a~b, AC-FR01-2 — empty-cell count validation (skeleton)."""

    def test_u_t02a_zero_empty_cells_returns_e_empty_count(self) -> None:
        """U-T02a, AC-FR01-2 — count(0)==0 → E_EMPTY_COUNT."""
        # Given — fixture label: invalid_blank_0 (4×4, no zeros)
        # grid = ...  # TODO: lock literal per Report/02
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_EMPTY_COUNT
        pytest.fail("RED: U-T02a — 빈칸 0개 → E_EMPTY_COUNT")

    def test_u_t02b_three_empty_cells_returns_e_empty_count(self) -> None:
        """U-T02b, AC-FR01-2 — count(0)==3 → E_EMPTY_COUNT."""
        # Given — PRD §16.4: 4×4 with three zeros
        # grid = ...
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_EMPTY_COUNT
        pytest.fail("RED: U-T02b — 빈칸 3개 → E_EMPTY_COUNT")


@pytest.mark.unit
class TestUt03RangeRed:
    """U-T03a~b, AC-FR01-3 — cell value range validation (skeleton)."""

    def test_u_t03a_cell_seventeen_returns_e_range(self) -> None:
        """U-T03a, AC-FR01-3 — value 17 → E_RANGE."""
        # Given — fixture label: invalid_range (cell 17)
        # grid = ...
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_RANGE
        pytest.fail("RED: U-T03a — 값 17 → E_RANGE")

    def test_u_t03b_cell_negative_one_returns_e_range(self) -> None:
        """U-T03b, AC-FR01-3 — value -1 → E_RANGE."""
        # Given — fixture label: invalid_range (cell -1)
        # grid = ...
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_RANGE
        pytest.fail("RED: U-T03b — 값 -1 → E_RANGE")


@pytest.mark.unit
class TestUt04DuplicateRed:
    """U-T04, AC-FR01-4 — non-zero duplicate validation (skeleton)."""

    def test_u_t04_duplicate_five_returns_e_duplicate(self) -> None:
        """U-T04, AC-FR01-4 — duplicate non-zero 5 → E_DUPLICATE."""
        # Given — fixture label: duplicate_five
        # grid = ...
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_DUPLICATE
        pytest.fail("RED: U-T04 — 비零 5 중복 → E_DUPLICATE")


@pytest.mark.unit
class TestAcFr015ExecuteIsolationUt02ToUt04Red:
    """AC-FR01-5 — U-T02~U-T04 invalid grids: UseCase.execute 0회 (skeleton)."""

    def test_ac_fr01_5_u_t02a_execute_zero_calls(self) -> None:
        """AC-FR01-5 — U-T02a invalid: Mock(spec=SolvePuzzleUseCase), execute 0회."""
        # Given
        # mock_use_case = Mock(spec=SolvePuzzleUseCase)
        # boundary = PuzzleBoundary(use_case=mock_use_case)
        # grid = ...  # U-T02a: zero empty cells
        # When
        # result = boundary.receive(grid)
        # Then — ErrorResponse, mock_use_case.execute not called
        pytest.fail("RED: AC-FR01-5 — U-T02a invalid → execute 0회")

    def test_ac_fr01_5_u_t02b_execute_zero_calls(self) -> None:
        """AC-FR01-5 — U-T02b invalid: execute 0회."""
        # Given — Mock(spec=SolvePuzzleUseCase), PuzzleBoundary
        pytest.fail("RED: AC-FR01-5 — U-T02b invalid → execute 0회")

    def test_ac_fr01_5_u_t03a_execute_zero_calls(self) -> None:
        """AC-FR01-5 — U-T03a invalid: execute 0회."""
        # Given — Mock(spec=SolvePuzzleUseCase), PuzzleBoundary
        pytest.fail("RED: AC-FR01-5 — U-T03a invalid → execute 0회")

    def test_ac_fr01_5_u_t03b_execute_zero_calls(self) -> None:
        """AC-FR01-5 — U-T03b invalid: execute 0회."""
        # Given — Mock(spec=SolvePuzzleUseCase), PuzzleBoundary
        pytest.fail("RED: AC-FR01-5 — U-T03b invalid → execute 0회")

    def test_ac_fr01_5_u_t04_execute_zero_calls(self) -> None:
        """AC-FR01-5 — U-T04 invalid: execute 0회."""
        # Given — Mock(spec=SolvePuzzleUseCase), PuzzleBoundary
        pytest.fail("RED: AC-FR01-5 — U-T04 invalid → execute 0회")
