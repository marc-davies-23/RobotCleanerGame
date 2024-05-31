"""

    Class for the main game functions, loop & processing actions.

    Game.grid: object of the Grid class
    Game.robot: object of the Robot class

"""

from Actions import *  # Needed mostly for type-hinting
from Grid import *
from Robot import *


class Game:
    """
        The game has a grid, which holds most of the current game state; the robot is the player's agent.

        The Interface class defines display & control input; the base Interface class is a console mode.

        History will be useful for retracing games; a necessity for advanced functions, e.g. ML
    """

    def __init__(self, size_x: int = DEFAULT_SIZE_X, size_y: int = DEFAULT_SIZE_Y,
                 robot_start: (int, int | None) = None, interface=None, history=None) -> None:
        """
        :param size_x: Horizontal size of Grid
        :param size_y: Vertical size of Grid
        :param robot_start: Robot's starting coordinates
        :param interface: Interface controls
        :param history: History list
        """
        self.grid = None
        self.robot = None
        self.initialise_grid(size_x, size_y, robot_start)

        self.interface = interface

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
        self.grid = Grid(size_x, size_y)
        self.robot = Robot(start=robot_start)

        self.grid.set_tile(self.robot.coords, ROBOT_TOKEN)

    def add_grid_token(self, coords: (int, int), token_symbol: str) -> None:
        """
        Method to add a token to the Game grid

        :param coords: Coordinates of the Grid where a token should be placed.
        :param token_symbol: Token character symbol; see Constants.py
        """
        if not (token_symbol in SET_OF_ITEMS | SET_OF_BINS | SET_OF_MESS):
            # Only Items, Bins, and Messes can be placed for now
            raise ValueError(f"Game.add_grid_token: token_symbol not valid")

        if not self.grid.get_tile(coords).is_empty():
            # This method should not over-write existing tokens
            raise ValueError(f"Game.add_grid_token: tile at co-ordinates {coords} is not empty")

        self.grid.set_tile(coords, token_symbol)

    def get_possible_actions(self) -> [Action]:
        """
        This method determines what possible Actions the Robot may take given the current state of the Grid

        :return: List of Actions; see Actions.py
        """
        actions = []

        for coord in self.grid.get_adjacent_coordinates(self.robot.coords):

            tile = self.grid.get_tile(coord)

            if tile.is_empty():
                # Can move or drop into an empty co-ord
                actions.append(Move(coord))
                if not self.robot.is_stack_empty():
                    actions.append(Drop(coord))
            elif tile.is_bin():
                # Can -- potentially -- drop an item into a bin
                if not self.robot.is_stack_empty():
                    actions.append(Drop(coord))
                else:
                    # Do nothing: logically necessary
                    pass
            elif tile.is_item():
                # Can pick up an item
                actions.append(PickUp(coord))
            elif tile.is_mess():
                # Can sweep a mess
                actions.append(Sweep(coord))
            else:
                # We should never get here
                raise NotImplementedError("Game.get_possible_actions: impossible state")

        return actions

    @staticmethod
    def is_action_type_in_actions(action_name: str, actions: [Action]) -> bool:
        # Not the most efficient of algorithms but there shouldn't be too many actions
        for a in actions:
            if a.__class__.__name__ == action_name:
                return True

        return False

    @staticmethod
    def order_actions_by_coords(actions: [Action]) -> dict[(int, int): set[Action]]:
        ordered_actions = {}
        for a in actions:
            if a.coords in ordered_actions:
                # Add to set
                ordered_actions[a.coords].add(a)
            else:
                # Create set
                ordered_actions[a.coords] = {a}

        return ordered_actions

    def apply_drop(self, drop: Drop) -> bool:
        """
        Apply a Drop Action, if possible.

        :param drop: Drop Action (see Actions.py)
        :return: Has Item been successfully dropped?
        """
        # First, pop the item; if we find nothing, exit
        if not (item := self.robot.drop()):
            return False

        # Can drop into empty tiles or bins; bins are more complicated.
        tile = self.grid.get_tile(drop.coords)

        # Deal with empty tile first, as it's simple
        if tile.is_empty():
            self.grid.set_tile(drop.coords, item)
            return True

        # If we get to here we're dealing with bin tiles; bin logic applies
        if tile.get_content() in ITEMS_TO_BIN_MAP[item]:
            # Accepted bin; we don't need to set the item here, it is "destroyed"
            return True
        else:
            # The robot can't drop the item otherwise so the robot has to pick it up again
            self.robot.pickup(item)
            return False

    def apply_move(self, move: Move) -> None:
        """
        Applies a Move Action. The destination coordinates are in move.coords, and the destination tile should be
        empty; which is a given if the Move Action has been generated by Game.get_possible_actions()

        :param move: Move Action
        """
        # First, double-check that the destination is empty. Throw an error if not
        if not self.grid.get_tile(move.coords).is_empty():
            raise ValueError("Game.apply_move: destination not empty")

        # Clear the old coordinates
        self.grid.get_tile(self.robot.coords).clear()

        # Set the new coordinates
        self.grid.set_tile(move.coords, ROBOT_TOKEN)
        self.robot.coords = move.coords

    def apply_pickup(self, pickup: PickUp) -> None:
        """
        Applies a PickUp Action. This should in principle always be successful as PickUp Actions should be
        curated to be valid, as per Game.get_possible_actions()

        :param pickup: PickUp Action
        """
        tile = self.grid.get_tile(pickup.coords)

        if not tile.is_item():
            # Only Items can be picked up
            raise ValueError("Game.apply_pickup: wrong token type")

        if self.robot.pickup(tile.get_content()):
            tile.clear()

    def apply_sweep(self, sweep: Sweep) -> None:
        """
        Applies a Sweep Action. This should in principle always be successful as Sweep Actions should be curated to be
        valid, as per Game.get_possible_actions()

        :param sweep: Sweep Action
        """
        tile = self.grid.get_tile(sweep.coords)
        if tile.is_mess():
            tile.clear()

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
                if not (i.get_content() in {EMPTY_TILE, ROBOT_TOKEN} | SET_OF_BINS):
                    return False

        # If we get here then the grid is cleared
        return True

    def start(self) -> None:
        """
        The game's control loop.

        User input is defined into Actions; those Actions are then processed.

        """
        if self.interface is None:
            raise Exception("Game.start_control_loop: No Interface set")

        go = True

        # One-off events at the start, e.g. title screen
        self.interface.event_start()

        while go:
            # Stuff that happens at the start of a loop pass, but isn't strictly related to display of the state
            self.interface.event_begin_of_loop()

            # Display the current game state to user
            self.interface.display_state()

            # Listen for action from user; skip this pass if Action is None
            if (action := self.interface.listen_for_action()) is None:
                continue

            # If processing the action returns False,this stops the current While loop
            go = self.interface.process_action(action)

            if self.is_grid_cleared():
                self.interface.event_grid_cleared()
        else:
            # This catches 'go' turning to False, which should be a Quit action
            self.interface.event_quit()


if __name__ == "__main__":
    g = Game()
    print(g.grid)
