"""AC-FR-01-01, PRD §8.1 INVALID_SIZE — FR-01 input size validation RED tests."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from boundary.error_response import ErrorResponse
from boundary.input_contract_validator import InputContractValidator
from boundary.puzzle_boundary import PuzzleBoundary
from control.solve_puzzle_use_case import SolvePuzzleUseCase

# PRD §8.1 / AC-FR-01-01 고정 계약 (Boundary 노출 코드)
EXPECTED_CODE = "INVALID_SIZE"
EXPECTED_MESSAGE = "Grid must be 4x4."

# AC-FR-01-02~05 범위 — 본 슬라이스에서 반환되면 안 되는 코드
OUT_OF_SCOPE_CODES = frozenset(
    {
        "INVALID_EMPTY_COUNT",
        "INVALID_RANGE",
        "INVALID_DUPLICATE",
        "E_EMPTY_COUNT",
        "E_RANGE",
        "E_DUPLICATE",
        "E_NO_SOLUTION",
    }
)


@pytest.mark.unit
class TestAcFr0101InvalidSizeRed:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Track A Boundary RED suite."""

    # ------------------------------------------------------------------
    # 정상 실패 반환 (Happy Path of Failure)
    # ------------------------------------------------------------------

    def test_none_grid_returns_invalid_size_code(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — null grid rejects with size code."""
        # AC-FR-01-01
        # Given
        grid = None
        boundary = PuzzleBoundary(use_case=Mock(spec=SolvePuzzleUseCase))

        # When
        result = boundary.receive(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE

    def test_none_grid_returns_error_response_type(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure payload is ErrorResponse."""
        # AC-FR-01-01
        # Given
        grid = None
        boundary = PuzzleBoundary(use_case=Mock(spec=SolvePuzzleUseCase))

        # When
        result = boundary.receive(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert not isinstance(result, list)

    # ------------------------------------------------------------------
    # 메시지 동일성 (PRD §8.1 문구 byte-equal)
    # ------------------------------------------------------------------

    def test_none_grid_message_byte_equal_prd_section(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message matches PRD exactly."""
        # AC-FR-01-01
        # Given
        grid = None
        boundary = PuzzleBoundary(use_case=Mock(spec=SolvePuzzleUseCase))
        prd_message = "Grid must be 4x4."

        # When
        result = boundary.receive(grid)

        # Then
        assert result.message == prd_message
        assert result.message == EXPECTED_MESSAGE

    # ------------------------------------------------------------------
    # 격리 검증 — Domain 해 결정 진입점(resolve) 0회
    # ------------------------------------------------------------------

    def test_none_grid_resolve_zero_calls(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve entry point never invoked."""
        # AC-FR-01-01
        # Given
        grid = None
        mock_use_case = Mock(spec=SolvePuzzleUseCase)
        boundary = PuzzleBoundary(use_case=mock_use_case)

        # When
        result = boundary.receive(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        mock_use_case.execute.assert_not_called()
        mock_use_case.resolve.assert_not_called()

    # ------------------------------------------------------------------
    # 경계값 — 크기 불일치
    # ------------------------------------------------------------------

    def test_empty_list_returns_invalid_size_failure(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — zero-row grid is rejected."""
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []
        validator = InputContractValidator()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    def test_four_empty_rows_returns_invalid_size_failure(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — four rows with zero columns rejected."""
        # AC-FR-01-01
        # Given
        grid = [[]] * 4
        validator = InputContractValidator()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    def test_three_by_four_grid_returns_invalid_size_failure(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3×4 row-count mismatch rejected."""
        # AC-FR-01-01
        # Given
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        validator = InputContractValidator()

        # When
        result = validator.validate(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    # ------------------------------------------------------------------
    # 범위 제한 — AC-FR-01-02~05 / FR-02~05 코드 미반환
    # ------------------------------------------------------------------

    def test_none_grid_not_out_of_scope_error_codes(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — only size code, not later FR codes."""
        # AC-FR-01-01
        # Given
        grid = None
        boundary = PuzzleBoundary(use_case=Mock(spec=SolvePuzzleUseCase))

        # When
        result = boundary.receive(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.code not in OUT_OF_SCOPE_CODES
