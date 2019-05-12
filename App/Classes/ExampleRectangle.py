import pygame


class ExampleRectangle:

    # Constructor / initialisation code for this instance
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = (255, 0, 0)

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))
