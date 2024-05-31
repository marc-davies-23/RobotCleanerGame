"""
    Actions here mean user input actions that translate into robot/program functions.

    The Action class itself is in effect an abstract class. Other classes inherit Action to define robot/program
    controls.

    The approach of having a separate class for every action may be a little over-engineered but the complexity of
    actions could increase with future functionality; thus the concept is hopefully future-proof.
"""


class Action:
    """
        The base Action class is essentially an abstract class, and a placeholder for further functionality
        as necessary.
    """
    pass


class ActionWithCoords(Action):
    """
        Second abstract class; this is an action with coords
    """

    def __init__(self, coords: (int, int)) -> None:
        """
        :param coords: Co-ordinates tuple of form (x, y)
        """
        self.coords = coords


class Drop(ActionWithCoords):
    """
        Action for the Robot to drop the top of its stack
    """
    pass


class Move(ActionWithCoords):
    """
        Action for the Robot to move to coords
    """
    pass


class PickUp(ActionWithCoords):
    """
        Action for Robot to try to pick up something from coords
    """
    pass


class Quit(Action):
    """
        Action to Quit current game
    """
    pass


class Refresh(Action):
    """
        Action to refresh display of game state
    """
    pass


class Sweep(ActionWithCoords):
    """
        Action to Sweep something from board
    """
    pass


if __name__ == "__main__":
    print(Move.__name__)
