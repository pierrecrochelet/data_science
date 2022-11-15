class ChessPlayer(object):

    def __init__(self, team, score=0, name="human") -> None:
        self.team = team
        self.score = score
        self.name = name

    def reset_player_informations(self):
        self.score = 0