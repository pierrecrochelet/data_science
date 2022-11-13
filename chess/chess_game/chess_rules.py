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
            state: object of ChessState, defines the state of the game
            action: object of ChessAction, defines the action with the from_cell and to_cell
            player: object of ChessPlayer, defines the player who moves next

        Returns:
            bool: True if the action is legal. False if not.
        """

        action = action.get_action_as_dict()

        if state.get_next_player() == player:
            if state.get_board().get_cell_team(action["from_cell"][0], action["from_cell"][1])==player.team:
                # If king is attacked and player is trying to move another piece
                # TO DO: player can move other piece if it intercepts the attack
                if ChessRules.is_king_attacked(state) and state.get_board().board_state[action["from_cell"]].name!="king":
                    return False
                # If king is moving towards attack
                if state.get_board().board_state[action["from_cell"]].name=="king" and ChessRules.is_cell_attacked(state, action["to_cell"][0], action["to_cell"][1], state.get_latest_player()):
                    return False
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
            state: object of ChessState, defines the state of the game
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell

        Returns:
            moves: np.array containing all the moves the piece at the specified coordinates can do
        """
        board = state.get_board()
        moves = board[x_coordinate, y_coordinate].move(board.board_state)
        return moves

    @staticmethod
    def is_king_attacked(state):
        """
        Check if in the current state, the king is attacker.

        Args:
            state: object of ChessState, defines the state of the game

        Returns:
            bool: True if the king is attacker. False if not.
        """
        board = state.get_board()
        next_player = state.get_next_player()

        # Get king coordinates
        for i in range(0, board.board_state.shape[0]):
            for j in range(0, board.board_state.shape[1]):
                if board.board_state[i,j].name=="king" and board.board_state[i,j].team==next_player.team:
                    king_position = np.array([i,j])
                    break
        # Get all other player actions
        other_player_actions = ChessRules.get_player_all_cases_actions(state, state.get_latest_player())
        for i in range(0, other_player_actions.shape[0]):
            action = other_player_actions[i].get_action_as_dict()
            # If one piece of other player can attack king
            if king_position==action["to_cell"]:
                return True
        # If no piece of other player can attack king
        return False

    @staticmethod
    def is_cell_attacked(state, x_coordinate, y_coordinate, player):
        """
        Checks if the cell can be attacked by the player

        Args:
            state: object of ChessState, defines the state of the game
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell
            player: object of ChessPlayer, defines the player who attacks the cell

        Returns:
            moves: np.array containing all the moves the piece at the specified coordinates can do
        """
        # Get all actions of the player
        player_actions = ChessRules.get_player_all_cases_actions(state, player)
        for i in range(0, player_actions.shape[0]):
            action = player_actions[i].get_action_as_dict()
            # If coordinate can be attacked
            if np.array([x_coordinate, y_coordinate])==action["to_cell"]:
                return True
        return False

    @staticmethod
    def act(state, action, player):
        """
        If the move is legal, call the make move function

        Args: 
            state: object of ChessState, defines the state of the game
            action: object of ChessAction, defines the action with the from_cell and to_cell
            player: object of ChessPlayer, defines the player who moves next

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
        else:
            captured_piece = None
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
        state.score[player.team] += reward
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
            moves = board.board_state[piece_position].move(board.board_state)
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
        if ChessRules.is_checkmate(state):
            return True
        if ChessRules.is_stalemate(state):
            return True
        # TO DO: Add the threefold rule implementation, returning True if the current state has already been seen 2 times (and is therefore the third)
        return False

    @staticmethod
    def is_stalemate(state):
        """
        Check if the given state is stalemate.

        Args:
            state: object of ChessState, 

        Returns:
            bool: True if the given state is stalemate. False if not.

        """
        board = state.get_board()
        next_player = state.get_next_player()
        latest_player = state.get_latest_player()
        actions = ChessRules.get_player_all_cases_actions(state, next_player)
        # No actions i.e. king is trapped behind other pieces
        if actions.shape[0]==0:
            return True
        for i in range(0, actions.shape[0]):
            action = actions[i].get_action_as_dict()
            # If player can move any other piece than king. They have to move it and it is not stalemate
            if board.board_state[action["from_cell"]].name!="king":
                return False
            # If player can only move king. Check if king is allowed to move
            else:
                # If king is allowed to move then no stalemate
                if not ChessRules.is_cell_attacked(state, action["to_cell"][0], action["to_cell"][1], latest_player):
                    return False
        # If none of the possible actions is allowed then stalemate
        return True
    
    @staticmethod
    def is_checkmate(state):
        """
        Check if the given state is checkmate.

        Args:
            state: object of ChessState, 

        Returns:
            bool: True if the given state is checkmate. False if not.
        """
        board = state.get_board()
        latest_player = state.get_latest_player()
        next_player = state.get_next_player()
        
        # Get opponent actions
        opponent_actions = ChessRules.get_player_all_cases_actions(state, latest_player)

        # get king position
        for i in range(0, board.board_state.shape[0]):
            for j in range(0, board.board_state.shape[1]):
                if board.board_state[i,j].name=="king" and board.board_state[i,j].team==next_player.team:
                    king_position = np.array([i,j])
                    king_moves = board.board_state[i,j].move(board.board_state)
                    break
        # Initialize number of free tiles as the king position + each chell where the king can move
        free_tiles = king_moves.shape[0]+1
        # Decrement free_tiles for each cell where the king could move but is attacked
        for move in king_moves:
            for k in range(0, opponent_actions.shape[0]):
                action = opponent_actions[k].get_action_as_dict()
                if action["to_cell"]==move:
                    free_tiles -=1
                    break
        # Decrement free_tile if the king position is attacked
        for k in range(0, opponent_actions.shape[0]):
            action = opponent_actions[k].get_action_as_dict()
            if action["to_cell"]==king_position:
                free_tiles -=1
                break
        # If king has no tile to move and is attacked and the attack is not blockable then it's checkmate
        # TO DO: add the check if the attack is blockable
        if free_tiles==0:
            return True
        return False




