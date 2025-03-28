import math
import pygame
from game_objects import Team, Unit, Tile
import gamelogic

def hex_corners(center_x, center_y, size):
    """
    Returns the list of (x, y) corner coordinates for a pointy-top hex
    with the given center (center_x, center_y) and hex 'radius' (size).
    """
    corners = []
    for i in range(6):
        # 30° offset ensures a flat side is at the bottom for pointy-top orientation
        angle_deg = 60 * i + 30
        angle_rad = math.radians(angle_deg)
        x = center_x + size * math.cos(angle_rad)
        y = center_y + size * math.sin(angle_rad)
        corners.append((x, y))
    return corners

def draw_hex(surface, center_x, center_y, size, fill_color, outline_color=(0, 0, 0)):
    """
    Draws a single hex on the given 'surface' using Pygame's draw.polygon.
    """
    corners = hex_corners(center_x, center_y, size)
    corners_int = [(int(x), int(y)) for x, y in corners]
    # Draw filled polygon
    pygame.draw.polygon(surface, fill_color, corners_int)
    # Draw outline
    pygame.draw.polygon(surface, outline_color, corners_int, width=1)

def get_hex_center(col: int, row: int, size: float) -> tuple[float, float]:
    """
    Calculates the pixel center of a hex tile given its column, row, and size,
    using an "odd-r" pointy-top layout.

    Args:
        col (int): Column coordinate.
        row (int): Row coordinate.
        size (float): Radius of the hex (distance from center to vertex).

    Returns:
        tuple[float, float]: (center_x, center_y) pixel coordinates.
    """
    offset_x = (math.sqrt(3) * size) * col
    if row % 2 == 1:  # Offset for odd rows in pointy-top hex grid
        offset_x += (math.sqrt(3) / 2) * size
    offset_y = (1.5 * size) * row
    center_x = offset_x + size  # Extra padding
    center_y = offset_y + size
    return center_x, center_y

def draw_tiles(surface: pygame.Surface, tiles: list[list[Tile]], size: float, font: pygame.font.Font) -> None:
    """
    Draws a 2D list of Tile objects on the given surface.

    Args:
        surface (pygame.Surface): The Pygame surface to draw on.
        tiles (list[list[Tile]]): A 2D list of Tile objects.
        size (float): Radius of the hex tile.
        font (pygame.font.Font): Pygame font for rendering the tile coordinates.
    """
    for row_of_tiles in tiles:
        for tile in row_of_tiles:
            # Determine the hex center based on tile's col and row
            center_x, center_y = get_hex_center(tile.col, tile.row, size)

            fill_color = tile.get_affiliation_color()

            # Draw the hex
            draw_hex(surface, center_x, center_y, size, fill_color)

            # Optionally render the coordinates on top
            text = font.render(f"({tile.col}, {tile.row})", True, (0, 0, 0))
            text_rect = text.get_rect(center=(center_x, center_y))
            surface.blit(text, text_rect)

def draw_units(surface: pygame.Surface, units: list[Unit], size: float) -> None:
    """
    Draws units on the hex grid as colored circles.

    Args:
        surface (pygame.Surface): The Pygame surface to draw on.
        units (list[Unit]): List of Unit instances to draw.
        size (float): Radius of the hex, used to scale the unit circle.
    """
    for unit in units:
        center_x, center_y = get_hex_center(unit.col, unit.row, size)
        color = (0, 0, 255) if unit.team == Team.BLUE else (255, 0, 0)
        pygame.draw.rect(surface, color, (int(center_x)-int(size/2), int(center_y)-int(size/2), int(size), int(size)))

def render_affiliation_stats(
    surface: pygame.Surface, 
    tiles: list[list[Tile]], 
    font: pygame.font.Font,
    position: tuple[int, int] = (10, 10)
):
    """
    Renders the affiliation stats (percentages) onto the provided Pygame surface.

    Args:
        surface (pygame.Surface): The surface to draw on (typically the screen).
        stats (dict[str, float]): A dictionary like {"blue": 40.0, "red": 35.0, "none": 25.0}.
        font (pygame.font.Font): A Pygame Font object for rendering text.
        position (tuple[int, int]): The (x, y) position where text should start.
    """
    stats = gamelogic.calculate_tile_affiliation_percentages(tiles)

    text_str = (
        f"Blue: {stats['blue']:.2f}%  |  "
        f"Red: {stats['red']:.2f}%  |  "
        f"None: {stats['none']:.2f}%"
    )
    text_surface = font.render(text_str, True, (0, 0, 0))  # Render in black
    surface.blit(text_surface, position)  # Blit at the specified (x, y)