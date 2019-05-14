import pygame

class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = (0, 255, 0)

    def step(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, 1, 1))
