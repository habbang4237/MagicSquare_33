"""Serialize PuzzleBoundary results for Golden Master files."""

from __future__ import annotations

from typing import Any

from boundary.error_response import ErrorResponse
from boundary.puzzle_boundary import PuzzleBoundary
from control.solve_puzzle_use_case import SolvePuzzleUseCase

from .scenarios import GM_SCENARIOS, GoldenMasterScenario


def format_grid(grid: list[list[int]]) -> str:
    """Render ``int[4][4]`` as four space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def serialize_scenario_block(scenario: GoldenMasterScenario, result: Any) -> str:
    """Format one ``[GM-TC-XX]`` block for the golden master file."""
    lines = [
        f"[{scenario.test_case_id}]",
        "Input:",
        format_grid(scenario.grid),
    ]
    if isinstance(result, ErrorResponse):
        lines.extend(["Error:", result.code])
    else:
        lines.extend(["Output:", str(result)])
    return "\n".join(lines)


def capture_boundary_result(grid: list[list[int]]) -> list[int] | ErrorResponse:
    """Run full Boundary stack and return the contract payload."""
    boundary = PuzzleBoundary(use_case=SolvePuzzleUseCase())
    return boundary.receive(grid)


def build_scenario_block(scenario: GoldenMasterScenario) -> str:
    """Capture one scenario and return its serialized block."""
    result = capture_boundary_result(scenario.grid)
    return serialize_scenario_block(scenario, result)


def build_golden_master_document() -> str:
    """Capture all GM scenarios and return the full expected document."""
    blocks = [build_scenario_block(scenario) for scenario in GM_SCENARIOS]
    return "\n\n".join(blocks) + "\n"
