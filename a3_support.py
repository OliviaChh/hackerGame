from typing import Tuple, Optional, Dict, List

PLAYER = "P"
COLLECTABLE = "C"
DESTROYABLE = "D"
BLOCKER = "B"
BOMB = "O"

MOVE = (0, -1)
FIRE = (0, 1)
ROTATIONS = ((-1, 0), (1, 0))
SPLASH = ((0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1), (0, -1),
          (1, 0), (-1, 0))
LEFT = "A"
RIGHT = "D"
DIRECTIONS = (LEFT, RIGHT)
COLLECTION_TARGET = 7

COLLECT = "RETURN"
DESTROY = "SPACE"
SHOT_TYPES = (DESTROY, COLLECT)

ENTITY_TYPES = (COLLECTABLE, DESTROYABLE)
MAP_WIDTH = MAP_HEIGHT = 400
SCORE_WIDTH = 200
BAR_HEIGHT = 150

TASK = 2
TITLE = "HACKER"
TITLE_BG = "#222222"
TITLE_FONT = ('Arial', 28)

COLOURS = {COLLECTABLE: "#9FD7D5",
           DESTROYABLE: "#F93A3A",
           BLOCKER: "#B2B2B2",
           PLAYER: "#A482DB",
           BOMB: "#FF7324"}

FIELD_COLOUR = "#2D3332"
SCORE_COLOUR = "#332027"
PLAYER_AREA = "#8E8E8E"

IMAGES = {COLLECTABLE: "C.png",
          DESTROYABLE: "D.png",
          BLOCKER: "B.png",
          PLAYER: "P.png",
          BOMB: "O.png"}

GRID_SIZE = 7


class Position:
    """
    The position class represents a location in a 2D grid.

    A position is made up of an x coordinate and a y coordinate.
    The x and y coordinates are assumed to be non-negative whole numbers which
    represent a square in a 2D grid.

    Examples:
        >>> position = Position(2, 4)
        >>> position
        Position(2, 4)
        >>> position.get_x()
        2
        >>> position.get_y()
        4
    """

    def __init__(self, x: int, y: int):
        """
        The position class is constructed from the x and y coordinate which the
        position represents.

        Parameters:
            x: The x coordinate of the position
            y: The y coordinate of the position
        """
        self._x = x
        self._y = y

    def get_x(self) -> int:
        """Returns the x coordinate of the position."""
        return self._x

    def get_y(self) -> int:
        """Returns the y coordinate of the position."""
        return self._y

    def add(self, position: "Position") -> "Position":
        """
        Add a given position to this position and return a new instance of
        Position that represents the cumulative location.

        This method shouldn't modify the current position.

        Examples:
            >>> start = Position(1, 2)
            >>> offset = Position(2, 1)
            >>> end = start.add(offset)
            >>> end
            Position(3, 3)

        Parameters:
            position: Another position to add with this position.

        Returns:
            A new position representing the current position plus
            the given position.
        """
        return Position(self._x + position.get_x(), self._y + position.get_y())

    def subtract(self, position: "Position") -> "Position":
        """
        Add a given position to this position and return a new instance of
        Position that represents the cumulative location.

        This method shouldn't modify the current position.

        Examples:
            >>> start = Position(1, 2)
            >>> offset = Position(2, 1)
            >>> end = start.add(offset)
            >>> end
            Position(3, 3)

        Parameters:
            position: Another position to add with this position.

        Returns:
            A new position representing the current position plus
            the given position.
        """
        return Position(self._x - position.get_x(), self._y - position.get_y())

    def __eq__(self, other: object) -> bool:
        """
        Return whether the given other object is equal to this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are equal, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        # an __eq__ method needs to support any object for example
        # so it can handle `Position(1, 2) == 2`
        # https://www.pythontutorial.net/python-oop/python-__eq__/
        if not isinstance(other, Position):
            return False
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __hash__(self) -> int:
        """
        Calculate and return a hash code value for this position instance.

        This allows Position instances to be used as keys in dictionaries.

        A hash should be based on the unique data of a class, in the case
        of the position class, the unique data is the x and y values.
        Therefore, we can calculate an appropriate hash by hashing a tuple of
        the x and y values.

        Reference: https://stackoverflow.com/questions/17585730/what-does-hash-do-in-python
        """
        return hash((self.get_x(), self.get_y()))

    def __repr__(self) -> str:
        """
        Return the representation of a position instance.

        The format should be 'Position({x}, {y})' where {x} and {y} are replaced
        with the x and y value for the position.

        Examples:
            >>> repr(Position(12, 21))
            'Position(12, 21)'
            >>> Position(12, 21).__repr__()
            'Position(12, 21)'
        """
        return f"Position({self.get_x()}, {self.get_y()})"

    def __str__(self) -> str:
        """
        Return a string of this position instance.

        The format should be 'Position({x}, {y})' where {x} and {y} are replaced
        with the x and y value for the position.
        """
        return self.__repr__()

    def __lt__(self, other: object) -> bool:
        """
        Return whether the given other object is less than this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are less than the other x and y coordinates,
        return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x < other.get_x():
            return True
        if self._y < other.get_y():
            return True
        return False

    def __le__(self, other: object) -> bool:
        """
        Return whether the given other object is less than or equal to
        this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are less than or equal to the other x and y
        coordinates, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x <= other.get_x():
            return True
        if self._y <= other.get_y():
            return True
        return False

    def __gt__(self, other: object) -> bool:
        """
        Return whether the given other object is greater than this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are greater than the other x and y coordinates,
        return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x > other.get_x():
            return True
        if self._y > other.get_y():
            return True
        return False

    def __ge__(self, other: object) -> bool:
        """
        Return whether the given other object is greater than or equal to
        this position.

        If the other object is not a Position instance, returns False.
        If the other object is a Position instance and the
        x and y coordinates are greater than or equal to the other x and y
        coordinates, return True.

        Parameters:
            other: Another instance to compare with this position.
        """
        if not isinstance(other, Position):
            return False
        if self._y == other.get_y() and self._x >= other.get_x():
            return True
        if self._y >= other.get_y():
            return True
        return False
