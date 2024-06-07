"""
    Here are screens for the PyGame interface as well as screen factories.
"""
import Actions as Ac
import BuildGameFromFile as Bd
import Constants as Co
import PyGameConstants as PCo
import Game as Gm
import os
import pygame
import PyGameInterface as PIn

STATE_FLAG_MOVE_PRESSED = Ac.Move.__name__
STATE_FLAG_DROP_PRESSED = Ac.Drop.__name__
STATE_FLAG_PICK_PRESSED = Ac.PickUp.__name__
STATE_FLAG_SWEEP_PRESSED = Ac.Sweep.__name__


class PyGameScreenElement:
    def __init__(self, window, x: int, y: int):
        self.window = window
        self.x = x
        self.y = y

    def draw(self):
        # self.window.blit(foo, (self.x, self.y))
        pass


class PyGameTextElement(PyGameScreenElement):
    def __init__(self, window, x: int, y: int, text: str, size, font=PCo.FONT_COURIER_NEW,
                 color=PCo.COLOR_WHITE, bold: bool = False, antialias: bool = True):
        super().__init__(window, x, y)
        self.font = font
        self.size = size
        self.color = color
        self.bold: bool = bold
        self.text: str = text
        self.antialias: bool = antialias

    def draw(self):
        font = pygame.font.SysFont(self.font, self.size, self.bold)
        text = font.render(text=self.text, antialias=self.antialias, color=self.color)
        self.window.blit(text, (self.x, self.y))


class PyGameImageElement(PyGameScreenElement):
    def __init__(self, window, x: int, y: int, img_path: str = None, image: pygame.image = None):
        if img_path is None and image is None:
            raise AttributeError("img_path and image cannot both be None")
        super().__init__(window, x, y)
        if image is None:
            self.image = pygame.image.load(img_path)
        else:
            self.image = image

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))


class PyGameTokenElement(PyGameScreenElement):
    def __init__(self, window, x: int, y: int, token, incr=True, static=False):
        super().__init__(window, x, y)
        self.token: PyGameToken = token
        self.increment = incr
        self.static = static

    def draw(self):
        self.token.draw(self.window, self.x, self.y, self.increment, self.static)


class PyGameScreen:
    @staticmethod
    def factory(interface):
        """
        Should return an instance of itself
        """
        return PyGameScreen(interface)

    def __init__(self, interface, bg_color=PCo.COLOR_BLACK, delay=PCo.DELAY_REGULAR):
        self.interface = interface
        self.window = interface.window
        self.bg_color = bg_color
        self.delay = delay
        self.elements: [PyGameScreenElement] = []
        self.inventory = {}  # Store screen events

    def add_element(self, element: PyGameScreenElement):
        self.elements.append(element)

    def draw(self):
        self.window.fill(self.bg_color)

        for el in self.elements:
            el.draw()

        pygame.display.update()
        pygame.time.delay(self.delay)

    def on_mouse_click(self, coords) -> (Ac.Action | None):
        try:
            screen_item = self.inventory[coords]
        except KeyError:
            return

        return screen_item


class HelpScreen(PyGameScreen):
    @staticmethod
    def factory(interface) -> PyGameScreen:
        x = 0
        y = 0

        window = interface.window
        message = PCo.FEEDBACK_MSG_PRESS_B_TO_GO_BACK

        hlp_scn = HelpScreen(interface)

        for key, txt in Co.TOKEN_DESCRIPTIONS.items():
            hlp_scn.add_element(PyGameTokenElement(window, x, y, TOKEN_MAP[key], False, True))
            hlp_scn.add_element(PyGameTextElement(window, x + PCo.TILE_SIZE, y + 8, txt + ": ", 24,
                                                  bold=True, antialias=True))
            hlp_scn.add_element(PyGameTextElement(window, x + PCo.TILE_SIZE, y + 40,
                                                  PCo.HELP_TOKEN_ADDITIONAL_TEXT[key],
                                                  16, bold=False, antialias=True))

            y += PCo.TILE_SIZE

        y += 20

        for txt in PCo.HELP_BOTTOM_TEXT:
            hlp_scn.add_element(PyGameTextElement(window, x + 16, y + 8, txt, 16,
                                                  bold=False, antialias=True))
            y += 20

        x = 5 * PCo.BUTTON_WIDTH
        y = interface.win_height - PCo.TILE_SIZE - PCo.FEEDBACK_TEXT_BOX_HEIGHT

        hlp_scn.add_element(menu_button_factory(interface, hlp_scn, x, y))

        hlp_scn.add_element(feedback_box_factory(window, message))

        return hlp_scn


