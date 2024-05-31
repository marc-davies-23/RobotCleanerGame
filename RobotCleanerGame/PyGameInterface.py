"""
    Interface incorporating PyGame functionality
"""

from Interface import Interface
from PyGameConstFuncs import *


def map_pixel_to_tile_coord(pixel_coords: (int, int)) -> (int, int):
    return int(pixel_coords[0] / TILE_SIZE), int(pixel_coords[1] / TILE_SIZE)


class PyGameInterface(Interface):
    def __init__(self, game: Game, win_width: int = WIN_WIDTH, win_height: int = WIN_HEIGHT) -> None:
        super().__init__(game)
        self.state = {CURRENT_SCREEN: MAIN_SCREEN,
                      PRESSED_BUTTON: None}
        self.win_width = win_width
        self.win_height = win_height

        pygame.init()
        pygame.display.set_caption(WIN_CAPTION)

        self.window = pygame.display.set_mode((win_width, win_height))

        self.animation_beat = 0

        # Dictionary to store items on the screen that can be clicked
        self.screen_inventory = {}

        # Store feedback message
        self.feedback_msg = FEEDBACK_MSG_PRESS_H_FOR_HELP

    def give_user_feedback(self, feedback: str) -> None:
        self.feedback_msg = feedback

    def draw_background_tile(self, x: int, y: int) -> None:
        self.window.blit(TILE_IMG, (x, y))

    def beat(self) -> bool:
        # Are we on an animation beat?
        return self.animation_beat == 0

    def draw_help_screen(self):
        help_screen = help_screen_factory(self.window, FEEDBACK_MSG_PRESS_B_TO_GO_BACK)
        help_screen.draw()

    def draw_main_screen(self):
        # Default animation beats are hit once every ten loops
        self.animation_beat = (self.animation_beat + 1) % 10

        # Get possible actions
        actions = self.game.get_possible_actions()

        main = main_screen_factory(self, actions)

        main.draw()

    def event_start(self) -> None:
        title_screen = title_screen_factory(self.window, self.win_width)

        title_screen.draw()

    def event_begin_of_loop(self) -> None:
        # Refresh the screen inventory
        self.screen_inventory = {}

    def event_grid_cleared(self) -> None:
        self.give_user_feedback(FEEDBACK_MSG_GRID_CLEARED)

    def event_quit(self) -> None:
        pygame.quit()

    def display_state(self) -> None:
        screen = self.state[CURRENT_SCREEN]

        getattr(self, "draw_" + screen + "_screen")()

    def listen_for_action(self) -> (Action | None):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return Quit()
                case pygame.MOUSEBUTTONUP:
                    return self.process_mouse_click()
                case _:
                    pass

        # Check for key press
        key = pygame.key.get_pressed()
        if key[pygame.K_h]:
            if self.state[CURRENT_SCREEN] != HELP_SCREEN:  # Prevents double-firing
                self.state[PREVIOUS_SCREEN] = self.state[CURRENT_SCREEN]
                self.state[CURRENT_SCREEN] = HELP_SCREEN
        if key[pygame.K_b]:
            current = self.state[CURRENT_SCREEN]
            previous = self.state[PREVIOUS_SCREEN]
            if current == HELP_SCREEN and previous != HELP_SCREEN:  # Can only go back from Help Screen
                self.state[PREVIOUS_SCREEN] = current
                self.state[CURRENT_SCREEN] = previous
                self.feedback_msg = FEEDBACK_MSG_PRESS_H_FOR_HELP

        return None

    def process_mouse_click(self) -> (Action | None):
        x, y = map_pixel_to_tile_coord(pygame.mouse.get_pos())

        try:
            screen_item = self.screen_inventory[(x, y)]

        except KeyError:
            # Nothing in inventory, reset
            self.state[PRESSED_BUTTON] = None
            self.feedback_msg = FEEDBACK_MSG_PRESS_BUTTON
            return None

        try:
            # Try to set a pressed button state
            if screen_item.__name__ in {STATE_FLAG_MOVE_PRESSED, STATE_FLAG_DROP_PRESSED,
                                        STATE_FLAG_PICK_PRESSED, STATE_FLAG_SWEP_PRESSED}:
                self.state[PRESSED_BUTTON] = screen_item.__name__
                self.feedback_msg = FEEDBACK_MSG_CLICK_GRID

        except AttributeError:
            # If not applicable, continue
            pass

        # Catch no button pressed and stop here
        if self.state[PRESSED_BUTTON] is None:
            self.feedback_msg = FEEDBACK_MSG_PRESS_BUTTON
            return None

        try:
            for a in screen_item:
                if a.__class__.__name__ == self.state[PRESSED_BUTTON]:
                    # Can reset the Pressed Button state
                    self.state[PRESSED_BUTTON] = None
                    self.feedback_msg = FEEDBACK_MSG_PERFORMED_ACTION
                    return a

                # If we found nothing...
                self.feedback_msg = FEEDBACK_MSG_WRONG_TILE_FOR_ACTION

        except TypeError:
            # Continue
            pass

        # Last catch all
        return None


