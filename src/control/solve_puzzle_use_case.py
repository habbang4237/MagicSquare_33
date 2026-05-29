"""Solve puzzle application use case (Control port for Boundary)."""

from __future__ import annotations

from typing import Any


class SolvePuzzleUseCase:
    """Orchestrates puzzle resolution (stub for Boundary Mock spec)."""

    def execute(self, grid: Any) -> list[int]:
        """Run puzzle resolution for a validated grid.

        Args:
            grid: Validated ``int[4][4]`` puzzle grid.

        Returns:
            Solution coordinates ``int[6]``.
        """
        raise NotImplementedError

    def resolve(self, grid: Any) -> list[int]:
        """Alternative resolution entry point (stub).

        Args:
            grid: Validated ``int[4][4]`` puzzle grid.

        Returns:
            Solution coordinates ``int[6]``.
        """
        raise NotImplementedError
