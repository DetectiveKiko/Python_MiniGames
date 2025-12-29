import pickle
import os
from tkinter import filedialog, Tk

# This will store the path chosen by the user during the session
SELECTED_HISTORY_PATH = None


def get_history_path():
    """Opens a window to ask the user where to save the history file."""
    global SELECTED_HISTORY_PATH

    # If we already picked a path this session, just return it
    if SELECTED_HISTORY_PATH:
        return SELECTED_HISTORY_PATH

    # Hide the main tkinter root window
    root = Tk()
    root.withdraw()

    # Open the 'Save As' dialog
    path = filedialog.asksaveasfilename(
        title="Select where to save Game History",
        defaultextension=".pkl",
        filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
    )

    root.destroy()

    if path:
        SELECTED_HISTORY_PATH = path
        return path
    else:
        # Default fallback if they cancel
        return "game_history.pkl"


def save_game_result(player1_name, player2_name, winner_name):
    """Saves the result to the user-selected path."""
    path = get_history_path()
    history = load_history(path)

    result = {
        "p1": player1_name,
        "p2": player2_name,
        "winner": winner_name,
    }

    history.append(result)

    with open(path, "wb") as f:
        pickle.dump(history, f)
    print(f"History saved to: {path}")


def load_history(path=None):
    """Loads history from a specific path."""
    if not path:
        path = get_history_path()

    if not os.path.exists(path):
        return []

    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return []