class LoadScreen(PyGameScreen):
    @staticmethod
    def factory(interface) -> PyGameScreen:
        x_limit = 5
        win = interface.window  # Shorten calls
        message = PCo.FEEDBACK_MSG_SELECT_GAME_TO_LOAD

        x = 0              # Declare here for scope
        y = -1 * PCo.TILE_SIZE  # Start negative for the loop

        load_scn = LoadScreen(interface)

        for game_type in [PCo.TUTORIAL_PREFIX, PCo.GAME_PREFIX]:
            i = 0

            x = PCo.TILE_SIZE  # Start with padding
            y += 2 * PCo.TILE_SIZE

            # Build Tutorials
            while True:
                i += 1

                current_game = game_type + str(i)

                folder_path = PCo.SET_PIECES_PATH + current_game + "/"

                if not os.path.exists(folder_path):
                    break

                if interface.profile and current_game in interface.profile.completed:
                    image = PCo.GAME_BUTTON_COMPLETE
                    color = PCo.COLOR_WHITE
                else:
                    image = PCo.GAME_BUTTON_INCOMPLETE
                    color = PCo.COLOR_BLACK

                text = game_type[0] + str(i)
                padding = 16 - 8 * (len(text) - 2)
                load_scn.add_element(PyGameImageElement(win, x, y, image=image))
                load_scn.add_element(PyGameTextElement(win, x+padding, y+16, text=text, color=color,
                                                       size=30, bold=True, antialias=True))

                tile_x, tile_y = PIn.map_pixel_to_tile_coord((x, y))
                load_scn.inventory[(tile_x, tile_y)] = current_game

                if i % x_limit == 0:
                    x = PCo.TILE_SIZE
                    y += 2 * PCo.TILE_SIZE
                else:
                    x += 2 * PCo.TILE_SIZE

        # Bottom of the screen
        x = 5 * PCo.BUTTON_WIDTH
        y = interface.win_height - PCo.TILE_SIZE - PCo.FEEDBACK_TEXT_BOX_HEIGHT

        load_scn.add_element(menu_button_factory(interface, load_scn, x, y))

        load_scn.add_element(feedback_box_factory(interface.window, message))

        return load_scn

    def on_mouse_click(self, coords) -> (Ac.Action | None):
        try:
            screen_item = self.inventory[coords]
        except KeyError:
            return

        # If we get a string here, try to load that game
        if isinstance(screen_item, str):
            self.interface.game = Bd.build_game_from_file("../GameFiles/SetPieces/" + screen_item + "/",
                                                          tag=screen_item, interface=self.interface)
            self.interface.state[PCo.CURRENT_SCREEN] = PCo.MAIN_SCREEN
            self.interface.give_user_feedback("Loading " + screen_item.replace("_", " "))
            return
        else:
            # Presume it's an object to be executed and return it
            return screen_item


