"""Main window for the 4×4 magic square puzzle screen."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.error_response import ErrorResponse
from boundary.puzzle_boundary import PuzzleBoundary

_GRID_DIMENSION = 4
_CELL_MIN = 0
_CELL_MAX = 16

VALID_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class MagicSquareMainWindow(QMainWindow):
    """4×4 spin grid wired to ``PuzzleBoundary.receive``."""

    def __init__(self, boundary: PuzzleBoundary) -> None:
        """Initialize window with injected boundary port.

        Args:
            boundary: Boundary entry point (validation + use case delegation).
        """
        super().__init__()
        self._boundary = boundary
        self._spin_boxes: list[list[QSpinBox]] = []
        self._result_label = QLabel("")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build grid, solve button, and result label."""
        self.setWindowTitle("Magic Square 4x4")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        grid_layout = QGridLayout()
        for row in range(_GRID_DIMENSION):
            row_boxes: list[QSpinBox] = []
            for col in range(_GRID_DIMENSION):
                spin = QSpinBox()
                spin.setRange(_CELL_MIN, _CELL_MAX)
                spin.setValue(VALID_GRID[row][col])
                grid_layout.addWidget(spin, row, col)
                row_boxes.append(spin)
            self._spin_boxes.append(row_boxes)
        layout.addLayout(grid_layout)

        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        layout.addWidget(solve_button)

        self._result_label.setWordWrap(True)
        layout.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        """Read current spin-box values as ``int[4][4]``."""
        return [
            [self._spin_boxes[row][col].value() for col in range(_GRID_DIMENSION)]
            for row in range(_GRID_DIMENSION)
        ]

    def _on_solve_clicked(self) -> None:
        """Submit grid to boundary and display solution or error message."""
        result = self._boundary.receive(self._read_grid())
        if isinstance(result, ErrorResponse):
            self._result_label.setText(f"오류: {result.message}")
            return
        formatted = ", ".join(str(value) for value in result)
        self._result_label.setText(
            f"결과 (r1, c1, n1, r2, c2, n2): {formatted}"
        )
