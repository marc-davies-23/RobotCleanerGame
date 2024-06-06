"""
    Interface incorporating PyGame functionality
"""
import Actions as Ac
import Game as Gm
import Interface as In
import pygame
import PyGameConstFuncs as PCo
import PyGameScreens as PSc


def map_pixel_to_tile_coord(pixel_coords: (int, int)) -> (int, int):
    return int(pixel_coords[0] / PCo.TILE_SIZE), int(pixel_coords[1] / PCo.TILE_SIZE)


class PyGameInterface(In.Interface):

    def __init__(self, game: (Gm.Game | None) = None, width: int = PCo.WIN_WIDTH, height: int = PCo.WIN_HEIGHT) -> None:
        super().__init__(game)
        self.state = {PCo.CURRENT_SCREEN: PCo.MENU_SCREEN,
                      PCo.PRESSED_BUTTON: None}

        # Initial holder
        self.screen = None

        self.win_width = width
        self.win_height = height

        pygame.init()
        pygame.display.set_caption(PCo.WIN_CAPTION)

        self.window = pygame.display.set_mode((width, height))

        # Store animation beat at interface level
        self.animation_beat = 0

        # Store feedback message
        self.feedback_msg = PCo.FEEDBACK_MSG_PRESS_H_FOR_HELP

    def give_user_feedback(self, feedback: str) -> None:
        self.feedback_msg = feedback

    def beat(self) -> bool:
        # Are we on an animation beat?
        return self.animation_beat == 0

    def event_start(self) -> None:
        # One-off screen for Title
        PSc.TitleScreen.factory(self).draw()

    def event_begin_of_loop(self) -> None:
        pass

    def event_grid_cleared(self) -> None:
        self.give_user_feedback(PCo.FEEDBACK_MSG_GRID_CLEARED)

    def event_quit(self) -> None:
        pygame.quit()

    def display_state(self) -> None:
        current = self.state[PCo.CURRENT_SCREEN]

        self.screen = PSc.SCREEN_CLASS[current].factory(self)

        self.screen.draw()

    def listen_for_action(self) -> (Ac.Action | None):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return Ac.Quit(self)
                case pygame.MOUSEBUTTONUP:
                    if self.screen:
                        coords = map_pixel_to_tile_coord(pygame.mouse.get_pos())
                        return self.screen.on_mouse_click(coords)
                    else:
                        return None
                case _:
                    pass

        # Check for key press
        key = pygame.key.get_pressed()
        if key[pygame.K_h] and self.state[PCo.CURRENT_SCREEN] != PCo.HELP_SCREEN:  # Prevents double-firing
            self.state[PCo.PREVIOUS_SCREEN] = self.state[PCo.CURRENT_SCREEN]
            self.state[PCo.CURRENT_SCREEN] = PCo.HELP_SCREEN
        if key[pygame.K_b] and self.state[PCo.CURRENT_SCREEN] == PCo.HELP_SCREEN:
            try:
                previous = self.state[PCo.PREVIOUS_SCREEN]
            except KeyError:
                previous = PCo.MENU_SCREEN  # If there's no previous screen, go back to menu

            if previous == PCo.HELP_SCREEN:  # Can't go back to Help Screen
                previous = PCo.MENU_SCREEN

            self.state[PCo.CURRENT_SCREEN] = previous
            self.give_user_feedback(PCo.FEEDBACK_MSG_PRESS_H_FOR_HELP)

        return None


if __name__ == "__main__":
    pass
