"""Solve puzzle application use case (Control port for Boundary)."""

from __future__ import annotations

from typing import Any

from control.use_case_error import UseCaseError
from entity.domain_error_codes import NO_VALID_COMPLETION
from entity.errors import DomainError
from entity.grid import Grid
from entity.puzzle_solver import PuzzleSolver


class SolvePuzzleUseCase:
    """Orchestrates puzzle resolution (stub for Boundary Mock spec)."""

    def __init__(self) -> None:
        """Initialize domain solver collaborator."""
        self._solver = PuzzleSolver()

    def execute(self, grid: Any) -> list[int]:
        """Run puzzle resolution for a validated grid.

        Args:
            grid: Validated ``int[4][4]`` puzzle grid.

        Returns:
            Solution coordinates ``int[6]``.
        """
        domain_grid = Grid.of(grid)
        solution = self._solver.solve(domain_grid)
        return solution.to_array()

    def try_execute(self, grid: Any) -> list[int] | UseCaseError:
        """Run puzzle resolution; return domain failure without raising.

        Args:
            grid: Validated ``int[4][4]`` puzzle grid.

        Returns:
            Solution ``int[6]`` on success, or ``UseCaseError`` on domain failure.
        """
        try:
            return self.execute(grid)
        except DomainError as exc:
            if exc.code == NO_VALID_COMPLETION:
                return UseCaseError(code=exc.code)
            raise

    def resolve(self, grid: Any) -> list[int]:
        """Alternative resolution entry point (stub).

        Args:
            grid: Validated ``int[4][4]`` puzzle grid.

        Returns:
            Solution coordinates ``int[6]``.
        """
        raise NotImplementedError
