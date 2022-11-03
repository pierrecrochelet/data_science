import pieces
import numpy as np

board_state = np.array([
    [pieces.NoPiece(np.array([0, 0])), pieces.NoPiece(np.array([0, 1])), pieces.NoPiece(np.array([0, 2])), pieces.NoPiece(np.array([0, 3])), pieces.NoPiece(np.array([0, 4])), pieces.NoPiece(np.array([0, 5])), pieces.NoPiece(np.array([0, 6])), pieces.NoPiece(np.array([0, 7]))],
    [pieces.Pawn("Black", np.array([1, 0])), pieces.Pawn("Black", np.array([1, 1])), pieces.Pawn("Black", np.array([1, 2])), pieces.Pawn("Black", np.array([1, 3])), pieces.Pawn("Black", np.array([1, 4])), pieces.Pawn("Black", np.array([1, 5])), pieces.Pawn("Black", np.array([1, 6])), pieces.Pawn("Black", np.array([1, 7]))],
    [pieces.NoPiece(np.array([2, 0])), pieces.Rook("White", np.array([2, 1])), pieces.NoPiece(np.array([2, 2])), pieces.NoPiece(np.array([2, 3])), pieces.NoPiece( np.array([2, 4])), pieces.NoPiece(np.array([2, 5])), pieces.NoPiece(np.array([2, 6])), pieces.NoPiece(np.array([2, 7]))],
    [pieces.NoPiece(np.array([3, 0])), pieces.NoPiece(np.array([3, 1])), pieces.NoPiece(np.array([3, 2])), pieces.NoPiece(np.array([3, 3])), pieces.NoPiece( np.array([3, 4])), pieces.NoPiece(np.array([3, 5])), pieces.NoPiece(np.array([3, 6])), pieces.NoPiece(np.array([3, 7]))],
    [pieces.NoPiece(np.array([4, 0])), pieces.NoPiece(np.array([4, 1])), pieces.NoPiece(np.array([4, 2])), pieces.NoPiece(np.array([4, 3])), pieces.NoPiece( np.array([4, 4])), pieces.NoPiece(np.array([4, 5])), pieces.NoPiece(np.array([4, 6])), pieces.NoPiece(np.array([4, 7]))],
    [pieces.NoPiece(np.array([5, 0])), pieces.NoPiece(np.array([5, 1])), pieces.NoPiece(np.array([5, 2])), pieces.NoPiece(np.array([5, 3])), pieces.NoPiece( np.array([5, 4])), pieces.NoPiece(np.array([5, 5])), pieces.NoPiece(np.array([5, 6])), pieces.NoPiece(np.array([5, 7]))],
    [pieces.Knight("White", np.array([6, 0])), pieces.Pawn("White", np.array([6, 1])), pieces.Pawn("White", np.array([6, 2])), pieces.Pawn("White", np.array([6, 3])), pieces.Pawn("White", np.array([6, 4])), pieces.Pawn("White", np.array([6, 5])), pieces.Pawn("White", np.array([6, 6])), pieces.Pawn("White", np.array([6, 7]))],
    [pieces.NoPiece(np.array([7, 0])), pieces.Pawn("White", np.array([7, 1])), pieces.Pawn("White", np.array([7, 2])), pieces.NoPiece(np.array([7, 3])), pieces.NoPiece( np.array([7, 4])), pieces.NoPiece(np.array([7, 5])), pieces.NoPiece(np.array([7, 6])), pieces.NoPiece(np.array([7, 7]))]
    ])

for i in range(0, 8):
    for j in range(0, 8):
        if board_state[i,j].name != "empty" and board_state[i,j].move(board_state).shape[0]!=0:
            print(f"{board_state[i,j].name} Piece at position {board_state[i,j].position} has the following moves: {board_state[i,j].move(board_state)} ")
