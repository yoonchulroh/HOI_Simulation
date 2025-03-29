import sys
import pygame
import controllers
import renderer
import initialization

# --- MAIN LOOP ---

def main():
    screen, fps, hex_size = initialization.initialize_simulation("config.json")
    clock = pygame.time.Clock()
    running = True

    # Initialize controllers for both teams
    blue_controller = controllers.TeamController(controllers.Team.BLUE)
    red_controller = controllers.TeamController(controllers.Team.RED)

    # Load units from the JSON file and assign them to the controllers
    tiles = initialization.initialize_tiles("config.json")
    simulation_controller = controllers.SimulationController(blue_controller, red_controller, tiles)
    units = initialization.load_units_from_json("units.json", blue_controller, red_controller, simulation_controller)
    render_controller = renderer.RenderController(screen, fps, hex_size, tiles, units)

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        blue_controller.move_units_randomly()  # Moves all blue units randomly
        red_controller.move_units_randomly()  # Moves all red units randomly
        delta_time = clock.tick(fps)
        simulation_controller.update(delta_time)
        # 3) Draw the hex grid with coordinates
        render_controller.draw_map()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()