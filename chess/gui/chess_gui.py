from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import sys
import time
import argparse
import sys
sys.path.append("../chess_game")
sys.path.append("../utils")
from timer import Timer
from trace import Trace
from panel import Panel
from board import BoardGUI
from chess_state import ChessState
from chess_rules import ChessRules
from chess_action import ChessAction
from copy import deepcopy

class ChessGUI(QMainWindow):
    depth_to_cover = 9
    automatic_save_game = False

    def __init__(self, app, board_type, players, allowed_time=120.0, sleep_time=.500, first_player="White", parent=None) -> None:
        super(ChessGUI, self).__init__(parent)
        self.app = app

        self.saved = True
        self.board_type = 1
        self.players = players
        for i in range(2):
            if self.players[i].team=="Black" and self.players[i].name=="human":
                self.board_type = 0
        self.allowed_time = allowed_time
        self.sleep_time = sleep_time
        self.first_player = first_player

        self.setWindowTitle("PolyAI worhsop - chess game")
        self.statusBar()
        #self.setWindowIcon(QtGui.QIcon("assets/icon.png"))
        layout = QHBoxLayout()
        layout.addStretch()
        self.board_gui = BoardGUI(self.board_type)
        layout.addWidget(self.board_gui)
        layout.addSpacing(15)
        self.panel = Panel([players[0].name, players[1].name])
        layout.addWidget(self.panel)
        layout.addStretch()
        content = QWidget()
        content.setLayout(layout)
        self.setCentralWidget(content)
        self.create_menu()
        self.reset()


    def reset(self) -> None:
        self.done = False
        self.rewarding_move = False
        self.board = BoardGUI(self.board_type)
        for i in range(2):
            if self.players[i].team==self.first_player:
                next_player = self.players[i]
            else:
                latest_player = self.players[i]
        self.state = ChessState(board=self.board.get_board_state(), next_player=next_player, latest_player = latest_player)
        self.trace = Trace(
            self.state, 
            players={
                "White": self.players[0].name if self.players[0].team=="White" else self.players[1].name, 
                "Black": self.players[0].name if self.players[0].team=="Black" else self.players[1].name
                }
            )
        self.current_player = next_player

    def create_menu(self) -> None:
        menu = self.menuBar()

        # Game Menu
        game_menu = menu.addMenu("Game")

        # New Game Submenu
        new_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("../assets/New file.png")), 'New Game', self)
        new_game_action.setShortcut(QtGui.QKeySequence.New)
        new_game_action.setStatusTip("New game Luncher")

        new_game_action.triggered.connect(self.new_game_trigger)

        game_menu.addAction(new_game_action)

        game_menu.addSeparator()

        # Load Game Submenu
        load_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("../assets/Open file.png")), 'Load Game', self)
        load_game_action.setShortcut(QtGui.QKeySequence.Open)
        load_game_action.setStatusTip("Load a previous game")
        load_game_action.triggered.connect(self.load_game_trigger)
        game_menu.addAction(load_game_action)

        # Save Game
        save_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Save.png")), 'Save Game', self)
        save_game_action.setShortcut(QtGui.QKeySequence.Save)
        save_game_action.setStatusTip("Save current game")
        save_game_action.triggered.connect(self.save_game_trigger)
        game_menu.addAction(save_game_action)

        game_menu.addSeparator()

        # Exit and close game
        exit_game_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Close.png")), 'Exit Game', self)
        exit_game_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_game_action.setMenuRole(QAction.QuitRole)
        exit_game_action.setStatusTip("Exit and close window")
        exit_game_action.triggered.connect(self.exit_game_trigger)
        game_menu.addAction(exit_game_action)

        menu.addSeparator()

        # Help Menu
        help_menu = menu.addMenu("Help")

        # Rules
        game_rules_action = QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon("pieces/Help.png")), 'Rules', self)
        game_rules_action.setMenuRole(QAction.AboutRole)
        game_rules_action.triggered.connect(self.game_rules_trigger)
        help_menu.addAction(game_rules_action)

        help_menu.addSeparator()

        # About
        about_action = QAction('About', self)
        about_action.setMenuRole(QAction.AboutRole)
        about_action.triggered.connect(self.about_trigger)
        help_menu.addAction(about_action)

    def new_game_trigger(self):
        new_game = QMessageBox.question(self, 'New Game', "You're about to start a new Game.", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if new_game == QMessageBox.Yes:
            self.reset_for_new_game()
            self.app.processEvents()
            self.play_game()
        else:
            pass

    def reset_for_new_game(self) -> None:
        self.board.reset_board()
        self.board.score = {"White": 0, "Black": 0}
        self.done = False

        self.board.enable_all_squares()
        self.panel.reset_panel_player()
        self.board.current_player = self.first_player
        self.current_player = self.players[0] if self.players[0].team==self.first_player else self.players[1]
        self.panel.update_current_player(self.current_player)

        self.state = ChessState(
            board=self.board.get_board_state(), 
            next_player=self.players[0] if self.players[0].team==self.first_player else self.players[1], 
            latest_player = self.players[1] if self.players[0].team==self.first_player else self.players[0]
        )
        self.board.set_default_colors()

        for i in range(2):
            self.players[i].reset_player_informations()

    def step(self, action) -> None:
        """
        Plays one step of the game. Takes an action and perform in the environment.

        Args:
            action : object of class ChessAction, An action containing the move from a player.

        Returns:
            bool: Dependent on the validity of the action will return True if the was was performed False if not.
        """
        assert isinstance(action, ChessAction), "action has to be an Action class object"
        result = ChessRules.act(self.state, action, self.current_player)
        if isinstance(result, bool):
            return False
        else:
            self.state, self.done = result
            self.current_player = self.state.get_next_player()
            return True

    