"""

    A set of functions to build a game from a file

"""
import Game as Gm
import Interface as In

FILE_NAME = "game.rcgg"


def read_file_to_buffer(folder_path: str) -> [str]:
    """
    Function to read the input file and turn it into a buffer, stripping carriage returns and line breaks.

    :param folder_path: File path in string format
    :return: Buffer as list of strings
    """
    buffer = []
    with open(folder_path + FILE_NAME, "r") as file:
        for line in file:
            line = line.replace("\r", "")
            buffer.append(line.replace("\n", ""))  # Strip out line breaks

    return buffer


def build_game_from_buffer(buffer: [str]) -> Gm.Game:
    """
    Breaks up the buffer into actionable parts.

    The first line of the buffer should consist of four numbers: sizeX (of grid), sizeY (of grid),
    X coords (of robot), Y coords (of robot)

    Each line onwards consists of a format like so:
    T(x,y)

    where T is a token type, and x, y are its coords.

    :param buffer: Input buffer (list of strings)
    :return: RobotCleanerGame.Game object
    """
    line = buffer[0].split(",")

    x = int(line[0])
    y = int(line[1])
    rb_start = (int(line[2]), int(line[3]))

    if len(line) != 4:
        raise IOError("build_game_from_buffer: first line of file translate to four values.")

    game = Gm.Game(size_x=x, size_y=y, robot_start=rb_start)

    for line in buffer[1:]:
        coords = line[1:].replace("(", "").replace(")", "").split(",")

        game.add_grid_token((int(coords[0]), int(coords[1])), line[0])

    return game


def build_game_from_file(folder: str, tag: (str | None) = None, interface: (In.Interface | None) = None) -> Gm.Game:
    """
    Combine functionality to build a game from static file as of folder path

    :param tag: Game tag to identify tag
    :param folder: Folder path
    :param interface:  Provided interface, if any
    :return: Game object
    """

    game = build_game_from_buffer(read_file_to_buffer(folder))

    game.tag = tag
    game.interface = interface

    return game


if __name__ == "__main__":
    g = build_game_from_file("../GameFiles/SetPieces/Tutorial_1/")
    g.interface = In.Interface(g)

    g.interface.start()