class MainScreen(PyGameScreen):
    @staticmethod
    def factory(interface) -> PyGameScreen:
        # Default animation beats are hit once every ten loops
        interface.animation_beat = (interface.animation_beat + 1) % 10

        main = MainScreen(interface)

        window = interface.window

        # Get possible actions
        actions = interface.game.get_possible_actions()

        # Draw button menu at bottom of screen
        x = 0
        y = interface.win_height - PCo.TILE_SIZE - PCo.FEEDBACK_TEXT_BOX_HEIGHT

        avail = Gm.Game.is_action_type_in_actions(Ac.Move.__name__, actions)
        main.add_element(main_button_factory(interface, main, Ac.Move, avail, STATE_FLAG_MOVE_PRESSED,
                                             PCo.BUT_MOVE_PRESSED, PCo.BUT_MOVE_UNPRESS, x, y))
        x += PCo.BUTTON_WIDTH

        avail = Gm.Game.is_action_type_in_actions(Ac.PickUp.__name__, actions)
        main.add_element(main_button_factory(interface, main, Ac.PickUp, avail, STATE_FLAG_PICK_PRESSED,
                                             PCo.BUT_PICK_PRESSED, PCo.BUT_PICK_UNPRESS, x, y))
        x += PCo.BUTTON_WIDTH

        avail = Gm.Game.is_action_type_in_actions(Ac.Drop.__name__, actions)
        main.add_element(main_button_factory(interface, main, Ac.Drop, avail, STATE_FLAG_DROP_PRESSED,
                                             PCo.BUT_DROP_PRESSED, PCo.BUT_DROP_UNPRESS, x, y))
        x += PCo.BUTTON_WIDTH

        avail = Gm.Game.is_action_type_in_actions(Ac.Sweep.__name__, actions)
        main.add_element(main_button_factory(interface, main, Ac.Sweep, avail, STATE_FLAG_SWEEP_PRESSED,
                                             PCo.BUT_SWEEP_PRESSED, PCo.BUT_SWEEP_UNPRESS, x, y))

        # Score
        x += PCo.BUTTON_WIDTH
        score = str(interface.game.score)
        main.add_element(PyGameTextElement(window, x + 24, y + 8, "Score:", 24, bold=True, antialias=True))
        main.add_element(PyGameTextElement(window, x + 60, y + 40, score, 24, bold=False, antialias=True))

        # Menu button
        x += PCo.BUTTON_WIDTH
        main.add_element(menu_button_factory(interface, main, x, y))

        # Now draw the robot's stack
        # Draw it one tile to the right of the game grid
        x = interface.game.grid.size_x * PCo.TILE_SIZE

        # Draw it from the bottom, but leave space for a stack as well as icon underneath
        y = max(interface.game.grid.size_y, Co.MAX_CARRY) * PCo.TILE_SIZE

        # Add marker base
        main.add_element(PyGameImageElement(interface.window, x, y,
                                            img_path=PCo.PATH_TOKENS_64 + "CARRIED_ITEMS_MARKER_64x64.png"))

        # Add stack properly
        for item in interface.game.robot.stack:
            y -= PCo.TILE_SIZE
            main.add_element(PyGameTokenElement(interface.window, x, y, TOKEN_MAP[item],
                                                incr=False, static=True))

        ordered_actions = Gm.Game.order_actions_by_coords(actions)

        # Add game tiles + tokens
        for y in range(0, interface.game.grid.size_y):
            for x in range(0, interface.game.grid.size_x):

                tile = interface.game.grid.get_tile((x, y))

                # Add the base background tile
                main.add_element(
                    PyGameImageElement(interface.window, x * PCo.TILE_SIZE, y * PCo.TILE_SIZE, image=PCo.TILE_IMG))

                # If this tile can be clicked for an action, add them to the screen inventory
                if (x, y) in ordered_actions:
                    main.inventory[(x, y)] = ordered_actions[(x, y)]

                if tile.is_empty():
                    # Go to next
                    continue

                main.add_element(PyGameTokenElement(interface.window, x * PCo.TILE_SIZE, y * PCo.TILE_SIZE,
                                                    token=TOKEN_MAP[tile.get_content()], incr=interface.beat()))

        if len(interface.feedback_msg) > 0:
            main.add_element(feedback_box_factory(interface.window, interface.feedback_msg))

        return main

    def on_mouse_click(self, coords) -> (Ac.Action | None):
        try:
            screen_item = self.inventory[coords]

        except KeyError:
            # Nothing in inventory, reset
            self.interface.state[PCo.PRESSED_BUTTON] = None
            self.interface.give_user_feedback(PCo.FEEDBACK_MSG_PRESS_BUTTON)
            return

        # Catch GoTo here for now...
        if screen_item.__class__.__name__ == Ac.GoToMenu.__name__:
            return screen_item

        try:
            # Try to set a pressed button state
            if screen_item.__name__ in {STATE_FLAG_MOVE_PRESSED, STATE_FLAG_DROP_PRESSED,
                                        STATE_FLAG_PICK_PRESSED, STATE_FLAG_SWEEP_PRESSED}:
                self.interface.state[PCo.PRESSED_BUTTON] = screen_item.__name__
                self.interface.give_user_feedback(PCo.FEEDBACK_MSG_CLICK_GRID)

        except AttributeError:
            # If not applicable, continue
            pass

            # Catch no button pressed and stop here
        if self.interface.state[PCo.PRESSED_BUTTON] is None:
            self.interface.give_user_feedback(PCo.FEEDBACK_MSG_PRESS_BUTTON)
            return

        try:
            for a in screen_item:
                if a.__class__.__name__ == self.interface.state[PCo.PRESSED_BUTTON]:
                    # Can reset the Pressed Button state
                    self.interface.state[PCo.PRESSED_BUTTON] = None
                    self.interface.give_user_feedback(PCo.FEEDBACK_MSG_PERFORMED_ACTION)
                    return a

                # If we found nothing...
                self.interface.give_user_feedback(PCo.FEEDBACK_MSG_WRONG_TILE_FOR_ACTION)

        except TypeError:
            # Continue
            pass


