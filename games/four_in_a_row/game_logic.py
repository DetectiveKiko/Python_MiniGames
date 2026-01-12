import turtle
from tkinter import messagebox
from games.four_in_a_row.constants_4IAR import BOARD_COLS, CELL_SIZE, SYMBOL_P1, SYMBOL_P2
from games.four_in_a_row.gui import setup_gui, draw_board, drop_piece_visual, draw_slot
from games.four_in_a_row.board import FourInARowBoard
from players.player_factory import choose_players
from players.human_player import HumanPlayer
from storage.history import save_game_result
from storage.save_load import save_current_state, load_unfinished_game, delete_save

# Global state to manage game flow and safety locks
state = {
    "board_obj": None,
    "p1": None,
    "p2": None,
    "current": None,
    "over": False,
    "busy": False  # Crucial for preventing input during animations or AI processing
}


def game_loop():
    """Main entry point for Four in a Row."""
    setup_gui()
    draw_board()

    state["board_obj"] = FourInARowBoard()
    state["over"] = False
    state["busy"] = True  # Lock input until setup is fully complete

    # 1. Check for Saved Game BEFORE initializing new players
    saved_data = load_unfinished_game()

    if saved_data and turtle.textinput("Resume?", "Found an unfinished game. Load it? (y/n)") in ["y", "Y"]:
        state["board_obj"].grid = saved_data["board"]
        # Ask for names/modes once
        state["p1"], state["p2"] = choose_players(game_type="four")

        # Determine whose turn it is from the save
        turn_symbol = saved_data["turn"]
        state["current"] = state["p1"] if turn_symbol == state["p1"].symbol else state["p2"]

        # Visually redraw the pieces already on the board
        redraw_loaded_pieces()
        print("Game Loaded Successfully.")
    else:
        # Start a fresh game
        state["p1"], state["p2"] = choose_players(game_type="four")
        state["current"] = state["p1"]

    state["busy"] = False

    # Input Handling
    turtle.onscreenclick(handle_click)

    # Initial AI check (if Player 1 is a computer)
    check_ai_turn()

    turtle.mainloop()


def redraw_loaded_pieces():
    """Redraws the static board slots for a loaded game."""
    grid = state["board_obj"].grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            symbol = grid[r][c]
            if symbol == SYMBOL_P1:
                draw_slot(r, c, "yellow")
            elif symbol == SYMBOL_P2:
                draw_slot(r, c, "green")


def handle_click(x, y):
    """Processes human column selection based on x-coordinate."""
    # Safety Check: Ignore clicks if busy, game over, or not human turn
    if state["over"] or state["busy"] or not isinstance(state["current"], HumanPlayer):
        return

    # Based on your GUI setworldcoordinates(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    col = int(x // CELL_SIZE)

    if 0 <= col < BOARD_COLS:
        process_move(col)


def check_ai_turn():
    """Schedules the AI move if the current player is a computer."""
    if not state["over"] and not isinstance(state["current"], HumanPlayer):
        state["busy"] = True  # Lock input while AI thinks
        turtle.ontimer(ai_move, 500)


def ai_move():
    """Fetches move from computer player and executes it."""
    if state["over"]:
        return

    grid = state["board_obj"].grid
    move = state["current"].get_move(grid)

    # Handle both column-integer returns and coordinate-tuple returns
    col = move[0] if isinstance(move, (tuple, list)) else move

    if col is not None:
        process_move(col)


def process_move(col):
    """Executes the placement, animation, and turn-switching logic."""
    board = state["board_obj"]
    row = board.get_open_row(col)

    if row is None:
        # Column full: unlock so human can pick another one
        state["busy"] = False
        return

    # Lock state for the duration of the animation and logic processing
    state["busy"] = True
    player = state["current"]

    # Update Logic
    board.place_piece(row, col, player.symbol)

    # Update Visuals (Animation)
    color = "yellow" if player.symbol == SYMBOL_P1 else "green"
    drop_piece_visual(row, col, color)

    # Win/Draw Detection
    if board.check_winner(player.symbol):
        end_game(f"Winner: {player.name}")
    elif board.is_full():
        end_game("It's a Draw!")
    else:
        # Switch Turn
        state["current"] = state["p2"] if state["current"] == state["p1"] else state["p1"]

        # Save state for the NEXT turn
        save_current_state(board.grid, state["current"].symbol)

        # Unlock and check if the next player is AI
        state["busy"] = False
        check_ai_turn()


def end_game(msg):
    """Finalizes game session, updates history, and cleans up saves."""
    state["over"] = True
    messagebox.showinfo("Game Over", msg)

    # Save to history file
    winner = state["current"].name if "Winner" in msg else "Draw"
    save_game_result(state["p1"].name, state["p2"].name, winner)

    # Clean up temp files
    delete_save()

    print("Game Over. Closing.")
    turtle.bye()