import pygame
import numpy as np
from App.Classes.ExampleRectangle import ExampleRectangle

pygame.init()

# Create global constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOUR = (0, 0, 0)
N_CELLS = 100
CELL_WIDTH = WINDOW_WIDTH / N_CELLS
CELL_HEIGHT = WINDOW_HEIGHT / N_CELLS
HEAT_SLOWNESS = 50

# Create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('BrainChild')

# Instantiate an ExampleRectangle
exampleRectangle = ExampleRectangle(100, 100, 20, 20)

# Create various map layers
temperature_map = np.random.rand(N_CELLS, N_CELLS)

# A target surface to draw temp related stuff to
temperature_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
temperature_surface.set_alpha(64)  # Up to 128

# Keep running until user clicks the exit button
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Update the example rectangle
    exampleRectangle.step(keys)

    # Fills the window with the background colour
    window.fill(BACKGROUND_COLOUR)

    # Draws the example rectangle
    exampleRectangle.draw(window)

    # Draw heatmap
    for x in range(0, N_CELLS):
        for y in range(0, N_CELLS):
            pygame.draw.rect(temperature_surface,
                             (temperature_map[x, y] * 255, 0, 0),
                             (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    # Propagate heat
    new_temperature_map = temperature_map.copy() * HEAT_SLOWNESS
    new_temperature_map[1:, :] += temperature_map[:-1, :]
    new_temperature_map[:-1, :] += temperature_map[1:, :]
    new_temperature_map[:, 1:] += temperature_map[:, :-1]
    new_temperature_map[:, :-1] += temperature_map[:, 1:]
    new_temperature_map /= HEAT_SLOWNESS + 4
    temperature_map = new_temperature_map

    # Add the heatmap to the visible surface
    window.blit(temperature_surface, (0, 0))

    # Sends update to the actual window
    pygame.display.update()

pygame.quit()
