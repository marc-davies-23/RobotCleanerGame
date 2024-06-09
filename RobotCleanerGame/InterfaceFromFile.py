"""

    This Interface accepts a file instead of user input: for automation and test scripts

"""
from Actions import *
from BuildGameFromFile import SOLVE_FILE, build_game_from_file
from Constants import SET_PIECES_FOLDER
import Interface as In


class InterfaceFromFile(In.Interface):
    def __init__(self, game, folder_path) -> None:
        super().__init__(game)
        self.__actionList: [Action] = []
        solve_path = folder_path + "/" + SOLVE_FILE
        with open(solve_path, "r") as file:
            for line in file:
                line = line.replace("\r", "").replace("\n", "")  # Strip out line breaks
                split = line.split("(")

                # Try to read the second part of the split; if out of index range, then there are no coords
                try:
                    coords = self.get_coords_from_str(split[1])

                except IndexError:
                    coords = None

                # Dynamically create action object
                class_name = split[0]
                this_class = globals()[class_name]

                if coords is None:
                    instance = this_class(interface=self)
                else:
                    instance = this_class(interface=self, coords=coords)

                self.__actionList.append(instance)

    @staticmethod
    def get_coords_from_str(input_string) -> (int, int):
        cds = input_string.replace(")", "").split(",")
        return int(cds[0]), int(cds[1])

    def listen_for_action(self) -> Action:
        # Simply return the front item from the action list; if the list is empty, print warning and Quit
        try:
            return self.__actionList.pop(0)
        except IndexError:
            print("End of Action list from file.")
            return Quit(self)


if __name__ == "__main__":
    game_tag = "Tutorial_1"

    g = build_game_from_file(SET_PIECES_FOLDER + game_tag)
    g.interface = InterfaceFromFile(g, SET_PIECES_FOLDER + game_tag)

    g.interface.start()