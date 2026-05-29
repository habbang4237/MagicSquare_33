"""GM-1 input scenarios — Report/02·PRD §16.4 aligned fixtures."""

from __future__ import annotations

from dataclasses import dataclass

NORMAL_SUCCESS_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

REVERSE_SUCCESS_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

INVALID_BLANK_COUNT_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

DUPLICATE_NUMBER_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 5],
]

NO_VALID_SOLUTION_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 0, 11],
    [12, 13, 14, 0],
]


@dataclass(frozen=True, slots=True)
class GoldenMasterScenario:
    """Named puzzle input for Golden Master capture."""

    name: str
    grid: list[list[int]]


GM_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario("normal_success", NORMAL_SUCCESS_GRID),
    GoldenMasterScenario("reverse_success", REVERSE_SUCCESS_GRID),
    GoldenMasterScenario("invalid_blank_count", INVALID_BLANK_COUNT_GRID),
    GoldenMasterScenario("duplicate_number", DUPLICATE_NUMBER_GRID),
    GoldenMasterScenario("no_valid_solution", NO_VALID_SOLUTION_GRID),
)
