import sys
sys.path.append("../core")
from PyQt5.QtWidgets import *
from piece import Piece
from square import Square
from board import Board

class BoardGUI(QWidget):
    def __init__(self, type, current_player="White", parent=None):
        super(BoardGUI, self).__init__(parent)
        self.current_player = current_player
        self.color = ["Black", "White"]
        self.score = {"white": 0, "Black": 0}
        self.board_type = type
        self.setFixedSize(100 * 8, 100 * 8)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        self.squares = list()
        self.board = None
        for i in range(8):
            temp = list()
            for j in range(8):
                square = Square(i, j)
                grid_layout.addWidget(square, 8 - i, j)
                temp.append(square)
            self.squares.append(temp)
        self.reset_board()
        self.set_default_colors()
        self.setLayout(grid_layout)

    def get_board(self):
        return self.board

    def add_piece(self, cell, piece_type, team):
        x, y = cell[0], cell[1]
        self.squares[x][y].set_piece(Piece(team, piece_type))

    def move_piece(self, at, to, team, piece_type):
        x, y = to[0], to[1]
        self.squares[x][y].set_piece(Piece(team, piece_type))
        x, y = at[0], at[1]
        self.squares[x][y].remove_piece()

    def remove_piece(self, cell):
        x, y = cell[0], cell[1]
        self.squares[x][y].remove_piece()

    def set_default_colors(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    self.squares[i][j].setStyleSheet("border: 1px solid black; background-color : #e1cebc")
                else:
                    self.squares[i][j].setStyleSheet("border: 1px solid black; background-color : #964f0b")

    def set_current_player(self, player):
        self.current_player = player

    def reset_board(self):
        self.board = Board(self.board_type)
        for i in range(0, 8):
            for j in range(0, 8):
                self.squares[i][j].remove_piece()
                if self.board.get_board_state()[i,j].name!="empty":
                    self.squares[i][j].set_piece(Piece(self.board.get_board_state()[i,j].team, self.board.get_board_state()[i,j].name))

    def enable_all_squares(self):
        for i in range(8):
            for j in range(8):
                self.squares[i][j].set_active(True)

    def disable_all_squares(self):
        for i in range(8):
            for j in range(8):
                self.squares[i][j].set_active(False)

    def putListBoard(self, listBoard):  
        for i in range(len(self.self.squares)):
            for j in range(len(self.self.squares[0])):
                if listBoard[i][j] == None:
                    self.squares[i][j].removePiece()
                elif listBoard[i][j][0] == "Black":
                    self.squares[i][j].setPiece(Piece("Black", listBoard[i][j][1]))
                elif listBoard[i][j] == "White":
                    self.squares[i][j].setPiece(Piece("White", listBoard[i][j][1]))

    def get_board_array(self): 
        list_board = []
        for i in range(len(self.squares)):
            temp = []
            for j in range(len(self.squares[0])):
                if not self.squares[i][j].isPiece():
                    temp.append(None)
                else:
                    temp.append((self.squares[i][j].piece.getTeam(), self.squares[i][j].piece.getType()))
            list_board.append(temp)
        return list_board