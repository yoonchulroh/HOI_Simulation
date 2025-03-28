import json
from game_objects import Team, Unit, TeamController, SimulationController, Tile

def load_units_from_json(json_file: str, blue_controller: TeamController, red_controller: TeamController, simulation_controller: SimulationController):
    units = []
    """
    Loads unit data from a JSON file and assigns units to the provided team controllers.

    Args:
        json_file (str): Path to the JSON file containing unit data.
        blue_controller (TeamController): Controller for the blue team.
        red_controller (TeamController): Controller for the red team.
        simulation_controller (SimulationController): Controller for the simulation.
    Raises:
        ValueError: If the JSON data is missing required keys or contains invalid team values.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Handle both single unit (dict) and multiple units (list)
    if isinstance(data, dict):
        data = [data]  # Convert single dict to a list with one item
    
    for unit_data in data:
        try:
            col = unit_data['col']
            row = unit_data['row']
            team_str = unit_data['team']
            team = Team(team_str)  # Automatically raises ValueError if team_str is invalid
            unit = Unit(col, row, team, simulation_controller)
            if team == Team.BLUE:
                blue_controller.add_unit(unit)
            elif team == Team.RED:
                red_controller.add_unit(unit)
            units.append(unit)
        except KeyError as e:
            raise ValueError(f"Missing key in unit data: {e}")
        except ValueError as e:
            raise e  # Re-raise ValueError from Team(team_str) or add_unit
        
    return units

def initialize_tiles(config_filename: str) -> list[list[Tile]]:
    """
    Loads the config file, reads 'rows' and 'cols', and creates a 2D array of Tile objects.

    Args:
        config_filename (str): The path to the JSON configuration file.

    Returns:
        list[list[Tile]]: A 2D list (rows x cols) of Tile objects.
    """
    with open(config_filename, 'r') as f:
        config = json.load(f)

    rows = config["rows"]
    cols = config["cols"]

    tiles = []
    for x in range(cols):   # x = horizontal
        column_tiles = []
        for y in range(rows):  # y = vertical
            tile = Tile(col=x, row=y) 
            column_tiles.append(tile)
        tiles.append(column_tiles)
        
    return tiles
