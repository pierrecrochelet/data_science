import numpy as np
from board_generator import BoardStateGenerator
import pieces

class Board:

    def __init__(self, board_type) -> None:

        self.board_state = BoardStateGenerator.generate_empty_board(board_type)

    def get_board_state(self):
        return self.board_state
    
    def is_cell_on_board(self, x_coordinate, y_coordinate):
        """
        Verify if cell exists on board

        Args:
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell

        Returns:
            bool: True if the cell is on the board. False if not.
        """

        if 0<=x_coordinate<8 and 0<=y_coordinate<8:
            return True
        return False

    def empty_cell(self, x_coordinate, y_coordinate):
        """
        Empty a cell on the board

        Args:
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell
        """

        if self.is_cell_on_board(x_coordinate, y_coordinate):
            self.board_state[x_coordinate, y_coordinate] = pieces.noPiece(np.array([x_coordinate, y_coordinate]))

    def get_cell_team(self, x_coordinate, y_coordinate):
        """
        Get the team of a cell on the board

        Args:
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell

        Returns:
            str: A string representing the team of the piece on the specified cell, i.e. one of ['White', 'Black', 'None']
        """
        
        if self.is_cell_on_board(x_coordinate, y_coordinate):
            return self.board_state[x_coordinate, y_coordinate].team

    def is_empty_cell(self, x_coordinate, y_coordinate):
        """
        Verify if cell is empty, i.e. NoPiece is on it

        Args:
            x_coordinate: int, the coordinate along the x axis of the cell
            y_coordinate: int, the coordinate along the y axis of the cell

        Returns:
            bool: True if the cell is empty. False if not.
        """

        if self.is_cell_on_board(x_coordinate, y_coordinate):
            return self.board_state[x_coordinate, y_coordinate].team=="None"

    def get_all_empty_cells(self):
        """
        Finds all the empty cells on the board

        Returns:
             np.array: containing the coordinates of all the empty cells
        """
        # Initalize the array which will be returned. Need to add a dummy cell to be able to concatenate later
        empty_cells = np.array([[-1, -1]], dtype=int)
        for i in range(0, self.board_state.shape[0]):
            for j in range(0, self.board_state.shape[1]):
                if self.board_state[i,j].team=="None":
                    empty_cells = np.concatenate((empty_cells, np.array([[i,j]])))

        # Remove the dummy cell that was added
        empty_cells = np.delete(empty_cells, 0, axis=0)
