import math
import pygame
from game_objects import Team, Unit

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

def draw_hex_grid(surface, rows, cols, size, font):
    """
    Draws a grid (rows x cols) of pointy-top hexes using an "odd-r" horizontal layout.
    - rows: number of rows
    - cols: number of columns
    - size: 'radius' of each hex
    - font: Pygame font object for rendering coordinates
    """
    for row in range(rows):
        for col in range(cols):
            offset_x = (math.sqrt(3) * size) * col
            # Shift every odd row
            if row % 2 == 1:
                offset_x += (math.sqrt(3)/2) * size

            offset_y = (1.5 * size) * row
            center_x = offset_x + size  # + size for padding
            center_y = offset_y + size

            # Draw the hexagon
            draw_hex(surface, center_x, center_y, size,
                     fill_color=(200, 200, 200),  # light gray
                     outline_color=(0, 0, 0))     # black outline

            # Render and draw the coordinates
            text = font.render(f"({col}, {row})", True, (0, 0, 0))  # Black text
            text_rect = text.get_rect(center=(center_x, center_y))
            surface.blit(text, text_rect)

def get_hex_center(col: int, row: int, size: float) -> tuple[float, float]:
    """
    Calculates the pixel center of a hex tile given its column, row, and size.

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
    center_x = offset_x + size  # Adjust for padding
    center_y = offset_y + size
    return center_x, center_y

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