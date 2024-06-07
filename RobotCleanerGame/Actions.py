"""
    Actions here mean user input actions that translate into robot/program functions.

    The Action class itself is in effect an abstract class. Other classes inherit Action to define robot/program
    controls.

    The approach of having a separate class for every action may be a little over-engineered but the complexity of
    actions could increase with future functionality; thus the concept is hopefully future-proof.
"""
import Constants as Co
import PyGameConstants as PCo


class Feedback:
    def __init__(self, message=None, quit_flag=False):
        self.message = message
        self.quit = quit_flag


class Action:
    """
        The base Action class is essentially an abstract class, and a placeholder for further functionality
        as necessary.
    """

    def __init__(self, interface):
        self.interface = interface

    def execute(self) -> Feedback:
        return Feedback()


class PyGameAction:
    """
        Action for executing on more dynamic PyGame Interface
    """

    def __init__(self, interface):
        self.interface = interface

    def execute(self) -> Feedback:
        return Feedback()


class ActionWithCoords(Action):
    """
        Second abstract class; this is an action with coords
    """

    def __init__(self, interface, coords: (int, int)) -> None:
        """
        :param coords: Co-ordinates tuple of form (x, y)
        """
        super().__init__(interface)
        self.coords = coords


class Drop(ActionWithCoords):
    """
        Action for the Robot to drop the top of its stack
    """

    def execute(self) -> Feedback:
        """
        Attempt to execute a Drop action.

        :return: Feedback message
        """
        # Deduct a point of score
        self.interface.game.change_score()

        # Pop the item; if we find nothing, exit
        if not (item := self.interface.game.robot.drop()):
            return Feedback("Nothing to drop!")

        # Can drop into empty tiles or bins; bins are more complicated.
        tile = self.interface.game.grid.get_tile(self.coords)

        # Deal with empty tile first, as it's simple
        if tile.is_empty():
            self.interface.game.grid.set_tile(self.coords, item)
            return Feedback()  # Empty feedback message

        # If we get to here we're dealing with bin tiles; bin logic applies
        if tile.get_content() in Co.ITEMS_TO_BIN_MAP[item]:
            # Accepted bin; we don't need to set the item here, it is "destroyed"
            if tile.get_content() == Co.UNIVERSAL_BIN:
                self.interface.game.change_score(Co.SCORING["half"])
            else:
                self.interface.game.change_score(Co.SCORING["full"])
            return Feedback()  # Empty feedback message
        else:
            # The robot can't drop the item otherwise so the robot has to pick it up again
            self.interface.game.robot.pickup(item)
            return Feedback("Wrong bin, drop failed!")


class GoToMenu(PyGameAction):
    """
        Action to tell the game to load the menu
    """

    def execute(self) -> Feedback:
        self.interface.state[PCo.CURRENT_SCREEN] = PCo.MENU_SCREEN
        return Feedback()


class Move(ActionWithCoords):
    """
        Action for the Robot to move to coords
    """

    def execute(self) -> Feedback:
        """
        Attempt to execute a Move action.

        :return: Feedback message
        """
        # Deduct a point of score
        self.interface.game.change_score()

        # Check-check that the destination is empty. Throw an error if not
        if not self.interface.game.grid.get_tile(self.coords).is_empty():
            return Feedback("Destination not empty")

        # Clear the old coordinates
        self.interface.game.grid.get_tile(self.interface.game.robot.coords).clear()

        # Set the new coordinates
        self.interface.game.grid.set_tile(self.coords, Co.ROBOT_TOKEN)
        self.interface.game.robot.coords = self.coords

        return Feedback()


class PickUp(ActionWithCoords):
    """
        Action for Robot to try to pick up something from coords
    """

    def execute(self) -> Feedback:
        """
        Attempt to execute a PickUp action.

        :return: Feedback message
        """
        # Deduct a point of score
        self.interface.game.change_score()

        tile = self.interface.game.grid.get_tile(self.coords)

        if not tile.is_item():
            return Feedback("Only Items can be picked up")

        if self.interface.game.robot.pickup(tile.get_content()):
            tile.clear()

        return Feedback()


class Quit(Action):
    """
        Action to quit
    """

    def execute(self) -> Feedback:
        return Feedback(Co.QUIT_MESSAGE, True)


class Refresh(Action):
    """
        Action to refresh display of game state
    """

    def execute(self) -> Feedback:
        self.interface.display_state()
        return Feedback(Co.REFRESH_MESSAGE)


class Sweep(ActionWithCoords):
    """
        Action to Sweep something from board
    """

    def execute(self) -> Feedback:
        # Deduct a point of score
        self.interface.game.change_score()

        tile = self.interface.game.grid.get_tile(self.coords)

        if tile.is_mess():
            tile.clear()
            self.interface.game.change_score(Co.SCORING["sweep"])

        return Feedback()


if __name__ == "__main__":
    pass
