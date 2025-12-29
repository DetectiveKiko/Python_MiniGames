# games/four_in_a_row/board.py

from games.four_in_a_row.constants import (
    BOARD_ROWS, BOARD_COLS, EMPTY_CELL, WIN_SEQUENCE
)

class FourInARowBoard:
    def __init__(self):
        """Initializes a 6x7 grid filled with EMPTY_CELL."""
        self.grid = [[EMPTY_CELL for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

    def get_open_row(self, col):
        """Returns the bottom-most empty row index in a column, or None if full."""
        for r in range(BOARD_ROWS):
            if self.grid[r][col] == EMPTY_CELL:
                return r
        return None

    def place_piece(self, row, col, symbol):
        """Updates the grid logically."""
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            self.grid[row][col] = symbol

    def is_full(self):
        """Checks if the board is completely full (draw condition)."""
        # Only need to check the top row
        return all(self.grid[BOARD_ROWS - 1][c] != EMPTY_CELL for c in range(BOARD_COLS))

    def check_winner(self, symbol):
        """Checks all 4 directions for a sequence of 4."""
        # Horizontal
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS - 3):
                if all(self.grid[r][c+i] == symbol for i in range(WIN_SEQUENCE)):
                    return True
        # Vertical
        for r in range(BOARD_ROWS - 3):
            for c in range(BOARD_COLS):
                if all(self.grid[r+i][c] == symbol for i in range(WIN_SEQUENCE)):
                    return True
        # Diagonal (Positive Slope /)
        for r in range(BOARD_ROWS - 3):
            for c in range(BOARD_COLS - 3):
                if all(self.grid[r+i][c+i] == symbol for i in range(WIN_SEQUENCE)):
                    return True
        # Diagonal (Negative Slope \)
        for r in range(3, BOARD_ROWS):
            for c in range(BOARD_COLS - 3):
                if all(self.grid[r-i][c+i] == symbol for i in range(WIN_SEQUENCE)):
                    return True
        return False