class MenuScreen(PyGameScreen):
    @staticmethod
    def factory(interface) -> PyGameScreen:
        response_list = [PCo.MENU_RESPONSE_PLAY, PCo.MENU_RESPONSE_HELP, PCo.MENU_RESPONSE_LOAD, PCo.MENU_RESPONSE_QUIT]
        image_list = [PCo.MENU_BUTTON_PLAY, PCo.MENU_BUTTON_HELP, PCo.MENU_BUTTON_LOAD, PCo.MENU_BUTTON_QUIT]

        # Alignment has to fit within tiles
        x = (int(interface.win_width / (2 * PCo.TILE_SIZE)) - 1) * PCo.TILE_SIZE
        y = (int(interface.win_height / (2 * PCo.TILE_SIZE)) - (len(image_list) - 1)) * PCo.TILE_SIZE

        menu_screen = MenuScreen(interface)

        for res, image in zip(response_list, image_list):
            menu_screen.add_element(PyGameImageElement(interface.window, x, y, image=image))

            # Add the button to the screen inventory with Tile coords; other it is inactive
            tile_x, tile_y = PIn.map_pixel_to_tile_coord((x, y))

            # The buttons are two tiles wide, so add two indices
            menu_screen.inventory[(tile_x, tile_y)] = res
            menu_screen.inventory[(tile_x + 1, tile_y)] = res

            y += PCo.TILE_SIZE

        return menu_screen

    def on_mouse_click(self, coords) -> (Ac.Action | None):
        try:
            response = self.inventory[coords]

        except KeyError:
            return None

        match response:
            case PCo.MENU_RESPONSE_HELP:
                self.interface.state[PCo.CURRENT_SCREEN] = PCo.HELP_SCREEN
            case PCo.MENU_RESPONSE_PLAY:
                if self.interface.game:
                    # Change current screen to main
                    self.interface.state[PCo.CURRENT_SCREEN] = PCo.MAIN_SCREEN
                else:
                    # Make them pick which game to play
                    self.interface.state[PCo.CURRENT_SCREEN] = PCo.LOAD_SCREEN
            case PCo.MENU_RESPONSE_LOAD:
                self.interface.state[PCo.CURRENT_SCREEN] = PCo.LOAD_SCREEN
            case PCo.MENU_RESPONSE_QUIT:
                return Ac.Quit(self)
            case _:
                pass

        return None


