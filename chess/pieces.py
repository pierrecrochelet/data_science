import numpy as np


"""
Mother class for all pieces including no piece (which i decided to define as a dummy useless piece)
"""
class Pieces():
    def __init__(self, team, position, name) -> None:
        self.team = team
        self.position = position
        self.name = name

    def move(self, board_state) -> np.array:
        """
        Returns all moves (possible or not). 
        The board class will filter the correct moves.
        """
        pass

"""
No Piece (represents most of the board)
"""
class NoPiece(Pieces):
    def __init__(self, position, team="None", name="empty") -> None:
        super().__init__(team, position, name)
    
    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        return np.array([])

"""
Pawn piece. Can move in a straight line and capture in diagonal.
"""
class Pawn(Pieces):
    def __init__(self, team, position, name="pawn") -> None:
        super().__init__(team, position, name)
        self.first_position = position
    
    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        # Initalize the moves which will be returned. Need to add a dummy move to be able to concatenate later
        moves = np.array([[-1, -1]], dtype=int)
        # If pawn goes from top to bottom
        if self.first_position[0]==1:
            # If tile in front +1 is empty
            if board_state[self.position[0]+1, self.position[1]].name=="empty":
                # Add advance in straight line +1
                moves = np.concatenate((moves, np.array([[self.position[0]+1, self.position[1]]])))

                # If pawn hasn't moved and tile in front +2
                if np.array_equal(self.position, self.first_position) and board_state[self.position[0]+2, self.position[1]].name=="empty":
                    # Add advance in straight line +2
                    moves = np.concatenate((moves, np.array([[self.position[0]+2, self.position[1]]])))
            
            # If pawn is not in left side border and tile on left diagonal+1 is occupied by ennemy piece
            if self.position[1]!=0 and board_state[self.position[0]+1, self.position[1]-1].name!="empty" and board_state[self.position[0]+1, self.position[1]-1].team!=self.team:
                # Add advance in left diagonal +1 
                moves = np.concatenate((moves, np.array([[self.position[0]+1, self.position[1]-1]])))
            
            # If pawn is not in right side border and tile on right diagonal+1 is occupied by ennemy piece
            if self.position[1]!=7 and board_state[self.position[0]+1, self.position[1]+1].name!="empty" and board_state[self.position[0]+1, self.position[1]+1].team!=self.team:
                # Add advance in right diagonal +1 
                moves = np.concatenate((moves, np.array([[self.position[0]+1, self.position[1]+1]])))

        # If pawn goes from bottom to top
        else:
            # If tile in front +1 is empty
            if board_state[self.position[0]-1, self.position[1]].name=="empty":
                # Add advance in straight line +1
                moves = np.concatenate((moves, np.array([[self.position[0]-1, self.position[1]]])))
            
                # If pawn hasn't moved and tile in front +2 is empty
                if np.array_equal(self.position, self.first_position) and board_state[self.position[0]-2, self.position[1]].name=="empty":
                    # Add advance in straight line +2
                    moves = np.concatenate((moves, np.array([[self.position[0]-2, self.position[1]]])))

            # If pawn is not in left side border and tile on left diagonal+1 is occupied by ennemy piece
            if self.position[1]!=0 and board_state[self.position[0]-1, self.position[1]-1].name!="empty" and board_state[self.position[0]-1, self.position[1]-1].team!=self.team:
                # Add advance in left diagonal+1
                moves = np.concatenate((moves, np.array([[self.position[0]-1, self.position[1]-1]])))
            
            # If pawn is not in right side border and tile on right diagonal+1 is occupied by ennemy piece
            if self.position[1]!=7 and board_state[self.position[0]-1, self.position[1]+1].name!="empty" and board_state[self.position[0]-1, self.position[1]+1].team!=self.team:
                # Add advance in right diagonal +1
                moves = np.concatenate((moves, np.array([[self.position[0]+1, self.position[1]+1]])))

        # Remove the dummy move that was added
        moves = np.delete(moves, 0, axis=0)
        return moves
    
