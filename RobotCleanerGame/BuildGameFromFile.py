"""

    A set of functions to build a game from a file

"""
import Game as Gm
import Interface as Int

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
    line1 = buffer[0].split(",")

    if len(line1) != 4:
        raise IOError("build_game_from_buffer: first line of file translate to four values.")

    g = Gm.Game(int(line1[0]), int(line1[1]), robot_start=(int(line1[2]), int(line1[3])))

    for line in buffer[1:]:
        coords = line[1:].replace("(", "").replace(")", "").split(",")

        g.add_grid_token((int(coords[0]), int(coords[1])), line[0])

    return g


def build_game_from_file(file_path: str) -> Gm.Game:
    """
    Combines functions to build a game from a file path reference.
    :param file_path: File path string
    :return: RobotCleanerGame.Game object
    """
    return build_game_from_buffer(read_file_to_buffer(file_path))


if __name__ == "__main__":
    g = build_game_from_file("../GameFiles/SetPieces/Game1/")
    g.interface = Int.Interface(g)

    g.interface.start()
