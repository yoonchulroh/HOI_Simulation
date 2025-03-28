from enum import Enum
import random

# Define the Team enumeration for blue and red teams
class Team(Enum):
    BLUE = "blue"
    RED = "red"

class Direction(Enum):
    W = "west"
    NE = "northeast"
    SE = "southeast"
    E = "east"
    SW = "southwest"
    NW = "northwest"

# Define the Unit class
class Unit:
    def __init__(self, col: int, row: int, team: Team):
        """
        Initializes a Unit with its location and team affiliation.

        Args:
            col (int): The column coordinate of the hex tile.
            row (int): The row coordinate of the hex tile.
            team (Team): The team affiliation, either Team.BLUE or Team.RED.
        """
        self.col = col
        self.row = row
        self.team = team

    def move(self, direction: Direction):
        if self.row % 2 == 0:  # Even row
            offsets = {
                Direction.W: (-1, 0),
                Direction.NE: (0, -1),
                Direction.SE: (0, 1),
                Direction.E: (1, 0),
                Direction.SW: (-1, 1),
                Direction.NW: (-1, -1)
            }
        else:  # Odd row
            offsets = {
                Direction.W: (-1, 0),
                Direction.NE: (1, -1),
                Direction.SE: (1, 1),
                Direction.E: (1, 0),
                Direction.SW: (0, 1),
                Direction.NW: (0, -1)
            }
        delta_col, delta_row = offsets[direction]
        self.col += delta_col
        self.row += delta_row

    def __str__(self):
        """
        Returns a string representation of the unit.

        Returns:
            str: A string in the format "Unit at (col, row), team: team_value"
        """
        return f"Unit at ({self.col}, {self.row}), team: {self.team.value}"

class TeamController:
    def __init__(self, team: Team):
        self.team = team
        self.units = []

    def add_unit(self, unit: Unit):
        if unit.team != self.team:
            raise ValueError(f"Cannot add unit of team {unit.team} to controller of team {self.team}")
        self.units.append(unit)

    def move_units_randomly(self):
        """Move all units to a random adjacent hex."""
        directions = list(Direction)  # Get all possible directions (N, NE, SE, S, SW, NW)
        for unit in self.units:
            random_direction = random.choice(directions)  # Pick a random direction
            unit.move(random_direction)  # Move the unit in that direction