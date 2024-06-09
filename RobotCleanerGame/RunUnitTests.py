from BuildGameFromFile import build_game_from_file
from BuildLogFilesForUnitTests import TESTCASE_LOG_FOLDER, LOG_FILE_SUFFIX, TESTCASES
from Constants import SET_PIECES_FOLDER
from InterfaceFromFile import InterfaceFromFile

import datetime
from io import StringIO
import os
import sys

CONFLICTS_FOLDER = "../UnitTesting/Conflicts/"


def get_unit_testcase(game_tag):
    buffer = []
    stdout_origin = sys.stdout

    sys.stdout = buffer = StringIO()

    g = build_game_from_file(SET_PIECES_FOLDER + game_tag)
    g.interface = InterfaceFromFile(g, SET_PIECES_FOLDER + game_tag)

    g.interface.start()

    sys.stdout = stdout_origin

    return buffer.getvalue()


def strip_date(s):
    for c in [" ", ":", "."]:
        s = s.replace(c, "-")
    return s


if __name__ == "__main__":
    if not os.path.exists(CONFLICTS_FOLDER):
        os.makedirs(CONFLICTS_FOLDER)

    now = strip_date(datetime.datetime.now().__str__())

    conflicts = CONFLICTS_FOLDER + now + "/"

    print(f"Conflicts folder (if any found): {conflicts}")

    for case in TESTCASES:

        ok = True

        test_case = get_unit_testcase(case)
        print(case + ": ", end="")

        with open(TESTCASE_LOG_FOLDER + case + LOG_FILE_SUFFIX, "r") as file:
            if file.read() == test_case:
                print("OK")
            else:
                print("Not OK; see Conflicts folder")
                ok = False

        # Skip rest of pass if OK
        if ok:
            continue

        if not os.path.exists(conflicts):
            os.makedirs(conflicts)

        with open(conflicts + case + ".txt", "w") as file:
            file.write(test_case)


