# games/four_in_a_row/constants.py

# Game Rules
BOARD_ROWS = 6
BOARD_COLS = 7
WIN_SEQUENCE = 4

# Symbols
SYMBOL_P1 = "X"
SYMBOL_P2 = "O"
EMPTY_CELL = None

# Visual Configuration
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
CELL_SIZE = SCREEN_WIDTH // BOARD_COLS
HALF_SCREEN = SCREEN_WIDTH // 2