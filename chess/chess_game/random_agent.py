from chess_rules import ChessRules
from chess_player import ChessPlayer

class AI(ChessPlayer):
    
    def __init__(self, team) -> None:
        super.__init__(team)

    def play(self, state, remain_time):
        print(f"Player {self.team} is playing.")
        print("time remain is ", remain_time, " seconds")
        return ChessRules.random_play(state, self)
    
    def set_score(self, new_score):
        self.score = new_score

    def reset_player_informations(self):
        self.score = 0
