"""Main window for the 4×4 magic square puzzle screen."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QAbstractSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.error_response import ErrorResponse
from boundary.puzzle_boundary import PuzzleBoundary
from boundary.screen.grid_ui_constants import (
    CELL_FONT_POINT_SIZE,
    CELL_HEIGHT,
    CELL_MAX,
    CELL_MIN,
    CELL_WIDTH,
    GRID_DIMENSION,
    HEADER_FONT_POINT_SIZE,
    MAGIC_LINE_SUM,
)

VALID_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

_STYLE_SUCCESS = "color: #1b5e20; font-weight: bold; font-size: 14pt;"
_STYLE_ERROR = "color: #b71c1c; font-weight: bold; font-size: 14pt;"
_STYLE_HINT = "color: #616161; font-size: 11pt;"
_STYLE_CELL = (
    "QSpinBox {"
    f" font-size: {CELL_FONT_POINT_SIZE}pt;"
    " font-weight: bold;"
    " padding: 8px;"
    "}"
)
_STYLE_HIGHLIGHT = (
    "QSpinBox {"
    f" font-size: {CELL_FONT_POINT_SIZE}pt;"
    " font-weight: bold;"
    " padding: 8px;"
    " background-color: #e8f5e9;"
    " border: 2px solid #43a047;"
    "}"
)


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
        """Build grid, action buttons, and result label."""
        self.setWindowTitle("Magic Square 4x4")
        self.setMinimumSize(560, 640)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)

        title = QLabel("4×4 마방진 퍼즐")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        hint = QLabel(
            f"빈칸(0)은 정확히 2개입니다. 행·열·대각선 합 = {MAGIC_LINE_SUM}"
        )
        hint.setWordWrap(True)
        hint.setStyleSheet(_STYLE_HINT)
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)

        header_font = QFont()
        header_font.setPointSize(HEADER_FONT_POINT_SIZE)
        header_font.setBold(True)

        corner = QLabel("")
        corner.setFixedWidth(36)
        grid_layout.addWidget(corner, 0, 0)

        for col in range(GRID_DIMENSION):
            header = QLabel(str(col + 1))
            header.setFont(header_font)
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setStyleSheet("color: #424242;")
            header.setFixedWidth(CELL_WIDTH)
            grid_layout.addWidget(header, 0, col + 1)

        cell_font = QFont()
        cell_font.setPointSize(CELL_FONT_POINT_SIZE)
        cell_font.setBold(True)

        for row in range(GRID_DIMENSION):
            row_header = QLabel(str(row + 1))
            row_header.setFont(header_font)
            row_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_header.setStyleSheet("color: #424242;")
            row_header.setFixedWidth(36)
            grid_layout.addWidget(row_header, row + 1, 0)

            row_boxes: list[QSpinBox] = []
            for col in range(GRID_DIMENSION):
                spin = QSpinBox()
                spin.setRange(CELL_MIN, CELL_MAX)
                spin.setFont(cell_font)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
                spin.setFixedSize(CELL_WIDTH, CELL_HEIGHT)
                spin.setStyleSheet(_STYLE_CELL)
                spin.setValue(VALID_GRID[row][col])
                grid_layout.addWidget(spin, row + 1, col + 1)
                row_boxes.append(spin)
            self._spin_boxes.append(row_boxes)

        layout.addLayout(grid_layout)

        button_row = QHBoxLayout()
        solve_button = QPushButton("풀기")
        solve_button.setMinimumHeight(44)
        solve_button.setFont(QFont("", 12))
        solve_button.clicked.connect(self._on_solve_clicked)
        button_row.addWidget(solve_button)

        reset_button = QPushButton("초기화")
        reset_button.setMinimumHeight(44)
        reset_button.setFont(QFont("", 12))
        reset_button.clicked.connect(self._on_reset_clicked)
        button_row.addWidget(reset_button)
        layout.addLayout(button_row)

        self._result_label.setWordWrap(True)
        self._result_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self._result_label.setMinimumHeight(72)
        layout.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        """Read current spin-box values as ``int[4][4]``."""
        return [
            [self._spin_boxes[row][col].value() for col in range(GRID_DIMENSION)]
            for row in range(GRID_DIMENSION)
        ]

    def _clear_highlights(self) -> None:
        """Reset spin-box highlight styles."""
        for row_boxes in self._spin_boxes:
            for spin in row_boxes:
                spin.setStyleSheet(_STYLE_CELL)

    def _apply_solution(self, solution: list[int]) -> None:
        """Highlight solved cells and show placed values.

        Args:
            solution: ``int[6] = [r1, c1, n1, r2, c2, n2]`` (1-index).
        """
        self._clear_highlights()
        placements = (
            (solution[0], solution[1], solution[2]),
            (solution[3], solution[4], solution[5]),
        )
        for row_1, col_1, value in placements:
            row = row_1 - 1
            col = col_1 - 1
            spin = self._spin_boxes[row][col]
            spin.setValue(value)
            spin.setStyleSheet(_STYLE_HIGHLIGHT)

    def _on_reset_clicked(self) -> None:
        """Restore default puzzle grid and clear result state."""
        self._clear_highlights()
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._spin_boxes[row][col].setValue(VALID_GRID[row][col])
        self._result_label.setText("")
        self._result_label.setStyleSheet("")

    def _on_solve_clicked(self) -> None:
        """Submit grid to boundary and display solution or error message."""
        self._clear_highlights()
        result = self._boundary.receive(self._read_grid())
        if isinstance(result, ErrorResponse):
            self._result_label.setStyleSheet(_STYLE_ERROR)
            self._result_label.setText(f"오류: {result.message}")
            return

        self._apply_solution(result)
        formatted = ", ".join(str(value) for value in result)
        self._result_label.setStyleSheet(_STYLE_SUCCESS)
        self._result_label.setText(
            f"결과 (r1, c1, n1, r2, c2, n2): {formatted}"
        )
