from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controllers import SimulationController, TeamController
from enum import Enum

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
    def __init__(self, col: int, row: int, team: Team, speed: int, simulation_controller: "SimulationController"):
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
        self.speed = speed
        self.simulation_controller = simulation_controller
        self.simulation_controller.add_unit(self)
        # Movement variables
        self.is_moving = False
        self.move_progress = 0.0
        self.start_tile = (col, row)
        self.target_tile = (col, row)
        self.move_duration = 0  # in milliseconds
        self.elapsed_time = 0

    def move(self, direction: Direction):
        """
        Requests the SimulationController to move the unit in the specified direction.

        Args:
            direction (Direction): The direction to move the unit in.
        """
        self.simulation_controller.move_unit(self, direction)

    def __str__(self):
        """
        Returns a string representation of the unit.

        Returns:
            str: A string in the format "Unit at (col, row), team: team_value"
        """
        return f"Unit at ({self.col}, {self.row}), team: {self.team.value}"

class Tile:
    """
    Represents a single hex tile on the map.
    """
    def __init__(self, col: int, row: int, affiliation: Team = None):
        """
        Initialize a Tile with grid coordinates and optional affiliation.

        Args:
            col (int): The column (hex coordinate).
            row (int): The row (hex coordinate).
            affiliation (Team, optional): The team (BLUE or RED) that owns this tile, if any.
        """
        self.col = col
        self.row = row
        self.affiliation = affiliation  # This can be None if the tile is neutral

    def set_affiliation(self, team: Team):
        """
        Sets the affiliation of this tile to the provided Team enum value.

        Args:
            team (Team): The team to affiliate with the tile.
        """
        self.affiliation = team

    def get_affiliation_color(self) -> tuple:
        """
        Returns the color representing the tile's affiliation.

        Returns:
            tuple: (R, G, B) color values.
        """
        if self.affiliation == Team.BLUE:
            return (150, 150, 255)  # Light bluish color to denote Blue affiliation
        elif self.affiliation == Team.RED:
            return (255, 150, 150)  # Light reddish color to denote Red affiliation
        else:
            return (200, 200, 200)  # Neutral gray