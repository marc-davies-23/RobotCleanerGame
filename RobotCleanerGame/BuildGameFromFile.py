"""

    A set of functions to build a game from a file

"""
from Constants import SET_PIECES_FOLDER
import Game as Gm
import Interface as In

# Set this value to false; toggle it with toggle_allow_solve() below
allow_export_solve = False

FILE_NAME = "game.rcgg"
SOLVE_FILE = "solve.rcgs"


def read_file_to_buffer(folder_path: str) -> [str]:
    """
    Function to read the input file and turn it into a buffer, stripping carriage returns and line breaks.

    :param folder_path: File path in string format
    :return: Buffer as list of strings
    """
    buffer = []
    if folder_path[len(folder_path) - 1] == "/":
        file_path = folder_path + FILE_NAME
    else:
        file_path = folder_path + "/" + FILE_NAME
    with open(file_path, "r") as file:
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
        if "#" in line:
            line, _ = line.split("#", 1)  # strip out comments
        coords = line[1:].replace("(", "").replace(")", "").split(",")

        game.add_grid_token((int(coords[0]), int(coords[1])), line[0])

    return game


def build_game_from_file(folder: str, game_tag: (str | None) = None, interface=None) -> Gm.Game:
    """
    Combine functionality to build a game from static file as of folder path

    :param game_tag: Game tag to identify tag
    :param folder: Folder path
    :param interface:  Provided interface, if any
    :return: Game object
    """

    game = build_game_from_buffer(read_file_to_buffer(folder))

    game.tag = game_tag
    game.interface = interface

    return game


def toggle_allow_solve():
    # Force the calling of this method
    global allow_export_solve
    allow_export_solve = not allow_export_solve


def export_solve(game_tag, history):
    # Double check we're allowed to export as this may override an existing solve file
    assert allow_export_solve

    solve_file_path = SET_PIECES_FOLDER + game_tag + "/" + SOLVE_FILE

    print(f"Exporting solve to: {solve_file_path}")

    data = ""

    for a in history:
        try:
            data = (data + a.__class__.__name__ + str(a.coords) + "\n").replace(" ", "")
        except AttributeError:
            pass

        with open(solve_file_path, "w") as file:
            file.write(data)


if __name__ == "__main__":
    tag = "Game_2"

    toggle_allow_solve()
    g = build_game_from_file(SET_PIECES_FOLDER + tag + "/")
    g.interface = In.Interface(g)
    g.tag = tag

    g.interface.start()
