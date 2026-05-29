"""GM-2 contract assertions — int[6], row-major, attempt rules, errors."""

from __future__ import annotations

from boundary.error_messages import (
    E_DUPLICATE_CODE,
    E_DUPLICATE_MESSAGE,
    E_EMPTY_COUNT_CODE,
    E_EMPTY_COUNT_MESSAGE,
    E_NO_SOLUTION_CODE,
    E_NO_SOLUTION_MESSAGE,
)
from boundary.error_response import ErrorResponse
from entity.empty_cell_locator import EmptyCellLocator
from entity.grid import Grid
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder

_GRID_DIMENSION = 4
_ERROR_MESSAGES = {
    E_EMPTY_COUNT_CODE: E_EMPTY_COUNT_MESSAGE,
    E_DUPLICATE_CODE: E_DUPLICATE_MESSAGE,
    E_NO_SOLUTION_CODE: E_NO_SOLUTION_MESSAGE,
}


def locate_row_major_blanks(grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return 1-index row-major blank coordinates."""
    blanks: list[tuple[int, int]] = []
    for row in range(_GRID_DIMENSION):
        for col in range(_GRID_DIMENSION):
            if grid[row][col] == 0:
                blanks.append((row + 1, col + 1))
    return blanks[0], blanks[1]


def _build_attempt_grid(
    grid: list[list[int]],
    *,
    first_value: int,
    second_value: int,
) -> Grid:
    """Fill row-major blanks with the given pair."""
    domain_grid = Grid.of(grid)
    slots = EmptyCellLocator().locate(domain_grid)
    return (
        domain_grid.with_cell(slots.first.row - 1, slots.first.col - 1, first_value)
        .with_cell(slots.second.row - 1, slots.second.col - 1, second_value)
    )


def assert_int6_output_format(result: list[int]) -> None:
    """Verify ``int[6]`` list shape."""
    assert isinstance(result, list)
    assert len(result) == 6
    assert all(isinstance(value, int) for value in result)


def assert_one_index_coordinates(result: list[int]) -> None:
    """Verify rows, columns, and values use 1-index contract ranges."""
    rows = (result[0], result[3])
    cols = (result[1], result[4])
    values = (result[2], result[5])
    for row, col in zip(rows, cols, strict=True):
        assert 1 <= row <= _GRID_DIMENSION
        assert 1 <= col <= _GRID_DIMENSION
    for value in values:
        assert 1 <= value <= 16


def assert_row_major_slot_match(grid: list[list[int]], result: list[int]) -> None:
    """Verify output coordinates match row-major blank positions."""
    first, second = locate_row_major_blanks(grid)
    assert [result[0], result[1]] == [first[0], first[1]]
    assert [result[3], result[4]] == [second[0], second[1]]


def assert_small_first_combination_rule(grid: list[list[int]], result: list[int]) -> None:
    """Verify attempt A (m1→slot1, m2→slot2) succeeds."""
    missing = MissingNumberFinder().find(Grid.of(grid))
    validator = MagicSquareValidator()
    attempt_a = _build_attempt_grid(
        grid,
        first_value=missing.m1,
        second_value=missing.m2,
    )
    assert validator.is_valid(attempt_a)
    assert result[2] == missing.m1
    assert result[5] == missing.m2


def assert_reverse_fallback_rule(grid: list[list[int]], result: list[int]) -> None:
    """Verify attempt A fails and attempt B (m2→slot1, m1→slot2) succeeds."""
    missing = MissingNumberFinder().find(Grid.of(grid))
    validator = MagicSquareValidator()
    attempt_a = _build_attempt_grid(
        grid,
        first_value=missing.m1,
        second_value=missing.m2,
    )
    attempt_b = _build_attempt_grid(
        grid,
        first_value=missing.m2,
        second_value=missing.m1,
    )
    assert not validator.is_valid(attempt_a)
    assert validator.is_valid(attempt_b)
    assert result[2] == missing.m2
    assert result[5] == missing.m1


def assert_error_contract(result: ErrorResponse, expected_code: str) -> None:
    """Verify Boundary ``ErrorResponse`` code and fixed message."""
    assert isinstance(result, ErrorResponse)
    assert result.code == expected_code
    assert result.message == _ERROR_MESSAGES[expected_code]
