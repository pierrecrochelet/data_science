from PyQt5 import QtGui
import sys
sys.path.append("../assets")


class Piece:
    def __init__(self, team, type):
        self.moveNumber = 0
        self.team = team
        self.type = type

        if team=="White" and type=="pawn":
            self.image_url = "../assets/Chess_white_pawn.svg"
        elif team=="White" and type=="knight":
            self.image_url = "../assets/Chess_white_knight.svg"
        elif team=="White" and type=="bishop":
            self.image_url = "../assets/Chess_white_bishop.svg"
        elif team=="White" and type=="rook":
            self.image_url = "../assets/Chess_white_rook.svg"
        elif team=="White" and type=="queen":
            self.image_url = "../assets/Chess_white_queen.svg"
        elif team=="White" and type=="king":
            self.image_url = "../assets/Chess_white_king.svg"
        elif team=="Black" and type=="pawn":
            self.image_url = "../assets/Chess_black_pawn.svg"
        elif team=="Black" and type=="knight":
            self.image_url = "../assets/Chess_black_knight.svg"
        elif team=="Black" and type=="bishop":
            self.image_url = "../assets/Chess_black_bishop.svg"
        elif team=="Black" and type=="rook":
            self.image_url = "../assets/Chess_black_rook.svg"
        elif team=="Black" and type=="queen":
            self.image_url = "../assets/Chess_black_queen.svg"
        elif team=="Black" and type=="king":
            self.image_url = "../assets/Chess_black_king.svg"

    def getImage(self):
        pixmap = QtGui.QPixmap()
        pixmap.load(self.image_url)
        pixmap = pixmap.scaledToHeight(80)
        return pixmap

    def getTeam(self):
        return self.team

    def getType(self):
        return self.type

    def getMoveNumber(self):
        return self.moveNumber

    def nextMove(self):
        self.moveNumber += 1