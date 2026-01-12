import turtle
from tkinter import messagebox
from utils.constants import SYMBOL_X, SYMBOL_O, EMPTY_CELL
from players.player_factory import choose_players
from players.human_player import HumanPlayer
from games.tic_tac_toe.gui import draw_x, draw_o, mark_winner, setup_gui, draw_board
from storage.save_load import save_current_state, load_unfinished_game, delete_save
from storage.history import save_game_result

# Added "busy": False to the state to track input locking
state = {"board": None, "p1": None, "p2": None, "current": None, "over": False, "busy": False}


def game_loop():
    setup_gui()
    draw_board()

    # Setup data + Check for saved game
    saved_data = load_unfinished_game()
    if saved_data and turtle.textinput("Resume Game?", "Found an unfinished game. Load it? (y/n)") in ["y", "Y"]:
        state["board"] = saved_data["board"]
        turn_symbol = saved_data["turn"]
        state["p1"], state["p2"] = choose_players()
        state["current"] = state["p1"] if turn_symbol == state["p1"].symbol else state["p2"]
        print("Game Loaded Successfully.")

        # Redraw loaded pieces
        for r in range(3):
            for c in range(3):
                if state["board"][r][c] == SYMBOL_X:
                    draw_x(r + 1, c + 1)
                elif state["board"][r][c] == SYMBOL_O:
                    draw_o(r + 1, c + 1)
    else:
        state["board"] = [[EMPTY_CELL for _ in range(3)] for _ in range(3)]
        state["p1"], state["p2"] = choose_players()
        state["current"] = state["p1"]

    state["over"] = False
    state["busy"] = False  # Input is allowed initially

    turtle.onscreenclick(handle_click)

    # If Player 1 is a computer, lock input immediately and trigger its move
    if not isinstance(state["current"], HumanPlayer):
        state["busy"] = True
        turtle.ontimer(ai_turn, 500)

    turtle.mainloop()


def handle_click(x, y):
    # 1. Check if game is busy, over, or not human turn
    # This prevents the "skip turn" bug by ignoring clicks while processing
    if state["busy"] or state["over"] or not isinstance(state["current"], HumanPlayer):
        return

    # 2. Lock input immediately so subsequent fast clicks are ignored
    state["busy"] = True

    col, row = int((x + 300) // 200), int((300 - y) // 200)

    # 3. Validate move
    if 0 <= row < 3 and 0 <= col < 3 and state["board"][row][col] == EMPTY_CELL:
        execute_move(row, col)
    else:
        # If click was invalid (e.g., occupied cell), unlock so user can try again
        state["busy"] = False


def ai_turn():
    if state["over"]: return

    # 1. Get the move
    move = state["current"].get_move(state["board"])

    # 2. FIX: Check if move is valid before accessing indices
    if move:
        execute_move(move[0], move[1])
    else:
        # Edge Case: AI couldn't find a move (board full?)
        # Just in case finish() wasn't called yet
        if all(cell != EMPTY_CELL for row in state["board"] for cell in row):
            finish("It's a Draw!")

def execute_move(r, c):
    p = state["current"]
    state["board"][r][c] = p.symbol

    if p.symbol == SYMBOL_X:
        draw_x(r + 1, c + 1)
    else:
        draw_o(r + 1, c + 1)

    win = check_winner(state["board"], p.symbol)
    if win:
        mark_winner(*win)
        finish(f"{p.name} Wins!")
    elif all(cell != EMPTY_CELL for row in state["board"] for cell in row):
        finish("It's a Draw!")
    else:
        # Switch turn
        state["current"] = state["p2"] if p == state["p1"] else state["p1"]
        save_current_state(state["board"], state["current"].symbol)

        # CONTROL FLOW: Check who plays next
        if isinstance(state["current"], HumanPlayer):
            # If next is Human, unlock the "busy" flag so they can click
            state["busy"] = False
        else:
            # If next is Computer, keep "busy" True (locked) and schedule move
            state["busy"] = True
            turtle.ontimer(ai_turn, 500)


def finish(msg):
    state["over"] = True
    messagebox.showinfo("Game Over", msg)

    # Save result
    save_game_result(state["p1"].name, state["p2"].name, state["current"].name if "Wins" in msg else "Draw")

    # Delete the temp save
    delete_save()
    print("Game Over. Closing.")
    turtle.bye()


 # b = board, s = symbol
def check_winner(b, s):
    for i in range(3):
        if all(b[i][j] == s for j in range(3)): return (i + 1, 1, i + 1, 3)
        if all(b[j][i] == s for j in range(3)): return (1, i + 1, 3, i + 1)
    if all(b[i][i] == s for i in range(3)): return (1, 1, 3, 3)
    if all(b[i][2 - i] == s for i in range(3)): return (1, 3, 3, 1)
    return None