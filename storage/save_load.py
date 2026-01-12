import json
import os
from tkinter import filedialog, Tk

# Global to store the path for the current session
SELECTED_SAVE_PATH = None


def get_save_path():
    global SELECTED_SAVE_PATH
    if SELECTED_SAVE_PATH:
        return SELECTED_SAVE_PATH

    root = Tk()
    root.withdraw()
    path = filedialog.asksaveasfilename(
        title="Select where to save Current Game State",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    root.destroy()

    if path:
        SELECTED_SAVE_PATH = path
    else:
        # FIX: Ensure it uses the ABSOLUTE path of the current folder
        # instead of just a loose filename
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # This goes up one level from 'storage' to the main project folder
        project_root = os.path.dirname(current_dir)
        SELECTED_SAVE_PATH = os.path.join(project_root, "current_game.json")

    return SELECTED_SAVE_PATH

def save_current_state(board, current_symbol):
    path = get_save_path() # Use the dynamic path
    data = {"board": board, "turn": current_symbol}
    with open(path, "w") as f:
        json.dump(data, f)

def load_unfinished_game():
    path = get_save_path() # Use the dynamic path
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return None
    return None

def delete_save():
    path = get_save_path() # Use the dynamic path
    if os.path.exists(path):
        os.remove(path)