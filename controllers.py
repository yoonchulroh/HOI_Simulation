from __future__ import annotations  # For Python 3.7+
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects import Unit, Tile
import gamelogic
import json
import random
from game_objects import Team, Direction

class SimulationController:
    def __init__(self, blue_controller, red_controller, tiles: list[list["Tile"]]):
        """
        Initializes the SimulationController with references to the team controllers.
        """
        self.blue_controller = blue_controller
        self.red_controller = red_controller
        self.units = []
        self.tiles = tiles
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
        self.tiles[unit.col][unit.row].set_affiliation(unit.team)

    def move_unit(self, unit: "Unit", direction: Direction):
        """
        Starts the movement of a unit in the given direction by setting animation parameters.
        The move will be executed gradually based on the unit's speed.
        """
        if unit.is_moving:
            return  # Ignore if already moving

        if not gamelogic.is_move_valid(unit, direction, self.rows, self.cols):
            return

        # Choose movement offsets based on row parity
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
        new_col = unit.col + delta_col
        new_row = unit.row + delta_row

        # Compute movement duration based on unit speed (higher speed => shorter duration)
        base_move_duration = 1000  # milliseconds for a unit with speed 1
        move_duration = base_move_duration / unit.speed

        # Set animation parameters on the unit
        unit.is_moving = True
        unit.move_progress = 0.0
        unit.start_tile = (unit.col, unit.row)
        unit.target_tile = (new_col, new_row)
        unit.move_duration = move_duration
        unit.elapsed_time = 0

    def update(self, delta_time: int):
        """
        Updates the movement of all units based on elapsed time.
        
        Args:
            delta_time (int): Milliseconds elapsed since the last update.
        """
        for unit in self.units:
            if unit.is_moving:
                unit.elapsed_time += delta_time
                # Calculate progress as a value between 0.0 and 1.0
                unit.move_progress = min(unit.elapsed_time / unit.move_duration, 1.0)
                if unit.move_progress >= 1.0:
                    # Movement complete: update unit's grid position and stop the animation
                    unit.is_moving = False
                    unit.col, unit.row = unit.target_tile
                    self.set_tile_affiliation(self.tiles[unit.col][unit.row], unit)

    def set_tile_affiliation(self, tile: "Tile", unit: "Unit"):
        """
        Updates the affiliation of the tile based on the unit's team.
        """
        tile.set_affiliation(unit.team)

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