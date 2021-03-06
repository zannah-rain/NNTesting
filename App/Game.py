import pygame
import tensorflow as tf
from App.Classes.ExampleRectangle import ExampleRectangle
from App.Classes.HeatMap import HeatMap
from App.Classes.Agent import Agent

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
heatMap = HeatMap(N_CELLS, CELL_WIDTH, CELL_HEIGHT, HEAT_SLOWNESS)

# A target surface to draw temp related stuff to
temperature_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
temperature_surface.set_alpha(64)  # Up to 128

with tf.Session() as sess:
    # Instantiate some example Agents
    agentList = []
    for i in range(10):
        agentList.append(Agent(50, 50, sess, heatMap))
    for i in range(10):
        agentList.append(Agent(50,
                               50,
                               sess,
                               heatMap,
                               colour=(0, 0, 255),
                               output_activation=tf.nn.relu,
                               rotation_sampling=True))

    step = 0

    # Keep running until user clicks the exit button
    running = True
    while running:
        step += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Update the example rectangle
        exampleRectangle.step(keys)

        for i in agentList:
            i.step()

        # Fills the window with the background colour
        window.fill(BACKGROUND_COLOUR)

        # Draws the example rectangle
        exampleRectangle.draw(window)

        for i in agentList:
            i.draw(window)

        # Draw heatmap
        heatMap.draw(temperature_surface)

        # Propagate heat
        if step < 50:
            heatMap.step()

        # Add the heatmap to the visible surface
        window.blit(temperature_surface, (0, 0))

        # Sends update to the actual window
        pygame.display.update()

pygame.quit()
