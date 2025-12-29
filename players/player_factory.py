import turtle
from players.human_player import HumanPlayer
from players.computer_player import (
    RandomComputerPlayer, SmartComputerPlayer,
    RandomFourAI, SmartFourAI
)
from utils.constants import SYMBOL_X, SYMBOL_O
from games.four_in_a_row.constants import SYMBOL_P1, SYMBOL_P2


def choose_players(game_type="ttt"):
    screen = turtle.Screen()

    # Set symbols based on game type
    s1 = SYMBOL_P1 if game_type == "four" else SYMBOL_X
    s2 = SYMBOL_P2 if game_type == "four" else SYMBOL_O

    # 1. Ask for Player 1
    p1_name = screen.textinput("Player 1", f"Enter Name for Player 1 ({s1}):") or "Player 1"
    p1 = HumanPlayer(p1_name, s1)

    # 2. Ask Game Mode
    mode = screen.textinput("Game Mode", "Choose opponent:\n1. Human\n2. Computer")

    if mode == "1":
        p2_name = screen.textinput("Player 2", f"Enter Name for Player 2 ({s2}):") or "Player 2"
        p2 = HumanPlayer(p2_name, s2)
    else:
        # 3. Ask for AI Difficulty
        diff = screen.textinput("Difficulty", "Choose AI Level:\n1. Stupid (Random)\n2. Smart (Hard)")

        # Instantiate the correct AI based on the game type
        if game_type == "four":
            if diff == "2":
                p2 = SmartFourAI("Smart AI", s2)
            else:
                p2 = RandomFourAI("Stupid AI", s2)
        else:
            # Default to Tic-Tac-Toe AI
            if diff == "2":
                p2 = SmartComputerPlayer("Smart AI", s2)
            else:
                p2 = RandomComputerPlayer("Stupid AI", s2)

    return p1, p2