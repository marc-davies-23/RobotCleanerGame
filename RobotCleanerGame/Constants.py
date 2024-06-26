"""

    Store constants here

"""

QUIT_MESSAGE = "Quitting..."
REFRESH_MESSAGE = "Refreshing"

# Default x/y dimensions
DEFAULT_SIZE_X = 3
DEFAULT_SIZE_Y = 3

# Empty_tile
EMPTY_TILE = "."

# Blocked Tile
BLOCKED_TILE = " "

# Robot max actions
MAX_CARRY = 3
MAX_SWEEP = 1

# Moves along the x/y axes
MOVE_LIST = [(1, 0), (-1, 0), (0, 1), (0, -1)]

"""

    Here we define tokens & token types:

    r, g, b: items that need to be tidied away
    R, G, B, *: bin receptacle for items of appropriate type; * accepts all
    m : mess to be swept up

    A token can only contain one of these.

    Properties of tokens:
     - if an item, can be picked up or dropped
     - if a receptacle, can accept an item of appropriate type
     - if a mess, can be swept

"""

ROBOT_TOKEN = "¥"

UNIVERSAL_BIN = "*"

SCORING = {
    "full": 10,
    "half": 5,
    "sweep": 3,
}

# Tokens short reference & description
TOKEN_DESCRIPTIONS: dict[str, str] = {
    ROBOT_TOKEN: "Robot",
    "r": "Food Garbage",
    "g": "Plastic Garbage",
    "b": "Glass Garbage",
    "R": "Food Bin",
    "G": "Plastic Bin",
    "B": "Glass Bin",
    UNIVERSAL_BIN: "Universal Bin",
    "m": "Mess",
}

SET_OF_BINS = {"R", "G", "B", "*"}

SET_OF_ITEMS = {"r", "g", "b"}

SET_OF_MESS = {"m"}

ITEMS_TO_BIN_MAP = {
    # Item : Bins which accept that item
    "r": {"*", "R"},
    "g": {"*", "G"},
    "b": {"*", "B"},
}

SET_PIECES_FOLDER = "../GameFiles/SetPieces/"
