from BuildGameFromFile import *
from PyGameInterface import *

if __name__ == "__main__":
    g = build_game_from_file("../GameFiles/SetPieces/Game1/game.rcgg")

    g.interface = PyGameInterface(g)

    g.start()
