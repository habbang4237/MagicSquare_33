"""Approve-pattern compare and update for Golden Master files."""

from __future__ import annotations

import difflib
import re
from pathlib import Path

from .capture import build_golden_master_document, build_scenario_block
from .scenarios import GoldenMasterScenario

DEFAULT_GOLDEN_PATH = Path(__file__).resolve().parents[1] / "golden_master_expected.txt"
DEFAULT_GOLDEN_MASTER_PATH = DEFAULT_GOLDEN_PATH
_BLOCK_HEADER = re.compile(r"^\[(?P<id>GM-TC-\d{2})\]\s*$", re.MULTILINE)


def read_golden_master(path: Path = DEFAULT_GOLDEN_PATH) -> str | None:
    """Read golden master file when present."""
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_golden_master(content: str, path: Path = DEFAULT_GOLDEN_PATH) -> None:
    """Persist golden master content with UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def parse_golden_blocks(content: str) -> dict[str, str]:
    """Split golden master document into ``{test_case_id: block_text}``."""
    matches = list(_BLOCK_HEADER.finditer(content))
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        block_id = match.group("id")
        blocks[block_id] = content[start:end].rstrip() + "\n"
    return blocks


def extract_block(content: str, test_case_id: str) -> str | None:
    """Return one scenario block from the golden master document."""
    return parse_golden_blocks(content).get(test_case_id)


def unified_diff(expected: str, actual: str, label: str) -> str:
    """Build unified diff between expected and actual golden blocks."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f"{label} (expected)",
            tofile=f"{label} (actual)",
        )
    )


def approve_or_compare_scenario(
    scenario: GoldenMasterScenario,
    *,
    approve: bool,
    path: Path = DEFAULT_GOLDEN_PATH,
) -> None:
    """Compare or approve one GM scenario block.

    Args:
        scenario: Target scenario definition.
        approve: When ``True``, regenerate the full golden master file.
        path: Target golden master file path.

    Raises:
        AssertionError: When actual output differs from the baseline.
    """
    actual_block = build_scenario_block(scenario) + "\n"
    document = read_golden_master(path)

    if document is None or approve:
        write_golden_master(build_golden_master_document(), path)
        return

    expected_block = extract_block(document, scenario.test_case_id)
    if expected_block is None:
        write_golden_master(build_golden_master_document(), path)
        return

    if expected_block != actual_block:
        diff = unified_diff(expected_block.rstrip() + "\n", actual_block, scenario.test_case_id)
        raise AssertionError(
            f"{scenario.test_case_id} Golden Master mismatch. "
            "Run with --approve-golden-master to update.\n"
            f"{diff}"
        )


def approve_golden_master(
    actual: str,
    path: Path = DEFAULT_GOLDEN_PATH,
    *,
    auto_create: bool = True,
    force_update: bool = False,
) -> str:
    """Create, compare, or update the golden master baseline.

    Args:
        actual: Captured solver output document.
        path: Target golden master file path.
        auto_create: When ``True``, write baseline if the file is missing.
        force_update: When ``True``, overwrite baseline on mismatch.

    Returns:
        ``"created"``, ``"updated"``, or ``"unchanged"``.

    Raises:
        AssertionError: When baseline is missing (``auto_create=False``) or differs.
    """
    expected = read_golden_master(path)

    if expected is None:
        if not auto_create:
            raise AssertionError(f"Golden master missing: {path}")
        write_golden_master(actual, path)
        return "created"

    if expected == actual:
        return "unchanged"

    if force_update:
        write_golden_master(actual, path)
        return "updated"

    diff = unified_diff(expected, actual, path.name)
    raise AssertionError(f"Golden Master mismatch: {path}\n{diff}")


def approve_or_compare(*, approve: bool, path: Path = DEFAULT_GOLDEN_PATH) -> None:
    """Create, compare, or update the full golden master baseline.

    Args:
        approve: When ``True``, overwrite the baseline with current output.
        path: Target golden master file path.

    Raises:
        AssertionError: When actual output differs from the baseline.
    """
    actual = build_golden_master_document()
    approve_golden_master(
        actual,
        path,
        auto_create=True,
        force_update=approve,
    )
