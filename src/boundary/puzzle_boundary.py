"""Boundary entry point for puzzle input."""

from __future__ import annotations

from typing import Any

from boundary.error_response import ErrorResponse
from boundary.input_contract_validator import InputContractValidator
from control.solve_puzzle_use_case import SolvePuzzleUseCase


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
        return self._use_case.execute(grid)
