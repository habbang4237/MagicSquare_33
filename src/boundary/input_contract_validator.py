"""Validates incoming grid against FR-01 input contract."""

from __future__ import annotations

from typing import Any

from boundary.error_messages import (
    E_EMPTY_COUNT_CODE,
    E_EMPTY_COUNT_MESSAGE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)
from boundary.error_response import ErrorResponse

_GRID_DIMENSION = 4
_REQUIRED_EMPTY_COUNT = 2


class InputContractValidator:
    """Checks ``int[4][4]`` input shape and value constraints at Boundary."""

    def validate(self, grid: Any) -> ErrorResponse | None:
        """Return ``ErrorResponse`` on contract violation, else ``None``.

        Args:
            grid: Raw grid payload from external caller.

        Returns:
            ``ErrorResponse`` when validation fails; ``None`` when valid so far.
        """
        if grid is None:
            return ErrorResponse(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        if len(grid) == 0:
            return ErrorResponse(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        if len(grid) != _GRID_DIMENSION:
            return ErrorResponse(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        for row in grid:
            if not isinstance(row, list) or len(row) != _GRID_DIMENSION:
                return ErrorResponse(
                    code=INVALID_SIZE_CODE,
                    message=INVALID_SIZE_MESSAGE,
                )
        empty_count = sum(cell == 0 for row in grid for cell in row)
        if empty_count != _REQUIRED_EMPTY_COUNT:
            return ErrorResponse(
                code=E_EMPTY_COUNT_CODE,
                message=E_EMPTY_COUNT_MESSAGE,
            )
        return None