"""
Rook piece. Can move in a straight line unlimited
"""
class Rook(Pieces):
    def __init__(self, team, position, name = "rook") -> None:
        super().__init__(team, position, name)

    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        # Initalize the moves which will be returned. Need to add a dummy move to be able to concatenate later
        moves = np.array([[-1, -1]], dtype=int)

        # Check moves from current position to top of the board
        for i in range(self.position[0]-1, -1, -1):
            # If tile is empty
            if board_state[i, self.position[1]].name=="empty":
                # Add empty tile and continue loop
                moves = np.concatenate((moves, np.array([[i, self.position[1]]])))
            # If tile is occupied by ennemy piece
            elif board_state[i, self.position[1]].team!=self.team:
                # Add ennemy occupied tile to move and stop loop as rook can jump pieces
                moves = np.concatenate((moves, np.array([[i, self.position[1]]])))
                break
            # If tile is occupied by allied piece
            else:
                # Stop the loop as rook cannot get on same piece as allied piece and cannot jump pieces
                break

        # Check moves from current position to bottom of the board
        for i in range(self.position[0]+1, 8):
            # If tile is empty
            if board_state[i, self.position[1]].name=="empty":
                # Add empty tile and continue loop
                moves = np.concatenate((moves, np.array([[i, self.position[1]]])))
            # If tile is occupied by ennemy piece
            elif board_state[i, self.position[1]].team!=self.team:
                # Add ennemy occupied tile to move and stop loop as rook can jump pieces
                moves = np.concatenate((moves, np.array([[i, self.position[1]]])))
                break
            # If tile is occupied by allied piece
            else:
                # Stop the loop as rook cannot get on same piece as allied piece and cannot jump pieces
                break

        # Check moves from current position to left side of the board
        for i in range(self.position[1]-1, -1, -1):
            # If tile is empty
            if board_state[self.position[0], i].name=="empty":
                # Add empty tile and continue loop
                moves = np.concatenate((moves, np.array([[self.position[0], i]])))
            # If tile is occupied by ennemy piece
            elif board_state[self.position[0], i].team!=self.team:
                moves = np.concatenate((moves, np.array([[self.position[0], i]])))
                break
            # If tile is occupied by allied piece
            else:
                # Stop the loop as rook cannot get on same piece as allied piece and cannot jump pieces
                break

        # Check moves from current position to left side of the board
        for i in range(self.position[1]+1, 8):
            # If tile is empty
            if board_state[self.position[0], i].name=="empty":
                # Add empty tile and continue loop
                moves = np.concatenate((moves, np.array([[self.position[0], i]])))
            # If tile is occupied by ennemy piece
            elif board_state[self.position[0], i].team!=self.team:
                moves = np.concatenate((moves, np.array([[self.position[0], i]])))
                break
            # If tile is occupied by allied piece
            else:
                # Stop the loop as rook cannot get on same piece as allied piece and cannot jump pieces
                break

        # Remove the dummy move that was added
        moves = np.delete(moves, 0, axis=0)
        return moves

"""
Knight Piece. Has those wierd moves
"""
class Knight(Pieces):
    def __init__(self, team, position, name="Knight") -> None:
        super().__init__(team, position, name)

    def is_tile_valid(self, coordinate_x, coordinate_y):
        """
        Returns true if tile delimited by coordinate_x and coordinate_y is on a classic chess board, false otherwise.
        A classic chess board had 8 tiles on the x and y coordinates.
        """
        if coordinate_x>=0 and coordinate_x<8 and coordinate_y>=0 and coordinate_y<8:
            return True
        else:
            return False

    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        # Initalize the moves which will be returned. Need to add a dummy move to be able to concatenate later
        moves = np.array([[-1, -1]], dtype=int)

        for i in [-2, 2]:
            for j in [-1, 1]:
                # If cell is valid and empty or valid and with a piece of ennemy team
                if self.is_tile_valid(self.position[0]+i, self.position[1]+j) and (board_state[self.position[0]+i, self.position[1]+j].name=="empty" or (board_state[self.position[0]+i, self.position[1]+j].name=="empty" and board_state[self.position[0]+i, self.position[1]+j].team!=self.team)):
                    moves = np.concatenate((moves, np.array([[self.position[0]+i, self.position[1]+j]])))
        
        for i in [-1, 1]:
            for j in [-2, 2]:
                # If cell is valid and empty or valid and with a piece of ennemy team
                if self.is_tile_valid(self.position[0]+i, self.position[1]+j) and (board_state[self.position[0]+i, self.position[1]+j].name=="empty" or (board_state[self.position[0]+i, self.position[1]+j].name=="empty" and board_state[self.position[0]+i, self.position[1]+j].team!=self.team)):
                    moves = np.concatenate((moves, np.array([[self.position[0]+i, self.position[1]+j]])))

        # Remove the dummy move that was added
        moves = np.delete(moves, 0, axis=0)
        return moves

