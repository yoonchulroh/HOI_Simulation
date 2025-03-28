from enum import Enum
import random
import json
import gamelogic

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

class SimulationController:
    def __init__(self, blue_controller, red_controller):
        """
        Initializes the SimulationController with references to the team controllers.

        Args:
            blue_controller (TeamController): Controller for the blue team.
            red_controller (TeamController): Controller for the red team.
        """
        self.blue_controller = blue_controller
        self.red_controller = red_controller
        self.units = []
        blue_controller.simulation_controller = self
        red_controller.simulation_controller = self
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            self.rows = config['rows']
            self.cols = config['cols']
            if not isinstance(self.rows, int) or not isinstance(self.cols, int) or self.rows <= 0 or self.cols <= 0:
                raise ValueError("Grid dimensions must be positive integers.")
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading grid dimensions from config.json: {e}")


    def add_unit(self, unit: "Unit"):
        """
        Adds a unit to the simulation.
        """
        self.units.append(unit)

    def move_unit(self, unit: "Unit", direction: Direction):
        if not gamelogic.is_move_valid(unit, direction, self.rows, self.cols):
            return

        if unit.row % 2 == 0:  # Even row
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
        unit.col += delta_col
        unit.row += delta_row

# Define the Unit class
class Unit:
    def __init__(self, col: int, row: int, team: Team, simulation_controller: "SimulationController"):
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
        self.simulation_controller = simulation_controller
        self.simulation_controller.add_unit(self)

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

class TeamController:
    def __init__(self, team: Team):
        self.team = team
        self.units = []
        self.simulation_controller = None

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

