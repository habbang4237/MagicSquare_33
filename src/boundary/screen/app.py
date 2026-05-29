"""Application entry point for the Magic Square PyQt screen."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from boundary.puzzle_boundary import PuzzleBoundary
from boundary.screen.main_window import MagicSquareMainWindow
from control.solve_puzzle_use_case import SolvePuzzleUseCase


def main() -> None:
    """Start the Magic Square 4×4 desktop UI."""
    app = QApplication(sys.argv)
    boundary = PuzzleBoundary(use_case=SolvePuzzleUseCase())
    window = MagicSquareMainWindow(boundary)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
