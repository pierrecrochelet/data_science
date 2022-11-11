import numpy as np
from chess_player import ChessPlayer

class ChessState(object):

    def __init__(self, board, next_player=ChessPlayer(team="White"), latest_player=ChessPlayer(team="Black")) -> None:
        """The State of the Chess Game. It contains information regarding the game such as:
            - board          : The current board
            - score          : The game score
            - latest_move    : The latest performed action
            - latest_player  : The latest player
            - next_player    : The next player
            - captured       : The captured piece in the last move, can be None.
        Args:
            board (Board): The board game
            next_player (str, optional): The next or first player at the start. Defaults to White.
            latest_player (str, optional): The last player who played. Defaults to Black.
        """

        self.board = board
        self.latest_player = latest_player
        self.next_player = next_player
        self.latest_move = None
        self.captured = None
        self.score = {"White": 0, "Black": 0}

    def get_board(self):
        return self.board

    def set_board(self, new_board):
        self.board = new_board

    def get_latest_player(self):
        return self.latest_player

    def get_latest_move(self):
        return self.latest_move

    def get_next_player(self):
        return self.next_player

    def set_latest_move(self, action):
        self.latest_move = action

    def set_next_player(self, player):
        self.next_player = player

    def set_latest_player(self, player):
        self.latest_player = player

    def get_player_info(self, player):
        return {'score': self.score[player.team]}