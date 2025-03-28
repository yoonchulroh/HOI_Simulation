import sys
import pygame
import json
import game_objects  # Kept as in original code, though unused here
import renderer
import initialization
from enum import Enum

# --- HELPER FUNCTIONS ---

def load_config(filename):
    """
    Loads a JSON file and returns a dictionary of config values.
    """
    with open(filename, 'r') as f:
        return json.load(f)

# --- MAIN LOOP ---

def main():
    # 1) Load settings from the JSON config
    config = load_config("config.json")

    # 2) Extract config values
    window_width = config.get("window_width", 800)
    window_height = config.get("window_height", 600)
    fps = config.get("fps", 60)
    rows = config.get("rows", 5)
    cols = config.get("cols", 6)
    hex_size = config.get("hex_size", 40)

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Hex Grid Visualization (Pygame)")

    # Initialize font with size based on hex_size
    font_size = int(hex_size / 2)  # Scale font size with hex size
    font = pygame.font.Font(None, font_size)  # Use default font

    clock = pygame.time.Clock()
    running = True

    # Initialize controllers for both teams
    blue_controller = game_objects.TeamController(game_objects.Team.BLUE)
    red_controller = game_objects.TeamController(game_objects.Team.RED)
    simulation_controller = game_objects.SimulationController(blue_controller, red_controller)

    # Load units from the JSON file and assign them to the controllers
    units = initialization.load_units_from_json("units.json", blue_controller, red_controller, simulation_controller)

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # White background

        blue_controller.move_units_randomly()  # Moves all blue units randomly
        red_controller.move_units_randomly()  # Moves all red units randomly

        # 3) Draw the hex grid with coordinates
        renderer.draw_hex_grid(screen, rows, cols, hex_size, font)
        renderer.draw_units(screen, units, hex_size)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()