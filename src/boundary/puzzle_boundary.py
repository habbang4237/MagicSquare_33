"""Boundary entry point for puzzle input."""

from __future__ import annotations

from typing import Any

from boundary.error_messages import (
    DOMAIN_NO_VALID_COMPLETION,
    E_NO_SOLUTION_CODE,
    E_NO_SOLUTION_MESSAGE,
)
from boundary.error_response import ErrorResponse
from boundary.input_contract_validator import InputContractValidator
from control.solve_puzzle_use_case import SolvePuzzleUseCase
from control.use_case_error import UseCaseError


class PuzzleBoundary:
    """Receives external grid input and delegates solving to Control layer."""

    def __init__(self, use_case: SolvePuzzleUseCase) -> None:
        """Initialize with injected use case (Control port).

        Args:
            use_case: Application use case for puzzle resolution.
        """
        self._use_case = use_case
        self._validator = InputContractValidator()

    def receive(self, grid: Any) -> ErrorResponse | list[int]:
        """Accept grid input; return error or solution coordinates.

        Args:
            grid: ``int[4][4]`` puzzle grid (``0`` = empty cell).

        Returns:
            ``ErrorResponse`` on validation failure; solution ``int[6]`` otherwise.
        """
        validation_result = self._validator.validate(grid)
        if validation_result is not None:
            return validation_result
        result = self._use_case.try_execute(grid)
        if isinstance(result, UseCaseError):
            return self._map_use_case_error(result)
        return result

    def _map_use_case_error(self, error: UseCaseError) -> ErrorResponse:
        """Map Control failure payload to fixed Boundary ``ErrorResponse``.

        Args:
            error: Control-layer failure from use case execution.

        Returns:
            Boundary ``ErrorResponse`` for the given domain code.
        """
        if error.code == DOMAIN_NO_VALID_COMPLETION:
            return ErrorResponse(
                code=E_NO_SOLUTION_CODE,
                message=E_NO_SOLUTION_MESSAGE,
            )
        return ErrorResponse(code=error.code, message=error.code)
