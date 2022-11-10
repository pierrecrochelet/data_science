class ChessAction():

    def __init__(self, from_cell, to_cell) -> None:
        self.from_cell = from_cell
        self.to_cell = to_cell

    def __repr__(self):
        return str(self.get_action_as_dict())

    def get_action_as_dict(self):
        return {'from_cell': self.from_cell,
                'to_cell': self.to_cell}