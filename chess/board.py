import numpy as np
import pieces

team1 = "Black"
team2 = "White"

board_type1 = np.array([
    [pieces.Rook(team2, np.array([0, 0])), pieces.Knight(team2, np.array([0, 1])), pieces.Bishop(team2, np.array([0, 2])), pieces.King(team2, np.array([0, 3])), pieces.Queen(team2, np.array([0, 4])), pieces.Bishop(team2, np.array([0, 5])), pieces.Knight(team2, np.array([0, 6])), pieces.Rook(team2, np.array([0, 7]))],
    [pieces.Pawn(team2, np.array([1, 0])), pieces.Pawn(team2, np.array([1, 1])), pieces.Pawn(team2, np.array([1, 2])), pieces.Pawn(team2, np.array([1, 3])), pieces.Pawn(team2, np.array([1, 4])), pieces.Pawn(team2, np.array([1, 5])), pieces.Pawn(team2, np.array([1, 6])), pieces.Pawn(team2, np.array([1, 7]))],
    [pieces.NoPiece(np.array([2, 0])), pieces.NoPiece(np.array([2, 1])), pieces.NoPiece(np.array([2, 2])), pieces.NoPiece(np.array([2, 3])), pieces.NoPiece( np.array([2, 4])), pieces.NoPiece(np.array([2, 5])), pieces.NoPiece(np.array([2, 6])), pieces.NoPiece(np.array([2, 7]))],
    [pieces.NoPiece(np.array([3, 0])), pieces.NoPiece(np.array([3, 1])), pieces.NoPiece(np.array([3, 2])), pieces.NoPiece(np.array([3, 3])), pieces.NoPiece( np.array([3, 4])), pieces.NoPiece(np.array([3, 5])), pieces.NoPiece(np.array([3, 6])), pieces.NoPiece(np.array([3, 7]))],
    [pieces.NoPiece(np.array([4, 0])), pieces.NoPiece(np.array([4, 1])), pieces.NoPiece(np.array([4, 2])), pieces.NoPiece(np.array([4, 3])), pieces.NoPiece( np.array([4, 4])), pieces.NoPiece(np.array([4, 5])), pieces.NoPiece(np.array([4, 6])), pieces.NoPiece(np.array([4, 7]))],
    [pieces.NoPiece(np.array([5, 0])), pieces.NoPiece(np.array([5, 1])), pieces.NoPiece(np.array([5, 2])), pieces.NoPiece(np.array([5, 3])), pieces.NoPiece( np.array([5, 4])), pieces.NoPiece(np.array([5, 5])), pieces.NoPiece(np.array([5, 6])), pieces.NoPiece(np.array([5, 7]))],
    [pieces.Pawn(team1, np.array([6, 0])), pieces.Pawn(team1, np.array([6, 1])), pieces.Pawn(team1, np.array([6, 2])), pieces.Pawn(team1, np.array([6, 3])), pieces.Pawn(team1, np.array([6, 4])), pieces.Pawn(team1, np.array([6, 5])), pieces.Pawn(team1, np.array([6, 6])), pieces.Pawn(team1, np.array([6, 7]))],
    [pieces.Rook(team1, np.array([7, 0])), pieces.Knight(team1, np.array([7, 1])), pieces.Bishop(team1, np.array([7, 2])), pieces.King(team1, np.array([7, 3])), pieces.Queen(team1, np.array([7, 4])), pieces.Bishop(team1, np.array([7, 5])), pieces.Knight(team1, np.array([7, 6])), pieces.Rook(team1, np.array([7, 7]))]
    ])

board_type2 = np.array([
    [pieces.Rook(team1, np.array([0, 0])), pieces.Knight(team1, np.array([0, 1])), pieces.Bishop(team1, np.array([0, 2])), pieces.Queen(team1, np.array([0, 3])), pieces.King(team1, np.array([0, 4])), pieces.Bishop(team1, np.array([0, 5])), pieces.Knight(team1, np.array([0, 6])), pieces.Rook(team1, np.array([0, 7]))],
    [pieces.Pawn(team1, np.array([1, 0])), pieces.Pawn(team1, np.array([1, 1])), pieces.Pawn(team1, np.array([1, 2])), pieces.Pawn(team1, np.array([1, 3])), pieces.Pawn(team1, np.array([1, 4])), pieces.Pawn(team1, np.array([1, 5])), pieces.Pawn(team1, np.array([1, 6])), pieces.Pawn(team1, np.array([1, 7]))],
    [pieces.NoPiece(np.array([2, 0])), pieces.NoPiece(np.array([2, 1])), pieces.NoPiece(np.array([2, 2])), pieces.NoPiece(np.array([2, 3])), pieces.NoPiece( np.array([2, 4])), pieces.NoPiece(np.array([2, 5])), pieces.NoPiece(np.array([2, 6])), pieces.NoPiece(np.array([2, 7]))],
    [pieces.NoPiece(np.array([3, 0])), pieces.NoPiece(np.array([3, 1])), pieces.NoPiece(np.array([3, 2])), pieces.NoPiece(np.array([3, 3])), pieces.NoPiece( np.array([3, 4])), pieces.NoPiece(np.array([3, 5])), pieces.NoPiece(np.array([3, 6])), pieces.NoPiece(np.array([3, 7]))],
    [pieces.NoPiece(np.array([4, 0])), pieces.NoPiece(np.array([4, 1])), pieces.NoPiece(np.array([4, 2])), pieces.NoPiece(np.array([4, 3])), pieces.NoPiece( np.array([4, 4])), pieces.NoPiece(np.array([4, 5])), pieces.NoPiece(np.array([4, 6])), pieces.NoPiece(np.array([4, 7]))],
    [pieces.NoPiece(np.array([5, 0])), pieces.NoPiece(np.array([5, 1])), pieces.NoPiece(np.array([5, 2])), pieces.NoPiece(np.array([5, 3])), pieces.NoPiece( np.array([5, 4])), pieces.NoPiece(np.array([5, 5])), pieces.NoPiece(np.array([5, 6])), pieces.NoPiece(np.array([5, 7]))],
    [pieces.Pawn(team2, np.array([6, 0])), pieces.Pawn(team2, np.array([6, 1])), pieces.Pawn(team2, np.array([6, 2])), pieces.Pawn(team2, np.array([6, 3])), pieces.Pawn(team2, np.array([6, 4])), pieces.Pawn(team2, np.array([6, 5])), pieces.Pawn(team2, np.array([6, 6])), pieces.Pawn(team2, np.array([6, 7]))],
    [pieces.Rook(team2, np.array([7, 0])), pieces.Knight(team2, np.array([7, 1])), pieces.Bishop(team2, np.array([7, 2])), pieces.Queen(team2, np.array([7, 3])), pieces.King(team2, np.array([7, 4])), pieces.Bishop(team2, np.array([7, 5])), pieces.Knight(team2, np.array([7, 6])), pieces.Rook(team2, np.array([7, 7]))]
    ])

class board:
    def __init__(self, board_type) -> None:
        if board_type == 1:
            self.board_state = board_type1
        elif board_type==2:
            self.board_state = board_type2
        else:
            print("board_type can only be one of [1, 2]")
            exit()
        # White always starts playing in chess
        self.player_to_move = team2

    def move(self, board_state) -> np.array:
        """
        Returns all moves (possible or not). 
        The board class will filter the correct moves.
        """
        