from .constants_TTT import BOARD_ROWS, BOARD_COLS, EMPTY_CELL


def create_board():
    """
    Creates an empty Tic Tac Toe board.
    """
    return [
        [EMPTY_CELL for _ in range(BOARD_COLS)]
        for _ in range(BOARD_ROWS)
    ]


def is_cell_empty(board, row, col):
    """
    Check if a specific cell is empty.
    row, col are 1-based indexes.
    """
    return board[row - 1][col - 1] == EMPTY_CELL