class TitleScreen(PyGameScreen):
    @staticmethod
    def factory(interface) -> PyGameScreen:
        x = 200
        y = 100

        window = interface.window
        width = interface.win_width

        title_screen = TitleScreen(interface, delay=(2 * PCo.DELAY_ONE_SEC))

        title_screen.add_element(PyGameTextElement(window, x, y, PCo.VERSION_STRING, 32,
                                                   bold=True, antialias=True))
        title_screen.add_element(PyGameImageElement(window, int((width / 2) - 128), y + 20,
                                                    img_path=PCo.PATH_TOKENS_BIG + "ROBOT_256x256.png"))

        return title_screen


"""
    Other assistant factory methods here
"""


def menu_button_factory(interface, screen, x, y):
    tile_x, tile_y = PIn.map_pixel_to_tile_coord((x, y))
    screen.inventory[tile_x, tile_y] = Ac.GoToMenu(interface)
    screen.inventory[tile_x + 1, tile_y] = Ac.GoToMenu(interface)
    return PyGameImageElement(interface.window, x, y, image=PCo.MENU_BUTTON_MENU)


def main_button_factory(interface, screen, action, available, state_flag,
                        image_pressed, image_unpressed, x, y) -> PyGameImageElement:
    if not available:
        image = PCo.BUT_UNAVAILABLE
    elif interface.state[PCo.PRESSED_BUTTON] == state_flag:
        image = image_pressed
    else:
        image = image_unpressed

    # Add the button to the screen inventory with Tile coords; other it is inactive
    tile_x, tile_y = PIn.map_pixel_to_tile_coord((x, y))

    # The buttons are two tiles wide, so add two indices
    screen.inventory[(tile_x, tile_y)] = action
    screen.inventory[(tile_x + 1, tile_y)] = action

    return PyGameImageElement(interface.window, x, y, image=image)


def feedback_box_factory(window, message) -> PyGameTextElement:
    x = 16
    y = PCo.WIN_HEIGHT - PCo.FEEDBACK_TEXT_BOX_HEIGHT + 2

    return PyGameTextElement(window, x, y, message, 16, bold=False, antialias=True)


"""
    PyGameTokens
"""


class PyGameToken:
    def __init__(self, folder: str, files: [str]) -> None:
        self.anim_idx = 0
        self.anim_max = len(files) - 1

        if self.anim_max < 0:
            raise FileNotFoundError("PyGameToken.__init__: empty files list")

        self.images = []

        for file in files:
            self.images.append(pygame.image.load(folder + file))

    def get_image(self, static_img: bool = False) -> pygame.Surface:
        if static_img:
            return self.images[0]
        else:
            return self.images[self.anim_idx]

    def increment_idx(self) -> None:
        if self.anim_max == 0:
            # If max is zero, there's only one image; don't bother incrementing index
            return

        if self.anim_idx == self.anim_max:
            # Start again
            self.anim_idx = 0
        else:
            self.anim_idx += 1

    def draw(self, window, x: int, y: int, increment: bool = True, static_img: bool = False) -> None:
        window.blit(self.get_image(static_img), (x, y))
        if increment and not static_img:
            self.increment_idx()


SCREEN_CLASS = {
    PCo.MAIN_SCREEN: MainScreen,
    PCo.MENU_SCREEN: MenuScreen,
    PCo.LOAD_SCREEN: LoadScreen,
    PCo.HELP_SCREEN: HelpScreen,
}

TOKEN_MAP: dict[str, PyGameToken] = {
    Co.ROBOT_TOKEN: PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_ROBOT),
    "r": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_RED_ITEM),
    "g": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_GREEN_ITEM),
    "b": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_BLUE_ITEM),
    "R": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_RED_BIN),
    "G": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_GREEN_BIN),
    "B": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_BLUE_BIN),
    "*": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_UNIVERSAL_BIN),
    "m": PyGameToken(PCo.PATH_TOKENS_64, PCo.FILES_MESS),
}

if __name__ == "__main__":
    pass
