import random
import copy
from players.player import Player

# Import Tic-Tac-Toe constants
from utils.constants import (
    EMPTY_CELL as TTT_EMPTY,
    SYMBOL_X,
    SYMBOL_O
)

# Import Four in a Row constants
from games.four_in_a_row.constants_4IAR import (
    BOARD_COLS,
    BOARD_ROWS,
    EMPTY_CELL as FOUR_EMPTY,
    SYMBOL_P1,
    SYMBOL_P2,
    WIN_SEQUENCE
)


# --- TIC-TAC-TOE AI ---

class RandomComputerPlayer(Player):
    """The 'Stupid' AI for Tic-Tac-Toe."""

    def get_move(self, board, **kwargs):
        available = [(r, c) for r in range(3) for c in range(3) if board[r][c] == TTT_EMPTY]
        return random.choice(available) if available else None


class SmartComputerPlayer(Player):
    """The 'Smart' AI for Tic-Tac-Toe using Minimax."""

    def get_move(self, board, **kwargs):
        best_score = -float('inf')
        move = None
        valid_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == TTT_EMPTY]
        if not valid_moves:
            return None
        for r in range(3):
            for c in range(3):
                if board[r][c] == TTT_EMPTY:
                    board[r][c] = self.symbol
                    score = self.minimax(board, 0, False)
                    board[r][c] = TTT_EMPTY
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        if move is None:
            return random.choice(valid_moves)

        return move

    def minimax(self, board, depth, is_maximizing):
        if self.check_win(board, self.symbol): return 10 - depth
        opponent = SYMBOL_O if self.symbol == SYMBOL_X else SYMBOL_X
        if self.check_win(board, opponent): return depth - 10
        if all(cell != TTT_EMPTY for row in board for cell in row): return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == TTT_EMPTY:
                        board[r][c] = self.symbol
                        score = self.minimax(board, depth + 1, False)
                        board[r][c] = TTT_EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == TTT_EMPTY:
                        board[r][c] = opponent
                        score = self.minimax(board, depth + 1, True)
                        board[r][c] = TTT_EMPTY
                        best_score = min(score, best_score)
            return best_score

    def check_win(self, b, s):
        for i in range(3):
            if all(b[i][j] == s for j in range(3)) or all(b[j][i] == s for j in range(3)): return True
        return all(b[i][i] == s for i in range(3)) or all(b[i][2 - i] == s for i in range(3))


# --- FOUR IN A ROW AI ---

import random
from players.player import Player
from games.four_in_a_row.constants_4IAR import (
    BOARD_ROWS, BOARD_COLS, EMPTY_CELL, SYMBOL_P1, SYMBOL_P2
)


class RandomFourAI(Player):
    """
    The 'Stupid' AI.
    Strategy: Purely random. It identifies strictly valid columns
    (columns that are not full) and picks one.
    """

    def get_move(self, board, **kwargs):
        # Identify valid columns (where the top row is empty)
        valid_cols = [c for c in range(BOARD_COLS) if board[BOARD_ROWS - 1][c] == EMPTY_CELL]

        # Return a random choice or None if board is full
        return random.choice(valid_cols) if valid_cols else None


class SmartFourAI(Player):
    """
    The 'Smart' AI.
    Strategy: Minimax Algorithm with Alpha-Beta Pruning.
    It simulates moves 4 steps into the future to find the best outcome.
    Includes a fail-safe to prevent freezing.
    """

    def get_move(self, board, **kwargs):
        # 1. Identify valid moves first
        valid_locations = [c for c in range(BOARD_COLS) if board[BOARD_ROWS - 1][c] == EMPTY_CELL]

        if not valid_locations:
            return None

        # 2. Run Minimax (Depth 4 is the sweet spot for speed vs intelligence)
        try:
            # Alpha starts at -infinity, Beta at +infinity
            col, score = self.minimax(board, 4, -float('inf'), float('inf'), True)
        except Exception as e:
            print(f"AI Error: {e}")
            col = None

        # 3. Fail-Safe: If Minimax returns None (e.g., all moves look equal/bad), pick random
        if col is None or col not in valid_locations:
            return random.choice(valid_locations)

        return col

    def minimax(self, board, depth, alpha, beta, maximizing):
        """
        Recursive function to score imaginary board states.
        Returns: (best_column, score)
        """
        valid_locations = [c for c in range(BOARD_COLS) if board[BOARD_ROWS - 1][c] == EMPTY_CELL]

        # Identify who is the opponent in this simulation
        opp_sym = SYMBOL_P1 if self.symbol == SYMBOL_P2 else SYMBOL_P2

        # --- Terminal Conditions (Base Cases) ---
        if self.check_win_sim(board, self.symbol):
            return (None, 1000000)  # AI Wins
        if self.check_win_sim(board, opp_sym):
            return (None, -1000000)  # Human Wins (Bad for AI)
        if len(valid_locations) == 0:
            return (None, 0)  # Draw
        if depth == 0:
            return (None, self.score_position(board, self.symbol))

        # --- Recursive Steps ---
        if maximizing:
            value = -float('inf')
            best_col = valid_locations[0]
            for col in valid_locations:
                # Create a temporary copy of the board logic
                temp_board = [row[:] for row in board]
                self.drop_piece_sim(temp_board, col, self.symbol)

                # Recursion
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)[1]

                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Pruning
            return best_col, value

        else:  # Minimizing (The Human's hypothetical turn)
            value = float('inf')
            best_col = valid_locations[0]
            for col in valid_locations:
                temp_board = [row[:] for row in board]
                self.drop_piece_sim(temp_board, col, opp_sym)

                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def drop_piece_sim(self, board, col, symbol):
        """Simulates gravity for the temporary board."""
        for r in range(BOARD_ROWS):
            if board[r][col] == EMPTY_CELL:
                board[r][col] = symbol
                return

    def score_position(self, board, symbol):
        """Heuristic to evaluate non-winning board states."""
        score = 0

        # Strategic Priority 1: Control the Center
        center_array = [board[r][BOARD_COLS // 2] for r in range(BOARD_ROWS)]
        center_count = center_array.count(symbol)
        score += center_count * 3

        # Strategic Priority 2: Create lines of 2 or 3
        # (This can be expanded for smarter offense)

        return score


    # b = board, s = symbol
    # r = row, c = column

    def check_win_sim(self, b, s):
        """Internal win checker for the simulation loops."""
        # Horizontal
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS - 3):
                if all(b[r][c + i] == s for i in range(4)): return True
        # Vertical
        for r in range(BOARD_ROWS - 3):
            for c in range(BOARD_COLS):
                if all(b[r + i][c] == s for i in range(4)): return True
        # Diagonal (/)
        for r in range(BOARD_ROWS - 3):
            for c in range(BOARD_COLS - 3):
                if all(b[r + i][c + i] == s for i in range(4)): return True
        # Diagonal (\)
        for r in range(3, BOARD_ROWS):
            for c in range(BOARD_COLS - 3):
                if all(b[r - i][c + i] == s for i in range(4)): return True
        return False