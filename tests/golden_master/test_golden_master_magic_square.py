"""GM-2 Golden Master regression tests — per Test-Case approve pattern."""

from __future__ import annotations

import pytest

from boundary.error_response import ErrorResponse

from .approve import approve_or_compare_scenario
from .capture import capture_boundary_result
from .contract_checks import (
    assert_error_contract,
    assert_int6_output_format,
    assert_one_index_coordinates,
    assert_reverse_fallback_rule,
    assert_row_major_slot_match,
    assert_small_first_combination_rule,
)
from .scenarios import (
    DUPLICATE_NUMBER_GRID,
    INVALID_BLANK_COUNT_GRID,
    NO_VALID_SOLUTION_GRID,
    NORMAL_SUCCESS_GRID,
    REVERSE_SUCCESS_GRID,
    SCENARIO_BY_TEST_CASE_ID,
)

pytestmark = pytest.mark.golden_master


@pytest.fixture
def approve_golden_master(request: pytest.FixtureRequest) -> bool:
    """Return whether ``--approve-golden-master`` was passed."""
    return bool(request.config.getoption("--approve-golden-master"))


def _run_gm_tc(
    test_case_id: str,
    *,
    approve: bool,
    success_contract: str | None = None,
) -> None:
    """Execute one GM-TC: contract checks + golden block compare."""
    scenario = SCENARIO_BY_TEST_CASE_ID[test_case_id]
    result = capture_boundary_result(scenario.grid)

    if scenario.expected_error_code is not None:
        assert isinstance(result, ErrorResponse)
        assert_error_contract(result, scenario.expected_error_code)
    else:
        assert isinstance(result, list)
        assert_int6_output_format(result)
        assert_one_index_coordinates(result)
        assert_row_major_slot_match(scenario.grid, result)
        if success_contract == "small_first":
            assert_small_first_combination_rule(scenario.grid, result)
        elif success_contract == "reverse_fallback":
            assert_reverse_fallback_rule(scenario.grid, result)

    approve_or_compare_scenario(scenario, approve=approve)


@pytest.mark.golden_master
def test_gm_tc_01_normal_success(approve_golden_master: bool) -> None:
    """GM-TC-01 — attempt A (small-first) succeeds; int[6] contract."""
    _run_gm_tc("GM-TC-01", approve=approve_golden_master, success_contract="small_first")


@pytest.mark.golden_master
def test_gm_tc_02_reverse_success(approve_golden_master: bool) -> None:
    """GM-TC-02 — attempt A fails; attempt B (reverse) succeeds."""
    _run_gm_tc(
        "GM-TC-02",
        approve=approve_golden_master,
        success_contract="reverse_fallback",
    )


@pytest.mark.golden_master
def test_gm_tc_03_invalid_blank_count(approve_golden_master: bool) -> None:
    """GM-TC-03 — blank count != 2 → ``E_EMPTY_COUNT`` error contract."""
    _run_gm_tc("GM-TC-03", approve=approve_golden_master)


@pytest.mark.golden_master
def test_gm_tc_04_duplicate_number(approve_golden_master: bool) -> None:
    """GM-TC-04 — duplicate non-zero → ``E_DUPLICATE`` error contract."""
    _run_gm_tc("GM-TC-04", approve=approve_golden_master)


@pytest.mark.golden_master
def test_gm_tc_05_no_valid_magic_square(approve_golden_master: bool) -> None:
    """GM-TC-05 — no completion → ``E_NO_SOLUTION`` error contract."""
    _run_gm_tc("GM-TC-05", approve=approve_golden_master)


@pytest.mark.golden_master
class TestGoldenMasterMagicSquareInputs:
    """Sanity — GM-TC fixture grids remain locked."""

    def test_gm_tc_01_grid_locked(self) -> None:
        """GM-TC-01 uses D-T01 small-first success fixture."""
        assert NORMAL_SUCCESS_GRID[1][0] == 0
        assert NORMAL_SUCCESS_GRID[2][2] == 0

    def test_gm_tc_02_grid_locked(self) -> None:
        """GM-TC-02 uses reverse-only success fixture."""
        assert REVERSE_SUCCESS_GRID[1][1] == 0
        assert REVERSE_SUCCESS_GRID[2][2] == 0

    def test_gm_tc_03_grid_has_zero_blanks(self) -> None:
        """GM-TC-03 has no empty cells."""
        assert sum(cell == 0 for row in INVALID_BLANK_COUNT_GRID for cell in row) == 0

    def test_gm_tc_04_grid_has_duplicate_five(self) -> None:
        """GM-TC-04 has two cells with value 5."""
        fives = sum(
            1 for row in DUPLICATE_NUMBER_GRID for cell in row if cell == 5
        )
        assert fives == 2

    def test_gm_tc_05_grid_has_two_blanks(self) -> None:
        """GM-TC-05 has exactly two empty cells."""
        blanks = sum(cell == 0 for row in NO_VALID_SOLUTION_GRID for cell in row)
        assert blanks == 2
