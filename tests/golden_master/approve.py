"""Approve-pattern compare and update for Golden Master files."""

from __future__ import annotations

import difflib
from pathlib import Path

from .capture import build_golden_master_document

DEFAULT_GOLDEN_PATH = Path(__file__).resolve().parents[1] / "golden_master_expected.txt"


def read_golden_master(path: Path = DEFAULT_GOLDEN_PATH) -> str | None:
    """Read golden master file when present."""
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_golden_master(content: str, path: Path = DEFAULT_GOLDEN_PATH) -> None:
    """Persist golden master content with UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def unified_diff(expected: str, actual: str, path: Path) -> str:
    """Build unified diff between expected and actual golden documents."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"{path.name} (expected)",
            tofile=f"{path.name} (actual)",
        )
    )


def approve_or_compare(*, approve: bool, path: Path = DEFAULT_GOLDEN_PATH) -> None:
    """Create, compare, or update the golden master baseline.

    Args:
        approve: When ``True``, overwrite the baseline with current output.
        path: Target golden master file path.

    Raises:
        AssertionError: When actual output differs from the baseline.
    """
    actual = build_golden_master_document()
    expected = read_golden_master(path)

    if expected is None or approve:
        write_golden_master(actual, path)
        return

    if expected != actual:
        diff = unified_diff(expected, actual, path)
        raise AssertionError(
            "Golden Master mismatch. Run with --approve-golden-master to update.\n"
            f"{diff}"
        )
