from BuildGameFromFile import build_game_from_file
from Constants import SET_PIECES_FOLDER
from InterfaceFromFile import InterfaceFromFile
import sys

TESTCASE_LOG_FOLDER = "../UnitTesting/BaseLogs/"
LOG_FILE_SUFFIX = ".log"

TESTCASES = ["Tutorial_1", "Tutorial_2", "Tutorial_3", "Tutorial_4", "Tutorial_5"]


def export_logs():
    stdout_origin = sys.stdout

    for game_tag in TESTCASES:
        log_file = TESTCASE_LOG_FOLDER + game_tag + LOG_FILE_SUFFIX

        sys.stdout = open(log_file, "w")

        g = build_game_from_file(SET_PIECES_FOLDER + game_tag)
        g.interface = InterfaceFromFile(g, SET_PIECES_FOLDER + game_tag)

        g.interface.start()

        sys.stdout.close()

    sys.stdout = stdout_origin


if __name__ == "__main__":

    this_input = input('Warning! This will overwrite existing unit case logs. Type "OK" in upper case to proceed.\n')

    if this_input == "OK":
        print("Creating logs.")
        export_logs()
    else:
        print("Wrong input, aborting.")
