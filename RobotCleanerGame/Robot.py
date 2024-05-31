"""

    This class defines the robot agent.

    .location: the robot agent's location, defined here by x,y coordinates
    .stack: the robot's carry stack. It can carry up to MAX_CARRY items

    .pickup(): the robot picks up an item
    .drop(): the robot drops an item it is carrying; it must drop the "topmost" item
    .sweep(): the robot sweeps the mess from a square; it can only do this when it is carrying at most MAX_SWEEP items
    .is_stack_empty(): checks whether robot's stack is empty or not

"""

MAX_CARRY = 3
MAX_SWEEP = 1


class Robot:
    def __init__(self, start=None, stack=None):
        if start is None:
            start = (0, 0)
        if stack is None:
            stack = []
        self.coords = start
        self.stack = stack

    def pickup(self, item):
        if len(self.stack) < MAX_CARRY:
            self.stack.append(item)
            return True  # OK
        else:
            return False  # Not OK

    def drop(self):
        if len(self.stack) > 0:
            return self.stack.pop()  # OK
        else:
            return None  # Not OK

    def is_stack_empty(self):
        return self.stack == []

    """#TBD
    def sweep(self):
        if len(self.stack) >= MAX_SWEEP:
            return 1  # OK
        else:
            return 0  # Not OK"""


if __name__ == "__main__":
    pass
