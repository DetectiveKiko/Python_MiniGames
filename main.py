import turtle
from games.tic_tac_toe.game_logic import game_loop as play_ttt
from games.four_in_a_row.game_logic import game_loop as play_four

def main():
    screen = turtle.Screen()
    screen.title("Python Game Hub")
    screen.bgcolor("gray")

    # Choice menu
    choice = screen.textinput("Game Menu",
                              "Choose a game:\n1. Tic-Tac-Toe\n2. Four in a Row\n\nType 'exit' to quit")

    if choice == "1":
        print("Launching Tic-Tac-Toe...")
        play_ttt()
    elif choice == "2":
        print("Launching Four in a Row...")
        play_four()
    elif choice == "exit" or choice is None:
        print("Goodbye!")
        turtle.bye()
    else:
        # If they type something else, restart main
        main()

if __name__ == "__main__":
    main()