"""
    Here are screens for the PyGame interface as well as screen factories.
"""


class PyGameScreenElement:
    def __init__(self, window, x: int, y: int):
        self.window = window
        self.x = x
        self.y = y

    def draw(self):
        # self.window.blit(foo, (self.x, self.y))
        pass


class PyGameTextScreenElement(PyGameScreenElement):
    def __init__(self, window, x: int, y: int, font, size, text: str,
                 color=COLOR_WHITE, bold: bool = False, antialias: bool = True):
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


class PyGameImageScreenElement(PyGameScreenElement):
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


class PyGameTokenScreenElement(PyGameScreenElement):
    def __init__(self, window, x: int, y: int, token, incr=True, static=False):
        super().__init__(window, x, y)
        self.token: PyGameToken = token
        self.increment = incr
        self.static = static

    def draw(self):
        self.token.draw(self.window, self.x, self.y, self.increment, self.static)


class PyGameScreen:
    def __init__(self, window, bg_color=COLOR_BLACK, delay=DELAY_REGULAR):
        self.window = window
        self.bg_color = bg_color
        self.delay = delay
        self.elements: [PyGameScreenElement] = []

    def add_element(self, element: PyGameScreenElement):
        self.elements.append(element)

    def draw(self):
        self.window.fill(self.bg_color)

        for el in self.elements:
            el.draw()

        pygame.display.update()
        pygame.time.delay(self.delay)


def title_screen_factory(window, win_width) -> PyGameScreen:
    x = 200
    y = 100

    title_screen = PyGameScreen(window, delay=(2 * DELAY_ONE_SEC))

    title_screen.add_element(PyGameTextScreenElement(window, x, y, FONT_COURIER_NEW, 32,
                                                     TITLE_STRING, bold=True, antialias=True))
    title_screen.add_element(PyGameImageScreenElement(window, int((win_width / 2) - 128), y + 20,
                                                      img_path=PATH_TOKENS_BIG + "ROBOT_256x256.png"))

    return title_screen


def main_screen_factory(interface, actions) -> PyGameScreen:
    main = PyGameScreen(interface.window)

    # Draw button menu at bottom of screen
    x = 0
    y = interface.win_height - TILE_SIZE - FEEDBACK_TEXT_BOX_HEIGHT

    avail = Game.is_action_type_in_actions(Move.__name__, actions)
    main.add_element(button_menu_factory(interface, Move, avail, STATE_FLAG_MOVE_PRESSED,
                                         BUT_MOVE_PRESSED, BUT_MOVE_UNPRESS, x, y))
    x += BUTTON_WIDTH

    avail = Game.is_action_type_in_actions(PickUp.__name__, actions)
    main.add_element(button_menu_factory(interface, PickUp, avail, STATE_FLAG_PICK_PRESSED,
                                         BUT_PICK_PRESSED, BUT_PICK_UNPRESS, x, y))
    x += BUTTON_WIDTH

    avail = Game.is_action_type_in_actions(Drop.__name__, actions)
    main.add_element(button_menu_factory(interface, Drop, avail, STATE_FLAG_DROP_PRESSED,
                                         BUT_DROP_PRESSED, BUT_DROP_UNPRESS, x, y))
    x += BUTTON_WIDTH

    avail = Game.is_action_type_in_actions(Sweep.__name__, actions)
    main.add_element(button_menu_factory(interface, Sweep, avail, STATE_FLAG_SWEP_PRESSED,
                                         BUT_SWEEP_PRESSED, BUT_SWEEP_UNPRESS, x, y))

    # Now draw the robot's stack
    # Draw it one tile to the right of the game grid
    x = interface.game.grid.size_x * TILE_SIZE

    # Draw it from the bottom, but leave space for a stack as well as icon underneath
    y = max(interface.game.grid.size_y, MAX_CARRY) * TILE_SIZE

    # Add marker base
    main.add_element(PyGameImageScreenElement(interface.window, x, y,
                                              img_path=PATH_TOKENS_64 + "CARRIED_ITEMS_MARKER_64x64.png"))

    # Add stack properly
    for item in interface.game.robot.stack:
        y -= TILE_SIZE
        main.add_element(PyGameTokenScreenElement(interface.window, x, y, TOKEN_MAP[item],
                                                  incr=False, static=True))

    ordered_actions = Game.order_actions_by_coords(actions)

    # Add game tiles + tokens
    for y in range(0, interface.game.grid.size_y):
        for x in range(0, interface.game.grid.size_x):

            tile = interface.game.grid.get_tile((x, y))

            # Add the base background tile
            main.add_element(PyGameImageScreenElement(interface.window, x * TILE_SIZE, y * TILE_SIZE, image=TILE_IMG))

            # If this tile can be clicked for an action, add them to the screen inventory
            if (x, y) in ordered_actions:
                interface.screen_inventory[(x, y)] = ordered_actions[(x, y)]

            if tile.is_empty():
                # Go to next
                continue

            main.add_element(PyGameTokenScreenElement(interface.window, x * TILE_SIZE, y * TILE_SIZE,
                                                      token=TOKEN_MAP[tile.get_content()], incr=interface.beat()))

    if len(interface.feedback_msg) > 0:
        main.add_element(feedback_box_factory(interface.window, interface.feedback_msg))

    return main