"""
Bishop Bishop. Can move in diagonal
"""
class Bishop(Pieces):
    def __init__(self, team, position, name="Bishop") -> None:
        super().__init__(team, position, name)

    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        # Initalize the moves which will be returned. Need to add a dummy move to be able to concatenate later
        moves = np.array([[-1, -1]], dtype=int)

        # Check moves on the upper left side diagonaly
        for i in range(1, min(self.position[0]-1, self.position[1]-1)):
            # If tile is empty
            if board_state[self.position[0]-i, self.position[1]-i]:
                # Add empty tile and continue loop
                moves = np.concatenate((moves, np.array([[self.position[0]-i, self.position[1]-i]])))
            # If tile is occupied by ennemy piece
            elif board_state[self.position[0]-i, self.position[1]-i].teamn!=self.team:
                # Add ennemy occupied tile and stop loop as bishop cannot jump pieces
                moves = np.concatenate((moves, np.array([[self.position[0]-i, self.position[1]-i]])))
                break
            # If tile is occupied by allied piece
            else:
                # Stop loop as bishop cannot get on same piece as allied piece and cannot jump pieces
                break

        # Check moves on the upper left side diagonaly
        for i in range(1, min(self.position[0]-1, self.position[1]-1)):
            # If tile is empty
            if board_state[self.position[0]-i, self.position[1]-i]:
                # Add empty tile and continue loop
                moves = np.concatenate((moves, np.array([[self.position[0]-i, self.position[1]-i]])))
            # If tile is occupied by ennemy piece
            elif board_state[self.position[0]-i, self.position[1]-i].teamn!=self.team:
                # Add ennemy occupied tile and stop loop as bishop cannot jump pieces
                moves = np.concatenate((moves, np.array([[self.position[0]-i, self.position[1]-i]])))
                break
            # If tile is occupied by allied piece
            else:
                # Stop loop as bishop cannot get on same piece as allied piece and cannot jump pieces
                break        
        
        # Remove the dummy move that was added
        moves = np.delete(moves, 0, axis=0)
        return moves

"""
Queen Piece. Can move in any direction unlimited
"""
class Queen(Pieces):
    def __init__(self, team, position, name="Queen") -> None:
        super().__init__(team, position, name)

    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        # Initalize the moves which will be returned. Need to add a dummy move to be able to concatenate later
        moves = np.array([[-1, -1]], dtype=int)

        # Remove the dummy move that was added
        moves = np.delete(moves, 0, axis=0)
        return moves

"""
King Piece. Can move in any direction by 1
"""
class King(Pieces):
    def __init__(self, team, position, name="King") -> None:
        super().__init__(team, position, name)

    def move(self, board_state) -> np.array:
        """
        Returns all moves possible moves.
        board_state is an 8x8 np array with all the pieces present on the board.
        """
        # Initalize the moves which will be returned. Need to add a dummy move to be able to concatenate later
        moves = np.array([[-1, -1]], dtype=int)

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i!=0 and j!=0:
                    if board_state[self.position[0]+i, self.position[1]+j].name!="empty" and board_state[self.position[0]+i, self.position[1]+j].team!=self.team:
                        moves = np.concatenate((moves, np.array([[self.position[0]+i, self.position[1]+j]])))

        # Remove the dummy move that was added
        moves = np.delete(moves, 0, axis=0)
        return moves