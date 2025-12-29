"""
Base Player Class
Defines the shared properties and interface for all player types.
"""

class Player:
    def __init__(self, name, symbol):
        """
        Initializes a player with a name and a symbol (X or O).
        """
        self.name = name
        self.symbol = symbol

    def get_move(self, board, **kwargs):
        """
        Abstract method to be implemented by subclasses.
        - HumanPlayer returns None (handled by clicks).
        - ComputerPlayer returns (row, col).
        """
        raise NotImplementedError("Subclasses must implement get_move")

    def __repr__(self):
        """Returns a string representation of the player object."""
        return f"{self.__class__.__name__}(Name: {self.name}, Symbol: {self.symbol})"