def button_menu_factory(interface, action, available, state_flag,
                        image_pressed, image_unpressed, x, y) -> PyGameImageScreenElement:
    if not available:
        image = BUT_UNAVAILABLE
    elif interface.state[PRESSED_BUTTON] == state_flag:
        image = image_pressed
    else:
        image = image_unpressed

    # Add the button to the screen inventory with Tile coords; other it is inactive
    tile_x, tile_y = map_pixel_to_tile_coord((x, y))

    # The buttons are two tiles wide, so add two indices
    interface.screen_inventory[(tile_x, tile_y)] = action
    interface.screen_inventory[(tile_x + 1, tile_y)] = action

    return PyGameImageScreenElement(interface.window, x, y, image=image)


def help_screen_factory(window, message) -> PyGameScreen:
    x = 0
    y = 0
    help_screen = PyGameScreen(window)

    for key, txt in TOKEN_DESCRIPTIONS.items():
        help_screen.add_element(PyGameTokenScreenElement(window, x, y, TOKEN_MAP[key], False, True))
        help_screen.add_element(PyGameTextScreenElement(window, x + TILE_SIZE, y + 8, FONT_COURIER_NEW, 24,
                                                        txt + ": ", bold=True, antialias=True))
        help_screen.add_element(PyGameTextScreenElement(window, x + TILE_SIZE, y + 40, FONT_COURIER_NEW, 16,
                                                        HELP_TOKEN_ADDITIONAL_TEXT[key], bold=False, antialias=True))

        y += TILE_SIZE

    help_screen.add_element(feedback_box_factory(window, message))

    return help_screen


def feedback_box_factory(window, message) -> PyGameTextScreenElement:
    x = 16
    y = WIN_HEIGHT - FEEDBACK_TEXT_BOX_HEIGHT + 2

    return PyGameTextScreenElement(window, x, y, FONT_COURIER_NEW, 16,
                                   message, bold=False, antialias=True)


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


TOKEN_MAP: dict[str, PyGameToken] = {
    ROBOT_TOKEN: PyGameToken(PATH_TOKENS_64, FILES_ROBOT),
    "r": PyGameToken(PATH_TOKENS_64, FILES_RED_ITEM),
    "g": PyGameToken(PATH_TOKENS_64, FILES_GREEN_ITEM),
    "b": PyGameToken(PATH_TOKENS_64, FILES_BLUE_ITEM),
    "R": PyGameToken(PATH_TOKENS_64, FILES_RED_BIN),
    "G": PyGameToken(PATH_TOKENS_64, FILES_GREEN_BIN),
    "B": PyGameToken(PATH_TOKENS_64, FILES_BLUE_BIN),
    "*": PyGameToken(PATH_TOKENS_64, FILES_UNIVERSAL_BIN),
    "m": PyGameToken(PATH_TOKENS_64, FILES_MESS),
}

if __name__ == "__main__":
    pass
