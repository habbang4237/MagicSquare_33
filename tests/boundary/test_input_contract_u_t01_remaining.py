"""U-T01d~f — 4×4 size contract RED skeleton (remaining cases)."""

from __future__ import annotations

import pytest

from boundary.error_response import ErrorResponse
from boundary.input_contract_validator import InputContractValidator

# PRD §16.4 invalid_size anchor
INVALID_SIZE_GRID = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


@pytest.mark.unit
class TestUt01RemainingSizeRed:
    """U-T01d~f, AC-FR01-1 — non-4×4 grids return E_SIZE (skeleton)."""

    def test_u_t01d_four_by_three_grid_returns_e_size(self) -> None:
        """U-T01d, AC-FR01-1 — 4×3 column-count mismatch → E_SIZE."""
        # Given
        # grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]  # 4 rows × 3 cols
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_SIZE, Domain not invoked (AC-FR01-5 covered elsewhere for null)
        pytest.fail("RED: U-T01d — 4×3 grid → E_SIZE")

    def test_u_t01e_five_by_five_grid_returns_e_size(self) -> None:
        """U-T01e, AC-FR01-1 — 5×5 grid → E_SIZE."""
        # Given
        # grid = [[1] * 5 for _ in range(5)]
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — E_SIZE
        pytest.fail("RED: U-T01e — 5×5 grid → E_SIZE")

    def test_u_t01f_invalid_size_prd_label_returns_e_size(self) -> None:
        """U-T01f, AC-FR01-1 — PRD §16.4 invalid_size (3×3) → E_SIZE."""
        # Given
        # grid = INVALID_SIZE_GRID
        # validator = InputContractValidator()
        # When
        # result = validator.validate(grid)
        # Then — isinstance(result, ErrorResponse), code E_SIZE
        pytest.fail("RED: U-T01f — invalid_size → E_SIZE")
