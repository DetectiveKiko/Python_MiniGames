import turtle
from tkinter import messagebox
from games.four_in_a_row.constants import BOARD_COLS, CELL_SIZE
from games.four_in_a_row.gui import setup_gui, draw_board, drop_piece_visual
from games.four_in_a_row.board import FourInARowBoard
from players.player_factory import choose_players
from players.human_player import HumanPlayer
from storage.history import save_game_result
from storage.save_load import save_current_state, load_unfinished_game, delete_save

# Game State Dictionary
state = {
    "board_obj": None,
    "p1": None,
    "p2": None,
    "current": None,
    "over": False
}


def game_loop():
    """Main entry point for Four in a Row."""
    setup_gui()

    # 1. Setup Board Object
    state["board_obj"] = FourInARowBoard()

    # 2. Setup Players (Specify "four" to get the correct AI)
    state["p1"], state["p2"] = choose_players(game_type="four")
    state["current"] = state["p1"]
    state["over"] = False

    # 3. Check for Saved Game
    saved_data = load_unfinished_game()
    if saved_data:
        # Ask user if they want to resume
        res = turtle.textinput("Resume Game?", "Found an unfinished game. Load it? (y/n)")
        if res and res.lower() == "y":
            # Restore Board
            state["board_obj"].grid = saved_data["board"]
            # Restore Turn
            turn_symbol = saved_data["turn"]
            state["current"] = state["p1"] if turn_symbol == state["p1"].symbol else state["p2"]
            print("Game Loaded Successfully.")

    # Draw the board (whether new or loaded)
    draw_board()
    # If loaded, we need to redraw the existing pieces
    redraw_loaded_pieces()

    # Input Handling
    turtle.onscreenclick(handle_click)

    # Check for AI start
    check_ai_turn()

    turtle.mainloop()


def redraw_loaded_pieces():
    """Visually updates the board based on the internal grid state."""
    grid = state["board_obj"].grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            symbol = grid[r][c]
            if symbol is not None:
                drop_piece_visual(r, c, symbol)


def handle_click(x, y):
    """Processes human clicks."""
    if state["over"] or state["current"] is None:
        return
    if not isinstance(state["current"], HumanPlayer):
        return

    col = int(x // CELL_SIZE)
    if 0 <= col < BOARD_COLS:
        process_move(col)


def check_ai_turn():
    """Triggers AI move if it's currently the computer's turn."""
    if not state["over"] and state["current"] is not None:
        if not isinstance(state["current"], HumanPlayer):
            turtle.ontimer(ai_move, 500)


def ai_move():
    """Executes the computer's logic."""
    if state["over"]: return

    grid = state["board_obj"].grid
    # AI logic handles its own move selection
    move = state["current"].get_move(grid)

    # Safely extract column index
    if isinstance(move, (tuple, list)):
        col = move[0]
    else:
        col = move

    if col is not None:
        process_move(col)


def process_move(col):
    """Common logic for applying a move (Human or AI)."""
    board = state["board_obj"]
    row = board.get_open_row(col)

    if row is not None:
        # Update Logic & Visuals
        board.place_piece(row, col, state["current"].symbol)
        drop_piece_visual(row, col, state["current"].symbol)

        # SAVE STATE after every move
        save_current_state(board.grid, state["current"].symbol)  # Saves the CURRENT player's symbol who just moved?
        # Actually, usually better to save the NEXT player, but saving current allows us to know whose turn just finished.
        # Let's stick to saving the symbol of the player who is *about* to move next, 
        # or handle it carefully in load. 
        # Simplest: Save the symbol of the player whose turn it is *before* switching, 
        # wait, if we switch turn below, we should save the *new* current.

        if check_game_over(board):
            delete_save()  # Clean up save file on game over
            return

        switch_turn()
        # Save the state for the *next* player
        save_current_state(board.grid, state["current"].symbol)

        check_ai_turn()


def switch_turn():
    state["current"] = state["p2"] if state["current"] == state["p1"] else state["p1"]


def check_game_over(board):
    player = state["current"]
    if board.check_winner(player.symbol):
        end_game(f"Winner: {player.name}")
        return True
    elif board.is_full():
        end_game("It's a Draw!")
        return True
    return False


def end_game(msg):
    state["over"] = True
    messagebox.showinfo("Game Over", msg)

    # Save History
    winner = state["current"].name if "Winner" in msg else "Draw"
    # This calls your history.py which opens the dialog
    save_game_result(state["p1"].name, state["p2"].name, winner)

    turtle.bye()