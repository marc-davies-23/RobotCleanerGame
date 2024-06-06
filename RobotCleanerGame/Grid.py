"""

    Defines the classes for grid & tiles on which the game is played

"""
from Constants import *

class Tile:
    """
        A single tile (or square) on the grid
    """

    def __init__(self) -> None:
        """
         Tiles start off empty
        """
        self.__content = EMPTY_TILE

    def __str__(self) -> str:
        return self.__content

    def __repr__(self) -> str:
        return self.__content

    def is_bin(self) -> bool:
        """
        Does the Tile hold a bin token?

        :return: True/False that the Tile holds a bin.
        """
        return self.__content in SET_OF_BINS

    def is_empty(self) -> bool:
        """
        Is the Tile Empty?

        :return: True/False that the Tile is empty.
        """
        return self.__content == EMPTY_TILE

    def is_item(self) -> bool:
        """
        Does the Tile hold an item token?

        :return: True/False that the Tile holds an item.
        """
        return self.__content in SET_OF_ITEMS

    def is_mess(self) -> bool:
        """
        Does the Tile hold a mess token?

        :return: True/False that the Tile holds a mess.
        """
        return self.__content in SET_OF_MESS

    def get_content(self) -> str:
        """
        Get the content of the tile
        :return: Empty Tile, or Token
        """
        return self.__content

    def set_content(self, new_content) -> bool:
        """
        Set the content of the Tile
        :param new_content: New content
        :return: OK/ Not OK
        """
        if self.is_empty():
            self.__content = new_content
            return True  # OK
        else:
            return False  # Not OK

    def clear(self) -> None:
        """
        Set tile to Empty Tile
        """
        self.__content = EMPTY_TILE


class Grid:
    def __init__(self, x: int = DEFAULT_SIZE_X, y: int = DEFAULT_SIZE_Y) -> None:
        self.grid = []
        self.size_x = x
        self.size_y = y
        for j in range(y):
            row = []
            for i in range(x):
                row.append(Tile())
            self.grid.append(row)

    def __str__(self) -> str:
        out = ""
        for j in self.grid:
            for i in j:
                out = out + i.get_content()
            out = out + "\n"

        return out

    def get_tile(self, coordinates: (int, int)) -> Tile:
        """
        Returns the Tile at the given coordinates.

        :param coordinates: (x, y) coordinates
        :return: Tile
        """
        return self.grid[coordinates[1]][coordinates[0]]

    def get_adjacent_coordinates(self, from_cds: (int, int)) -> [(int, int)]:
        """
        Get the tiles next to a given input coordinate.

        :param from_cds: From coordinate (x, y)
        :return: List of adjacent coordinates
        """
        adjacent_coordinates: [(int, int)] = []

        for move in MOVE_LIST:
            x = from_cds[0] + move[0]
            if x < 0 or x >= self.size_x:
                # If negative or too big, not a valid coordinate
                continue

            y = from_cds[1] + move[1]
            if y < 0 or y >= self.size_y:
                # If negative or too big, not a valid coordinate
                continue

            adjacent_coordinates.append((x, y))

        return adjacent_coordinates

    def set_tile(self, coordinates: (int, int), content) -> None:
        """
        Set the content of a Tile.

        :param coordinates: (x, y) coordinates of Tile
        :param content: content of Tile
        """
        if not self.grid[coordinates[1]][coordinates[0]].set_content(content):
            raise ValueError(f"Grid.set_tile: could not set content")


if __name__ == "__main__":
    print(grid := Grid())
