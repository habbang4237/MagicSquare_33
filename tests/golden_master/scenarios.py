"""GM-2 input scenarios — Report/02·PRD §16.4 aligned fixtures."""

from __future__ import annotations

from dataclasses import dataclass

from boundary.error_messages import (
    E_DUPLICATE_CODE,
    E_EMPTY_COUNT_CODE,
    E_NO_SOLUTION_CODE,
)

NORMAL_SUCCESS_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [0, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
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

    test_case_id: str
    name: str
    grid: list[list[int]]
    expected_error_code: str | None = None


GM_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario("GM-TC-01", "normal_success", NORMAL_SUCCESS_GRID),
    GoldenMasterScenario("GM-TC-02", "reverse_success", REVERSE_SUCCESS_GRID),
    GoldenMasterScenario(
        "GM-TC-03",
        "invalid_blank_count",
        INVALID_BLANK_COUNT_GRID,
        expected_error_code=E_EMPTY_COUNT_CODE,
    ),
    GoldenMasterScenario(
        "GM-TC-04",
        "duplicate_number",
        DUPLICATE_NUMBER_GRID,
        expected_error_code=E_DUPLICATE_CODE,
    ),
    GoldenMasterScenario(
        "GM-TC-05",
        "no_valid_solution",
        NO_VALID_SOLUTION_GRID,
        expected_error_code=E_NO_SOLUTION_CODE,
    ),
)

SCENARIO_BY_TEST_CASE_ID = {scenario.test_case_id: scenario for scenario in GM_SCENARIOS}
