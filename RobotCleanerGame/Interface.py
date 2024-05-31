"""

    This class is the generic console interface between player & program

"""

from Game import *

import string


class Interface:
    def __init__(self, game) -> None:
        self.game = game

    def display_state(self) -> None:
        if self.game.grid:
            print(self.game.grid)
        else:
            print(f"Grid not initialised")

        if self.game.robot:
            if self.game.robot.stack:
                print(f"Stack > ", end="")
                max_idx = len(self.game.robot.stack) - 1
                for index, item in enumerate(self.game.robot.stack):
                    if index == max_idx:
                        end = "\n"
                    else:
                        end = ", "
                    print(f"{item}", end=end)
            else:
                print(f"Stack > empty")
            print("")
        else:
            print(f"Robot not initialised")

    def listen_for_action(self) -> (Action | None):
        # Child Interfaces may return None to skip a pass in their control loop
        lookup = {}

        print(f"Please select an action:")
        for count, a in enumerate(self.game.get_possible_actions()):
            disp_count = count + 1
            print(f"{disp_count} : ", end="")
            match a.__class__.__name__:
                case Drop.__name__:
                    print(f"drop to {a.coords}")
                case Move.__name__:
                    print(f"move to {a.coords}")
                case PickUp.__name__:
                    print(f"pick-up from {a.coords}")
                case Sweep.__name__:
                    print(f"sweep {a.coords}")
                case _:
                    raise ValueError(f"Interface.action_list_feedback: {a.__class__.__name__} not matched")

            lookup[disp_count] = a

        # Refresh command
        print(f"R : Refresh")
        lookup["r"] = Refresh()

        # Quit command
        print(f"Q : Quit")
        lookup["q"] = Quit()

        selected = request_input("\nSelect action: ", validation_values=list(lookup.keys()))

        return lookup[selected]

    def give_user_feedback(self, feedback: str) -> None:
        # Might need to be an instance class with inheritance
        print(feedback)

    def process_action(self, action) -> bool:
        # Boolean return determines whether the action is a stopper or not; False = stop

        # Store move
        self.game.history.append(action)

        # Match Action
        match action.__class__.__name__:
            case Drop.__name__:
                if not self.game.apply_drop(action):
                    self.give_user_feedback("Drop failed!")
            case Move.__name__:
                self.game.apply_move(action)
            case PickUp.__name__:
                self.game.apply_pickup(action)
            case Refresh.__name__:
                self.display_state()
            case Sweep.__name__:
                self.game.apply_sweep(action)
            case Quit.__name__:
                return False  # Don't continue
            case _:
                raise ValueError(f"Interface.process_action: {action.__class__.__name__} not matched")

        # Continue by default
        return True

    def event_start(self) -> None:
        pass

    def event_begin_of_loop(self) -> None:
        pass

    def event_grid_cleared(self) -> None:
        # This method isn't static as it may be used for more complex functionality via inheritance
        self.give_user_feedback(f"\nGRID CLEARED!\n")

    def event_quit(self) -> None:
        # This method isn't static as it may be used for more complex functionality via inheritance
        self.give_user_feedback(f"\nQuitting game.")


def request_input(prompt: str, validation_values=None, convert_to_int=True, convert_to_lowercase=True) -> str:
    """
        Takes input from the console and validates it.
    :param prompt: Prompt for user
    :param validation_values: List of valid values
    :param convert_to_int: Should input be converted to int?
    :param convert_to_lowercase: Should input be converted to lowercase?
    :return:
    """
    if validation_values is None:
        validation_values = []

    while True:
        try:
            received = input(prompt)

            if convert_to_int and received in string.digits:
                received = int(received)
            elif convert_to_lowercase and not (received in string.digits):
                received = received.lower()

            if received in validation_values or not validation_values:
                return received
            else:
                print("Value not accepted, please try again.\n")
        except ValueError:
            print("Value error, please try again.\n")


if __name__ == "__main__":
    pass
