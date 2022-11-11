import sys
sys.path.append("../core")
from chess_action import ChessAction
import numpy as np
import pieces

class ChessRules():

    @staticmethod
    def is_legal_move(state, action, player):
        """
        Check if the action performed by the player is legal in the current state

        Args:
            state: object of ChessState, 
            action: object of ChessAction, defines the action with the from_cell and to_cell
            player: 

        Returns:
            bool: True if the action is legal. False if not.
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
        Returns all the moves doable by the piece on the cell

        Args:
            state: object of ChessState
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell

        Returns:
            moves: np.array containing all the moves the piece at the specified coordinates can do
        """
        board = state.get_board()
        moves = board[x_coordinate, y_coordinate].move(board.board_state)
        return moves

    @staticmethod
    def act(state, action, player):
        """
        If the move is legal, call the make move function

        Args: 
            state: object of ChessState, 
            action: object of ChessAction, defines the action with the from_cell and to_cell
            player: 

        Returns:
            bool: False if the move is not legal. a call to make_move otherwise.
        """

        if ChessRules.is_legal_move(state, action, player):
            return ChessRules.make_move(state, action, player)
        else:
            return False

    @staticmethod
    def make_move(state, action, player):
        """
        make the move and update the state

        Args:
            state: object of ChessState, 
            action: object of ChessAction, defines the action with the from_cell and to_cell
            player: 

        Return:
            ChessState: The new state of the game
            bool: True if the move lead to a position where the game is ended. False otherwise
        """

        board = state.get_board()
        action = action.get_action_as_dict()
        reward = 0

        from_x = action["from_cell"][0]
        from_y = action["from_cell"][1]
        to_x = action["to_cell"][0]
        to_y = action["to_cell"][1]
        team = board.board_state[from_x, from_y].team
        
        if board.board_state[to_x, to_y].name!="empty" and board.board_state[to_x, to_y].team!=team:
            captured_piece = board.board_state[to_x, to_y]
        state.captured = captured_piece
        if board.board_state[from_x, from_y].name=="pawn":
            board.fill_cell(to_x, to_y, pieces.Pawn(team=team, position=np.array([to_x, to_y])))
        elif board.board_state[from_x, from_y].name=="rook":
            board.fill_cell(to_x, to_y, pieces.Rook(team=team, position=np.array([to_x, to_y])))
        elif board.board_state[from_x, from_y].name=="knight":
            board.fill_cell(to_x, to_y, pieces.Knight(team=team, position=np.array([to_x, to_y])))
        elif board.board_state[from_x, from_y].name=="bishop":
            board.fill_cell(to_x, to_y, pieces.Bishop(team=team, position=np.array([to_x, to_y])))
        elif board.board_state[from_x, from_y].name=="queen":
            board.fill_cell(to_x, to_y, pieces.Queen(team=team, position=np.array([to_x, to_y])))
        elif board.board_state[from_x, from_y].name=="king":
            board.fill_cell(to_x, to_y, pieces.King(team=team, position=np.array([to_x, to_y])))
        board.empty_cell(from_x, from_y)
        if captured_piece:
            if captured_piece.name=="pawn":
                reward += 1
            elif captured_piece.name=="knight":
                reward += 3
            elif captured_piece.name=="bishop":
                reward += 3
            elif captured_piece.name=="rook":
                reward += 5
            elif captured_piece.name=="queen":
                reward += 9
        else:
            # TO DO: add the threefold rule implementation saving each board state
            pass 

        state.set_board(board)
        state.score[player] += reward
        state.set_latest_player(player)
        state.set_latest_move(action)
        done = ChessRules.is_end_game(state)
        return state, done

    @staticmethod
    def random_play(state, player):
        """
        Choose a random move for the player to play

        Args:
            state: object of ChessState, 
            action: object of ChessAction, defines the action with the from_cell and to_cell

        Returns:
            ChessAction: an action
        """
        import random
        print(f"Player, {player}")
        actions = ChessRules.get_player_all_cases_actions(state, player)
        choose = random.choice(actions)
        return choose

    @staticmethod
    def get_player_all_cases_actions(state, player):
        """
        Finds all possible actions for the player

        Args:
            state: object of ChessState, 
            action: object of ChessAction, defines the action with the from_cell and to_cell

        Returns:
            np.array: containing all the actions available for that player
        """
        board = state.get_board()
        actions = []
        all_pieces_positions = board.get_player_pieces_on_board(player.team)
        for piece_position in all_pieces_positions:
            moves = board[piece_position].move(board.board_state)
            for move in moves:
                actions.append(ChessAction(piece_position, move))
        return np.array(actions)

    @staticmethod
    def is_end_game(state):
        """
        Check if the given state is the last one for the current game.

        Args:
            state: object of ChessState, 


        Returns:
            bool: True if the given state is the final. False if not.

        """
        if ChessRules.is_stalemate(state):
            return True
        if ChessRules.checkmate(state):
            return True
        # TO DO: Add the threefold rule implementation, returning True if the current state has already been seen 2 times (and is therefore the third)
        return False

    @staticmethod
    def is_stalemate(state):
        """
        Check if the given state is the last one for the current game.

        Args:
            state: object of ChessState, 


        Returns:
            bool: True if the given state is stalemate. False if not.

        """
        next_player = state.get_next_player()

        actions = ChessRules.get_player_all_cases_actions(state, next_player)
        if len(actions)==0:
            return True
        return False
    
    @staticmethod
    def checkmate(state):
        """
        Check if the given state is the last one for the current game.

        Args:
            state: object of ChessState, 

        Returns:
            bool: True if the given state is checkmate. False if not.
        """
        board = state.get_board()
        last_player = state.get_last_player()
        next_player = state.get_next_player()
        
