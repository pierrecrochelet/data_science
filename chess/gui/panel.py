from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *


class Panel(QWidget):

    def __init__(self, players_name, parent=None):
        super(Panel, self).__init__(parent)
        self.players_name = players_name
        layout = QVBoxLayout()
        layout.addStretch()

        # Arrow 1
        horizontal1 = QHBoxLayout()
        horizontal1.addStretch()
        self.arrowBlack = QLabel(self)
        self.arrowBlack.setFixedSize(20, 20)
        self.arrowBlack.setScaledContents(True)
        horizontal1.addWidget(self.arrowBlack)
        horizontal1.addStretch()
        layout.addLayout(horizontal1)

        # Image 1
        horizontal2 = QHBoxLayout()
        horizontal2.addStretch()
        image1 = QLabel(self)
        image1.setAlignment(QtCore.Qt.AlignCenter)
        image1.setFixedSize(100, 100)
        image1.setScaledContents(True)
        image1.setPixmap(QtGui.QPixmap("../assets/robot_black.jpg"))
        horizontal2.addWidget(image1)
        horizontal2.addStretch()
        layout.addLayout(horizontal2)

        # Player 1 Name

        self.name1 = QLabel(self.players_name["Black"], self)
        self.name1.setAlignment(QtCore.Qt.AlignCenter)
        self.name1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.name1)

        # Score Player 1
        self.score1 = QLabel("0", self)
        self.score1.setAlignment(QtCore.Qt.AlignCenter)
        self.score1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.score1)

        # Lost By Player 1
        lost_white_layout = QGridLayout()
        layout.addLayout(lost_white_layout)

        # Arrow 2
        horizontal3 = QHBoxLayout()
        horizontal3.addStretch()
        self.arrowWhite = QLabel(self)
        self.arrowWhite.setFixedSize(20, 20)
        self.arrowWhite.setScaledContents(True)
        horizontal3.addWidget(self.arrowWhite)
        horizontal3.addStretch()
        layout.addLayout(horizontal3)

        # Image 2
        horizontal4 = QHBoxLayout()
        horizontal4.addStretch()
        image2 = QLabel(self)
        image2.setAlignment(QtCore.Qt.AlignCenter)
        image2.setFixedSize(100, 100)
        image2.setScaledContents(True)
        image2.setPixmap(QtGui.QPixmap("../assets/robot_white.jpg"))
        horizontal4.addWidget(image2)
        horizontal4.addStretch()
        layout.addLayout(horizontal4)

        # Player 2 Name
        self.name2 = QLabel(self.players_name["White"], self)
        self.name2.setAlignment(QtCore.Qt.AlignCenter)
        self.name2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.name2)

        # Score Player 2
        self.score2 = QLabel("0", self)
        self.score2.setAlignment(QtCore.Qt.AlignCenter)
        self.score2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.score2)

        # Lost By Player 2
        lostBlackLayout = QGridLayout()
        layout.addLayout(lostBlackLayout)

        layout.addStretch()
        self.setLayout(layout)
        self.update_current_player("White")

    def update_players_name(self, players_name):
        self.name1.setText(players_name["White"])
        self.name2.setText(players_name["Black"])

    def update_current_player(self, player_team):
        empty = QtGui.QPixmap(0, 0)
        arrow = QtGui.QPixmap('../assets/arrow.png')

        if player_team == "White":
            self.arrowWhite.setPixmap(arrow)
            self.arrowBlack.setPixmap(empty)
        else:
            self.arrowBlack.setPixmap(arrow)
            self.arrowWhite.setPixmap(empty)

    def reset_panel_player(self):
        empty = QtGui.QPixmap(0, 0)
        arrow = QtGui.QPixmap('../assets/arrow.png')
        self.arrowWhite.setPixmap(arrow)
        self.arrowBlack.setPixmap(empty)

    def update_score(self, score):
        self.score1.setText(str(score["Black"]))
        self.score2.setText(str(score["White"]))