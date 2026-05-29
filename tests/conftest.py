"""Shared pytest fixtures — PRD §16.4 labels (placeholder, literals TBD)."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register Golden Master approve CLI flag."""
    parser.addoption(
        "--approve-golden-master",
        action="store_true",
        default=False,
        help="Overwrite tests/golden_master_expected.txt with current output.",
    )


@pytest.fixture
def invalid_blank_1() -> None:
    """PRD §16.4 `invalid_blank_1` — U-T02a: 4×4, exactly one `0`."""
    # TODO: lock grid literal per Report/02
    return None


@pytest.fixture
def invalid_range() -> None:
    """PRD §16.4 `invalid_range` — U-T03: cell value `17` or `-1`."""
    # TODO: lock grid literal per Report/02
    return None


@pytest.fixture
def duplicate_five() -> None:
    """PRD §16.4 `duplicate_five` — U-T04: value `5` in two cells."""
    # TODO: lock grid literal per Report/02
    return None


@pytest.fixture
def row_major_blanks() -> None:
    """PRD §16.4 `row_major_blanks` — D-T03: 1st=(2,3), 2nd=(3,1) 1-index."""
    # TODO: lock 16 integers per Report/02
    return None


@pytest.fixture
def small_first_success() -> None:
    """PRD §16.4 `small_first_success` — D-T01: attempt A only valid."""
    # TODO: lock literals per Report/02
    return None


@pytest.fixture
def reverse_only_success() -> None:
    """PRD §16.4 `reverse_only_success` — D-T02: attempt B only valid."""
    pytest.fail("RED: D-T02 — reverse_only_success fixture TBD")


@pytest.fixture
def no_completion() -> None:
    """PRD §16.4 `no_completion` — D-T13: attempts A and B both fail."""
    # TODO: lock literals per Report/02
    return None
