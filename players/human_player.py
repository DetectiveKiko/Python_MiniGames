"""
Human Player Module
Handles input logic for human players.
"""
from players.player import Player


class HumanPlayer(Player):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)

    def get_move(self, board, **kwargs):
        """
        In the new click-based Tic-Tac-Toe, this method is a placeholder 
        because the game logic now listens for 'onscreenclick' events.

        However, for other games or terminal-based testing, it can 
        still be used to return coordinates.
        """
        # For our click-based Tic-Tac-Toe, we return None to let 
        # the event handler in game_logic.py take over.
        return None

    def __str__(self):
        return f"Human Player: {self.name} ({self.symbol})"