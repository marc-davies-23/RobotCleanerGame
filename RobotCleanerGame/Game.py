"""

    Class for the main game functions, loop & processing actions.

    Game.grid: object of the Grid class
    Game.robot: object of the Robot class

"""

import Actions as Ac
import Constants as Co
import Grid as Gr
import Robot as Rb


class Game:
    """
        The game has a grid, which holds most of the current game state; the robot is the player's agent.

        The Interface class defines display & control input; the base Interface class is a console mode.

        History will be useful for retracing games; a necessity for advanced functions, e.g. ML
    """

    def __init__(self, tag: (str | None) = None, size_x: int = Co.DEFAULT_SIZE_X, size_y: int = Co.DEFAULT_SIZE_Y,
                 robot_start: (int, int | None) = None, interface=None, history=None) -> None:
        """
        :param tag: Tag to identify game
        :param size_x: Horizontal size of Grid
        :param size_y: Vertical size of Grid
        :param robot_start: Robot's starting coordinates
        :param interface: Interface controls
        :param history: History list
        """
        self.tag = tag
        self.grid = None
        self.robot = None
        self.initialise_grid(size_x, size_y, robot_start)

        self.interface = interface

        self.score = 0
        self.game_ended = False

        if history is None:
            self.history = []
        else:
            self.history = history

    def initialise_grid(self, size_x: int, size_y: int, robot_start: (int, int | None) = None) -> None:
        """
        Creates a RobotCleanerGame.Grid object.

        Separate method so that games may be re-initialised.

        :param size_x: Horizontal size of Grid
        :param size_y: Vertical size of Grid
        :param robot_start: Robot's starting coordinates
        """
        self.grid = Gr.Grid(size_x, size_y)
        self.robot = Rb.Robot(start=robot_start)

        self.grid.set_tile(self.robot.coords, Co.ROBOT_TOKEN)

    def add_grid_token(self, coords: (int, int), token_symbol: str) -> None:
        """
        Method to add a token to the Game grid

        :param coords: Coordinates of the Grid where a token should be placed.
        :param token_symbol: Token character symbol; see Constants.py
        """
        if not (token_symbol in Co.SET_OF_ITEMS | Co.SET_OF_BINS | Co.SET_OF_MESS):
            # Only Items, Bins, and Messes can be placed for now
            raise ValueError(f"Game.add_grid_token: token_symbol not valid")

        if not self.grid.get_tile(coords).is_empty():
            # This method should not over-write existing tokens
            raise ValueError(f"Game.add_grid_token: tile at co-ordinates {coords} is not empty")

        self.grid.set_tile(coords, token_symbol)

    def get_possible_actions(self) -> [Ac.Action]:
        """
        This method determines what possible Actions the Robot may take given the current state of the Grid

        :return: List of Actions; see Actions.py
        """
        actions = []

        for coord in self.grid.get_adjacent_coordinates(self.robot.coords):

            tile = self.grid.get_tile(coord)

            if tile.is_empty():
                # Can move or drop into an empty co-ord
                actions.append(Ac.Move(self.interface, coord))
                if not self.robot.is_stack_empty():
                    actions.append(Ac.Drop(self.interface, coord))
            elif tile.is_bin():
                # Can -- potentially -- drop an item into a bin
                if not self.robot.is_stack_empty():
                    actions.append(Ac.Drop(self.interface, coord))
                else:
                    # Do nothing: logically necessary
                    pass
            elif tile.is_item():
                # Can pick up an item
                actions.append(Ac.PickUp(self.interface, coord))
            elif tile.is_mess():
                # Can sweep a mess
                actions.append(Ac.Sweep(self.interface, coord))
            else:
                # We should never get here
                raise NotImplementedError("Game.get_possible_actions: impossible state")

        return actions

    @staticmethod
    def is_action_type_in_actions(action_name: str, actions: [Ac.Action]) -> bool:
        # Not the most efficient of algorithms but there shouldn't be too many actions
        for a in actions:
            if a.__class__.__name__ == action_name:
                return True

        return False

    @staticmethod
    def order_actions_by_coords(actions: [Ac.Action]) -> dict[(int, int): set[Ac.Action]]:
        ordered_actions = {}
        for a in actions:
            if a.coords in ordered_actions:
                # Add to set
                ordered_actions[a.coords].add(a)
            else:
                # Create set
                ordered_actions[a.coords] = {a}

        return ordered_actions

    def is_grid_cleared(self) -> bool:
        """
        Is the whole Grid cleared, including items the Robot is carrying?

        :return: True/False that Grid is cleared
        """
        # Check the robot's not carrying anything first, this is fast to check; if he is, the grid isn't cleared
        if not self.robot.is_stack_empty():
            return False

        # Now check the grid; this is slower
        for j in self.grid.grid:
            for i in j:
                if not (i.get_content() in {Co.EMPTY_TILE, Co.ROBOT_TOKEN} | Co.SET_OF_BINS):
                    return False

        # If we get here then the grid is cleared
        self.game_ended = True

        # Update profile high score
        if self.interface.profile:
            try:
                old_score = self.interface.profile.completed[self.tag]
            except KeyError:
                old_score = None

            if old_score is None or old_score < self.score:
                self.interface.profile.add_completed(self.tag, self.score)
                self.interface.profile.save()

        return True

    def change_score(self, change=-1):
        # Default call deducts a point as this is the most common call
        if not self.game_ended:
            self.score += change


if __name__ == "__main__":
    g = Game()
    print(g.grid)
