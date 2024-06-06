"""

    This class is the generic console interface between player & program

"""

import Actions as Ac
from Constants import QUIT_MESSAGE
import string


class Interface:
    def __init__(self, game=None) -> None:
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

    def listen_for_action(self):
        # Child Interfaces may return None to skip a pass in their control loop
        lookup = {}

        print(f"Please select an action:")
        for count, act in enumerate(self.game.get_possible_actions()):
            disp_count = count + 1

            print(f"{disp_count} : ", end="")
            match act.__class__.__name__:
                case Ac.Drop.__name__:
                    print(f"drop to {act.coords}")
                case Ac.Move.__name__:
                    print(f"move to {act.coords}")
                case Ac.PickUp.__name__:
                    print(f"pick-up from {act.coords}")
                case Ac.Sweep.__name__:
                    print(f"sweep {act.coords}")
                case _:
                    raise ValueError(f"Interface.action_list_feedback: {act.__class__.__name__} not matched")

            lookup[disp_count] = act

        # Refresh command
        print(f"R : Refresh")
        lookup["r"] = Ac.Refresh(self)

        # Quit command
        print(f"Q : Quit")
        lookup["q"] = Ac.Quit(self)

        selected = request_input("\nSelect action: ", validation_values=list(lookup.keys()))

        return lookup[selected]

    def give_user_feedback(self, feedback: str) -> None:
        # Might need to be an instance class with inheritance
        print(feedback)

    def process_action(self, action) -> bool:
        # Boolean return determines whether the action is a stopper or not; False = stop

        # Store move
        if self.game is not None:
            self.game.history.append(action)

        if action:
            feedback = action.execute()
            if feedback:
                self.give_user_feedback(feedback)

            if feedback == QUIT_MESSAGE:
                return False

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

    def start(self) -> None:
        """
        The control loop.

        User input is defined into Actions; those Actions are then processed.

        """
        go = True

        # One-off events at the start, e.g. title screen
        self.event_start()

        while go:
            # Stuff that happens at the start of a loop pass, but isn't strictly related to display of the state
            self.event_begin_of_loop()

            # Display the current game state to user
            self.display_state()

            # Listen for action from user; skip this pass if Action is None
            if (action := self.listen_for_action()) is None:
                continue

            # If processing the action returns False,this stops the current While loop
            go = self.process_action(action)

            if self.game is not None and self.game.is_grid_cleared():
                self.event_grid_cleared()
        else:
            # This catches 'go' turning to False, which should be a Quit action
            self.event_quit()


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
