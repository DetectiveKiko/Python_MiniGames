import turtle
from games.tic_tac_toe.game_logic import game_loop as play_ttt
from games.four_in_a_row.game_logic import game_loop as play_four
# Import storage modules to reset/set paths
from storage.history import get_history_path, SELECTED_HISTORY_PATH
from storage.save_load import get_save_path, SELECTED_SAVE_PATH
import storage.save_load as save_module
import storage.history as history_module


def main():
    screen = turtle.Screen()
    screen.title("Python Game Hub")
    screen.bgcolor("lightblue")

    while True:
        # Reset paths for a new game session so we don't overwrite previous game files
        save_module.SELECTED_SAVE_PATH = None

        choice = screen.textinput("Game Menu",
                                  "Choose a game:\n1. Tic-Tac-Toe\n2. Four in a Row\n\nType 'exit' to quit")

        # 1. Safety Check: Handle Cancel/None immediately
        if choice is None:
            print("Goodbye!")
            turtle.bye()
            break

        clean_choice = choice.strip().lower()

        if clean_choice == "exit":
            print("Goodbye!")
            turtle.bye()
            break

        elif clean_choice in ["1", "2"]:
            # 2. Ask for Save Paths NOW (before game starts)
            print("Setup: Please select your file locations.")

            # This ensures the user picks a file specific to THIS game session
            hist = get_history_path()
            save = get_save_path()

            print(f"History: {hist}")
            print(f"Save File: {save}")

            if clean_choice == "1":
                print("Launching Tic-Tac-Toe...")
                play_ttt()
            elif clean_choice == "2":
                print("Launching Four in a Row...")
                play_four()
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()