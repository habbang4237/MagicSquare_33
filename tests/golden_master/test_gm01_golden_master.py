"""GM-1 Golden Master regression test — PuzzleBoundary E2E approve pattern."""

from __future__ import annotations

import pytest

from .approve import approve_or_compare


@pytest.mark.integration
def test_gm01_golden_master_boundary_output(request: pytest.FixtureRequest) -> None:
    """GM-1 — actual Boundary output matches ``golden_master_expected.txt``."""
    approve = request.config.getoption("--approve-golden-master")
    approve_or_compare(approve=approve)
