import game_objects

def is_move_valid(unit: "game_objects.Unit", direction: "game_objects.Direction", rows: int, cols: int) -> bool:
    """
    Checks if a unit's move in the specified direction is valid based on the grid boundaries.

    Args:
        unit_col (int): The current column of the unit.
        unit_row (int): The current row of the unit.
        direction (Direction): The direction in which the unit intends to move (e.g., W, NE, SE, E, SW, NW).

    Returns:
        bool: True if the move is within the grid boundaries, False otherwise.

    Raises:
        ValueError: If the JSON file cannot be loaded, is missing required keys, or contains invalid data.
        ValueError: If an invalid direction is provided.
    """
    

    # Define movement offsets based on row parity (pointy-top, odd-r layout)
    if unit.row % 2 == 0:  # Even row
        offsets = {
            game_objects.Direction.W: (-1, 0),    # West
            game_objects.Direction.NE: (0, -1),   # Northeast
            game_objects.Direction.SE: (0, 1),    # Southeast
            game_objects.Direction.E: (1, 0),     # East
            game_objects.Direction.SW: (-1, 1),   # Southwest
            game_objects.Direction.NW: (-1, -1)   # Northwest
        }
    else:  # Odd row
        offsets = {
            game_objects.Direction.W: (-1, 0),    # West
            game_objects.Direction.NE: (1, -1),   # Northeast
            game_objects.Direction.SE: (1, 1),    # Southeast
            game_objects.Direction.E: (1, 0),     # East
            game_objects.Direction.SW: (0, 1),    # Southwest
            game_objects.Direction.NW: (0, -1)    # Northwest
        }

    # Get the offset for the given direction
    try:
        delta_col, delta_row = offsets[direction]
    except KeyError:
        raise ValueError(f"Invalid direction: {direction}")

    # Calculate the new position
    new_col = unit.col + delta_col
    new_row = unit.row + delta_row

    # Check if the new position is within grid boundaries
    return 0 <= new_col < cols and 0 <= new_row < rows

def calculate_tile_affiliation_percentages(tiles: list[list["game_objects.Tile"]]) -> dict[str, float]:
    """
    Calculates the percentage of tiles affiliated with each team and those with no affiliation.
    
    Args:
        tiles (list[list[Tile]]): A 2D list of Tile objects.

    Returns:
        dict[str, float]: A dictionary mapping "blue", "red", and "none" to their respective percentages.
    """
    total_tiles = 0
    blue_count = 0
    red_count = 0
    
    for row_of_tiles in tiles:
        for tile in row_of_tiles:
            total_tiles += 1
            if tile.affiliation == game_objects.Team.BLUE:
                blue_count += 1
            elif tile.affiliation == game_objects.Team.RED:
                red_count += 1

    if total_tiles == 0:
        # Edge case: if there are no tiles at all
        return {"blue": 0.0, "red": 0.0, "none": 0.0}

    blue_percentage = (blue_count / total_tiles) * 100.0
    red_percentage = (red_count / total_tiles) * 100.0
    none_percentage = 100.0 - (blue_percentage + red_percentage)

    return {
        "blue": blue_percentage,
        "red": red_percentage,
        "none": none_percentage
    }