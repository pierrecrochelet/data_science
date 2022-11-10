import sys
sys.path.append("../core")
from chess_action import ChessAction
import numpy as np
import pieces

class ChessRules():

    @staticmethod
    def is_legal_move(cstate, action, player):
        """
        
        """

        action = action.get_action_as_dict()

        if state.get_next_player == player:
            if state.get_board().get_cell_team(action["from_cell"][0], action["from_cell"][1])==player.team:
                effective_moves = ChessRules.get_effective_cell_moves(state, action["from_cell"][0], action["from_cell"][1])
                if effective_moves and action["to_cell"] in effective_moves:
                    return True
                return False
            return False
        return False

    @staticmethod
    def get_effective_cell_moves(state, x_coordinate, y_coordinate):
        """
        
        """
        board = state.get_board()
        moves = board[x_coordinate, y_coordinate].move(board.board_state)
        return moves

    @staticmethod
    def act(state, action, player):
        """
        
        """

        if ChessRules.is_legal_move(state, action, player):
            return ChessRules.make_move(state, action, player)
        else:
            return False

    @staticmethod
    def make_move(state, action, player):
        """
        
        """

        board = state.get_board()
        action = action.get_action_as_dict()
        reward = 0

        from_x = action["from_cell"][0]
        from_y = action["from_cell"][1]
        to_x = action["to_cell"][0]
        to_y = action["to_cell"][1]
        team = board.board_state[from_x, from_y].team

        captured_pieces = ChessRules.captured(board, to_x, to_y, player)
        state.captured = captured_pieces
        if board.board_state[from_x, from_y].name=="pawn":
            board.fill_cell(to_x, to_y, pieces.Pawn(team=team, position=np.array([to_x, to_y])))
        elif board.board_state[from_x, from_y].name=="rook":
            board.fill_cell(to_x, to_y, pieces.Rook(team=team, position=np.array([to_x, to_y])))
        board.empty_cell(from_x, from_y)
        board.fill_cell()

