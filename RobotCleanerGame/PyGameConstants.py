"""
    Constants & functionality for PyGame interface
"""
import Constants as Co
from Version import VERSION_STRING
import pygame

BUTTON_WIDTH = 128

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

DELAY_ONE_SEC = 1000
DELAY_REGULAR = 50

FILE_TILE = "TILE_64x64.png"

FILES_ROBOT = ["ROBOT_64x64L.png", "ROBOT_64x64R.png"]

FILES_BLUE_BIN = ["BLUE_BIN_64x64.png"]
FILES_GREEN_BIN = ["GREEN_BIN_64x64.png"]
FILES_RED_BIN = ["RED_BIN_64x64.png"]
FILES_UNIVERSAL_BIN = ["UNIVERSAL_BIN_64x64.png"]

FILES_BLUE_ITEM = ["BLUE_ITEM_64x64L.png", "BLUE_ITEM_64x64R.png"]
FILES_GREEN_ITEM = ["GREEN_ITEM_64x64L.png", "GREEN_ITEM_64x64R.png"]
FILES_RED_ITEM = ["RED_ITEM_64x64L.png", "RED_ITEM_64x64R.png"]

FILES_MESS = ["MESS_64x64L.png", "MESS_64x64R.png"]

FONT_COURIER_NEW = "couriernew"

PATH_TOKENS_BIG = "../GameFiles/Assets/Images/Tokens_Original/"
PATH_TOKENS_64 = "../GameFiles/Assets/Images/Tokens_Play/"

TILE_IMG = pygame.image.load(PATH_TOKENS_64 + FILE_TILE)
TILE_SIZE = 64

FEEDBACK_TEXT_BOX_HEIGHT = 20
WIN_WIDTH = TILE_SIZE * 12
WIN_HEIGHT = TILE_SIZE * 11 + FEEDBACK_TEXT_BOX_HEIGHT  # 20 extra pixels for feedback text

WIN_CAPTION = "RobotCleanerGame"

MENU_BUTTON_HELP = pygame.image.load(PATH_TOKENS_64 + "MENU_BUTTON_HELP.png")
MENU_BUTTON_LOAD = pygame.image.load(PATH_TOKENS_64 + "MENU_BUTTON_LOAD.png")
MENU_BUTTON_MENU = pygame.image.load(PATH_TOKENS_64 + "MENU_BUTTON_MENU.png")
MENU_BUTTON_PLAY = pygame.image.load(PATH_TOKENS_64 + "MENU_BUTTON_PLAY.png")
MENU_BUTTON_QUIT = pygame.image.load(PATH_TOKENS_64 + "MENU_BUTTON_QUIT.png")

MENU_RESPONSE_HELP = "help"
MENU_RESPONSE_LOAD = "load"
MENU_RESPONSE_PLAY = "play"
MENU_RESPONSE_QUIT = "quit"

BUT_DROP_PRESSED = pygame.image.load(PATH_TOKENS_64 + "B_DROP_PRESSED.png")
BUT_DROP_UNPRESS = pygame.image.load(PATH_TOKENS_64 + "B_DROP_UNPRESSED.png")
BUT_MOVE_PRESSED = pygame.image.load(PATH_TOKENS_64 + "B_MOVE_PRESSED.png")
BUT_MOVE_UNPRESS = pygame.image.load(PATH_TOKENS_64 + "B_MOVE_UNPRESSED.png")
BUT_PICK_PRESSED = pygame.image.load(PATH_TOKENS_64 + "B_PICKUP_PRESSED.png")
BUT_PICK_UNPRESS = pygame.image.load(PATH_TOKENS_64 + "B_PICKUP_UNPRESSED.png")
BUT_SWEEP_PRESSED = pygame.image.load(PATH_TOKENS_64 + "B_SWEEP_PRESSED.png")
BUT_SWEEP_UNPRESS = pygame.image.load(PATH_TOKENS_64 + "B_SWEEP_UNPRESSED.png")
BUT_UNAVAILABLE = pygame.image.load(PATH_TOKENS_64 + "BUTTON_UNAVAILABLE.png")

PRESSED_BUTTON = "pres_but"

CURRENT_SCREEN = "curr_scr"
PREVIOUS_SCREEN = "prev_scr"

MAIN_SCREEN = "main"
MENU_SCREEN = "menu"
LOAD_SCREEN = "load"
HELP_SCREEN = "help"

FEEDBACK_MSG_PRESS_BUTTON = "Press a button to choose an action to perform."
FEEDBACK_MSG_CLICK_GRID = "Now click the grid to choose a tile to perform the action upon."
FEEDBACK_MSG_PERFORMED_ACTION = "Performed action successfully."
FEEDBACK_MSG_WRONG_TILE_FOR_ACTION = "Action can't be done here."
FEEDBACK_MSG_GRID_CLEARED = "All cleared!"
FEEDBACK_MSG_PRESS_H_FOR_HELP = "Press H for Help."
FEEDBACK_MSG_PRESS_B_TO_GO_BACK = "Press B to go back."
FEEDBACK_MSG_SELECT_GAME_TO_LOAD = "Select a game to load."

SET_PIECES_PATH = "../GameFiles/SetPieces/"

TUTORIAL_PREFIX = "Tutorial_"
GAME_PREFIX = "Game_"

GAME_BUTTON_COMPLETE = pygame.image.load(PATH_TOKENS_64 + "GAME_BUTTON_COMPLETE.png")
GAME_BUTTON_INCOMPLETE = pygame.image.load(PATH_TOKENS_64 + "GAME_BUTTON_INCOMPLETE.png")

HELP_TOKEN_ADDITIONAL_TEXT: dict[str, str] = {
    Co.ROBOT_TOKEN: "The robot can carry up to three items of garbage and sweep messes.",
    "r": "Can be carried by the robot and put into the correct bin(s).",
    "g": "Can be carried by the robot and put into the correct bin(s).",
    "b": "Can be carried by the robot and put into the correct bin(s).",
    "R": f"Can accept Food garbage for {Co.SCORING["full"]} points.",
    "G": f"Can accept Plastic garbage for {Co.SCORING["full"]} points.",
    "B": f"Can accept Glass garbage for {Co.SCORING["full"]} points.",
    "*": f"Can accept all garbage for {Co.SCORING["half"]} points.",
    "m": f"Sweeping a mess gives {Co.SCORING["sweep"]} points.",
}

HELP_BOTTOM_TEXT = ["Your objective is to clear the board.",
                    "Every action including movement costs one point.",
                    "Try to score the maximum possible points!"]
