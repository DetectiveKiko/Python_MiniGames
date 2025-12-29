import json
import os

SAVE_FILE = "current_game.json"

def save_current_state(board, current_symbol):
    """Saves the ongoing game state to a JSON file."""
    data = {
        "board": board,
        "turn": current_symbol
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_unfinished_game():
    """Loads the board and turn if a save file exists."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return None

def delete_save():
    """Removes the save file once the game is finished."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)