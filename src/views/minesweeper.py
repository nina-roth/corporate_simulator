import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox,
    QVBoxLayout
)
from PyQt5.QtCore import Qt


class Cell(QPushButton):
    def __init__(self, x, y, parent):
        super().__init__()
        self.x = x
        self.y = y
        self.parent = parent
        self.setFixedSize(30, 30)
        # Change default style to make unrevealed cells look less flat, and more clickable
        self.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                border: 2px solid #999;
                border-style: outset;
                background-color: #CCC;
            }
            QPushButton:hover {
                background-color: #BBB;
            }
        """)
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent_mines = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.reveal_cell(self)
        elif event.button() == Qt.RightButton:
            self.parent.toggle_flag(self)


class Minesweeper(QWidget):
    def __init__(self, difficulty: str = "easy", params: dict = {"rows": 9, "cols": 9, "num_mines": 10}):
        super().__init__()
        self.setWindowTitle("Minesweeper")

        # Create a container widget for the grid so that the view doesn't stretch
        self.container = QWidget()

        if difficulty is not None:
            difficulty = difficulty.lower()
            if difficulty == "easy":
                self.rows, self.cols, self.num_mines = 9, 9, 10
            elif difficulty == "intermediate":
                self.rows, self.cols, self.num_mines = 16, 16, 40
            elif difficulty == "expert":
                self.rows, self.cols, self.num_mines = 16, 30, 99
            else:
                raise ValueError(f"Unknown difficulty level: '{difficulty}'")
        else:
            if params is None:
                raise ValueError("Either 'difficulty' or 'params' must be provided.")
            self.rows = params["rows"]
            self.cols = params["cols"]
            self.num_mines = params["num_mines"]

        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.container.setLayout(self.grid)

        # Create a main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.container, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

        self.init_board()

    def init_board(self):
        self.cells = []
        for x in range(self.rows):
            row = []
            for y in range(self.cols):
                cell = Cell(x, y, self)
                self.grid.addWidget(cell, x, y)
                row.append(cell)
            self.cells.append(row)

        self.place_mines()
        self.calculate_adjacency()

    def place_mines(self):
        positions = [(x, y) for x in range(self.rows) for y in range(self.cols)]
        for x, y in random.sample(positions, self.num_mines):
            self.cells[x][y].is_mine = True

    def calculate_adjacency(self):
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.cells[x][y]
                if cell.is_mine:
                    continue
                mines = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.rows and 0 <= ny < self.cols:
                            if self.cells[nx][ny].is_mine:
                                mines += 1
                cell.adjacent_mines = mines

    def reveal_cell(self, cell):
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        cell.setDisabled(True)

        # Make revealed cells look flat
        base_style = "QPushButton { font-weight: bold; border: 1px solid #999; background-color: #EEE; }"

        if cell.is_mine:
            cell.setText("💣")
            cell.setStyleSheet(base_style + "background-color: red;")
            self.game_over(won=False)
            return

        if cell.adjacent_mines > 0:
            cell.setText(str(cell.adjacent_mines))
            cell.setStyleSheet(base_style)
        else:
            cell.setStyleSheet(base_style)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cell.x + dx, cell.y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols:
                        neighbor = self.cells[nx][ny]
                        if not neighbor.revealed:
                            self.reveal_cell(neighbor)

        self.check_win()

    def toggle_flag(self, cell):
        if cell.revealed:
            return
        if not cell.flagged:
            cell.setText("🚩")
            cell.flagged = True
        else:
            cell.setText("")
            cell.flagged = False

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.revealed:
                    return
        self.game_over(won=True)

    def game_over(self, won):
        for row in self.cells:
            for cell in row:
                cell.setDisabled(True)
                if cell.is_mine and not cell.revealed:
                    cell.setText("💣")

        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText("🎉 You won!" if won else "💥 You hit a mine!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Minesweeper(difficulty="intermediate")  # or "intermediate", "expert"
    window.show()
    sys.exit(app.exec_())
