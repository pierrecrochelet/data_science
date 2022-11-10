import numpy as np

class State(object):

    def __init__(self, board, latest_player=None, latest_move=None, next_player=None) -> None:
        self.board = board
        self.latest_player = latest_player
        self.latest_move = latest_move
        self.next_player = next_player
        self.score = {-1: 0, 1: 0}

    def get_board(self):
        return self.board

    def get_latest_player(self):
        return self.latest_player

    def get_latest_move(self):
        return self.latest_move

    def get_next_player(self):
        return self.next_player