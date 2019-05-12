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

# Initial example rectangle
x = 50
y = 50
width = 40
height = 60
speed = 5

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

    # Initial frame rate limit
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move the rectangle about
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # Fills the window with the background colour
    window.fill(BACKGROUND_COLOUR)

    # Draws the example rectangle
    pygame.draw.rect(window, (255, 0, 0), (x, y, width, height))
    exampleRectangle.draw(window)

    # Draw heatmap
    for x in range(0, N_CELLS):
        for y in range(0, N_CELLS):
            pygame.draw.rect(temperature_surface,
                             (temperature_map[x, y] * 255, 0, 0),
                             (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    # Propagate heat
    new_temperature_map = temperature_map
    new_temperature_map[1:, :] = ((new_temperature_map[1:, :] * HEAT_SLOWNESS) + new_temperature_map[:-1, :]) / (
                HEAT_SLOWNESS + 1)
    new_temperature_map[:-1, :] = ((new_temperature_map[:-1, :] * HEAT_SLOWNESS) + new_temperature_map[1:, :]) / (
                HEAT_SLOWNESS + 1)
    new_temperature_map[:, 1:] = ((new_temperature_map[:, 1:] * HEAT_SLOWNESS) + new_temperature_map[:, :-1]) / (
                HEAT_SLOWNESS + 1)
    new_temperature_map[:, :-1] = ((new_temperature_map[:, :-1] * HEAT_SLOWNESS) + new_temperature_map[:, 1:]) / (
                HEAT_SLOWNESS + 1)

    # Add the heatmap to the visible surface
    window.blit(temperature_surface, (0, 0))

    # Sends update to the actual window
    pygame.display.update()

pygame.quit()
