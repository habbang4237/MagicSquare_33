"""Generate or refresh ``tests/golden_master_expected.txt`` from live solver output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "tests"))

from golden_master.approve import DEFAULT_GOLDEN_PATH, approve_or_compare


def main() -> int:
    """Write Golden Master baseline from current Boundary output."""
    parser = argparse.ArgumentParser(
        description="Generate Golden Master expected output for GM-1.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GOLDEN_PATH,
        help="Target golden master file (default: tests/golden_master_expected.txt).",
    )
    args = parser.parse_args()
    approve_or_compare(approve=True, path=args.output)
    print(f"Golden Master written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
