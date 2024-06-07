"""
    The Profile class stores variables associated to a particular player's play through.
"""

PROFILE_FOLDER_PATH = "../GameFiles/Profiles/"
PROFILE_FILE_SUFFIX = ".rcgp"
SEPARATOR = ","


class Profile:
    def __init__(self, name: str = "Player"):
        self.name = name
        self.completed: {str: int} = {}

    def add_completed(self, game_label: str, score: int):
        self.completed[game_label] = score

    def reset_completed(self):
        self.completed = {}

    def load(self):
        try:
            # Check that a profile file exists; if so, load it
            with open(PROFILE_FOLDER_PATH + self.name + PROFILE_FILE_SUFFIX, "r") as file:
                for line in file:
                    key, data = line.split(SEPARATOR)
                    self.completed[key] = int(data)

        except FileNotFoundError:
            pass

    def save(self):
        with open(PROFILE_FOLDER_PATH + self.name + PROFILE_FILE_SUFFIX, "w") as file:
            for k in self.completed:
                file.write(k + SEPARATOR + str(self.completed[k]) + "\n")


if __name__ == "__main__":
    p = Profile()
    #p.add_completed("test", 1)
    #p.add_completed("foo", 2)
    #p.save()
    p.load()
    print(p.completed)
