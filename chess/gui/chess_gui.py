from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import sys
sys.path.append("../chess_game")
sys.path.append("../utils")
import time
import argparse
from chess_timer import Timer
from chess_trace import Trace
from panel import Panel
from board_gui import BoardGUI
from chess_state import ChessState
from chess_rules import ChessRules
from chess_action import ChessAction
from chess_player import ChessPlayer
from copy import deepcopy

class ChessGUI(QMainWindow):
    depth_to_cover = 9
    automatic_save_game = False

    def __init__(self, app, board_type, players, allowed_time=120.0, sleep_time=.500, first_player="White", parent=None) -> None:
        super(ChessGUI, self).__init__(parent)
        self.app = app

        self.saved = True
        self.board_type = board_type
        self.players = players
        self.allowed_time = allowed_time
        self.sleep_time = sleep_time
        self.first_player = first_player

        self.setWindowTitle("PolyAI worhsop - chess game")
        self.statusBar()
        layout = QHBoxLayout()
        layout.addStretch()
        self.board_gui = BoardGUI(self.board_type)
        layout.addWidget(self.board_gui)
        layout.addSpacing(15)
        self.panel = Panel({"White":players["White"].name, "Black":players["Black"].name})
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
        next_player = self.players["White"]
        latest_player = self.players["Black"]
        self.state = ChessState(board=self.board.get_board(), next_player=next_player, latest_player = latest_player)
        self.trace = Trace(state=self.state, players={"White": self.players["White"].name,  "Black": self.players["Black"].name})
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
        self.current_player = self.players[self.first_player]
        self.panel.update_current_player(self.current_player.team)

        self.state = ChessState(
            board=self.board.get_board(), 
            next_player=self.players[self.first_player], 
            latest_player = self.players["White"] if "White"==self.first_player else self.players["Black"]
        )
        self.board.set_default_colors()

        for team in ["White", "Black"]:
            self.players[team].reset_player_informations()

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

    def play_game(self):
        print("Game to be played")


    def update_gui():
        pass

    def get_player_info(self, player):
        return self.state.get_player_info(player)

    def is_end_game(self):
        return self.done

    def results(self):
        if self.done():
            self.trace.done = self.done
            results = ChessRules.get_results(self.state)
            if not results["tie"]:
                end = QMessageBox.information(self, "End", f"{results['winner']} wins.")
            else:
                end = QMessageBox.information(self, "End", "No winners.")

    def load_battle(self, states, delay=0.5, done=True):
        self.board.set_default_colors()
        self.state = states[0]
        for state in states[1:]:
            action = state.get_latest_move()
            self.state = state
            self._update_gui()
            time.sleep(delay)
        self.done = done
        self._results()
        print("It's over.")

    def load_game_trigger(self):
        self.board.set_default_colors()
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Game', options=QFileDialog.DontUseNativeDialog)
        print(name[0])
        trace = self.trace.load(name[0])
        print(trace.players)
        self.reset_for_new_game()
        actions = trace.get_actions()
        delay, _ = QInputDialog.getDouble(self, 'Enter the delay', '')
        players_name = trace.players
        self.panel.update_players_name(players_name)
        self.load_battle(actions, delay, trace.done)

    def save_game_trigger(self):
        if self.done:
            if self.automatic_save_game:
                self.trace.write(self.players["White"].name + "-" + self.players["Black"].name)
            else:
                name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Game', options=QFileDialog.DontUseNativeDialog)
                if name[0] == "":
                    pass
                else:
                    self.trace.write(name[0])
        else:
            warning = QMessageBox.warning(self, "Warning", "No game ongoing")

    def exit_game_trigger(self):
        sys.exit(self.app.exec_())

    def game_rules_trigger(self):
        rules = "For the rules of chess, refer to https://www.chess.com/learn-how-to-play-chess"
        box = QMessageBox()
        box.about(self, "Rules", rules)

    def about_trigger(self):
        about = "Chess game implementation for PolyAI, for a workshop on zero-sum games where participants learn to code their own agents to play chess."
        box = QMessageBox()
        box.about(self, "About", about)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='total number of seconds credited to each player')
    parser.add_argument('-ai0', help='path to the ai that will play as player 0')
    parser.add_argument('-ai1', help='path to the ai that will play as player 1')
    parser.add_argument('-s', help='time to show the board')
    args = parser.parse_args()

    # set the time to play
    allowed_time = float(args.t) if args.t is not None else .1
    sleep_time = float(args.s) if args.s is not None else 0.

    player_type = [None, None]
    player_type[0] = args.ai0 if args.ai0 != None else 'human'
    player_type[1] = args.ai1 if args.ai1 != None else 'human'
    for i in range(2):
        if player_type[i].endswith('.py'):
            player_type[i] = player_type[i][:-3]
    agents = {}

    # load the agents
    k = "White"
    for i in range(2):
        if player_type[i] != 'human':
            j = player_type[i].rfind('/')
            # extract the dir from the agent
            dir = player_type[i][:j]
            # add the dir to the system path
            sys.path.append(dir)
            # extract the agent filename
            file = player_type[i][j + 1:]
            # create the agent instance
            agents[k] = ChessPlayer(team=k, name=file)
            k = "Black"
        else:
            agents[k] = ChessPlayer(team=k, name="human")
    if player_type[0]=="human" and player_type[1]=="human":
        raise Exception('Problems in  AI players instances. \n'
                        'Note that this implementation is not made for 2 humans. At least one of the players must be an AI agent.\n'
                        'Usage:\n'
                        '-t time credited \n'
                        '\t total number of seconds credited to each player \n'
                        '-ai0 ai0_file.py \n'
                        '\t path to the ai that will play as player 0 \n'
                        '-ai1 ai1_file.py\n'
                        '\t path to the ai that will play as player 1 \n'
                        '-s sleep time \n'
                        '\t time(in second) to show the board(or move)')

    # Set black at bottom of board only if a human plays black
    if player_type[1]=="human":
        board_type = 0
    else:
        board_type = 1
    game = ChessGUI(app=app, board_type=board_type, players=agents, sleep_time=sleep_time, allowed_time=allowed_time)
    game.show()
    sys.exit(app.exec_())