"""

    This Interface accepts a file instead of user input: for automation and test scripts

"""
import Actions as Act
from BuildGameFromFile import *
import Interface as Int


class InterfaceFromFile(Int.Interface):
    def __init__(self, game, file_path) -> None:
        super().__init__(game)
        self.__actionList: [Act.Action] = []
        with open(file_path, "r") as file:
            for line in file:
                line = line.replace("\r", "").replace("\n", "")  # Strip out line breaks
                split = line.split("(")

                # Try to read the second part of the split; if out of index range, then there are no coords
                try:
                    coords = self.get_coords_from_str(split[1])

                except IndexError:
                    coords = None

                # Dynamically create action object
                if coords is None:
                    self.__actionList.append(type(split[0], (object,), {})())
                else:
                    self.__actionList.append(type(split[0], (object,), {"coords": coords})())

    @staticmethod
    def get_coords_from_str(input_string) -> (int, int):
        cds = input_string.replace(")", "").split(",")
        return int(cds[0]), int(cds[1])

    def listen_for_action(self) -> Act.Action:
        # Simply return the front item from the action list; if the list is empty, print warning and Quit
        try:
            return self.__actionList.pop(0)
        except IndexError:
            print("Warning: end of Action list from file; Quitting")
            return Act.Quit(self)


if __name__ == "__main__":
    g = build_game_from_file("../GameFiles/SetPieces/Game1/game.rcgg")
    g.interface = InterfaceFromFile(g, "../GameFiles/SetPieces/Game1/solve.rcgs")

    g.interface.start()
