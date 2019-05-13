import numpy as np
import pygame


class HeatMap:

    def __init__(self, n_cells, cell_width, cell_height, heat_slowness):
        self.n_cells = n_cells
        self.temperature_map = np.random.rand(n_cells, n_cells)
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.heat_slowness = heat_slowness

    def draw(self, surface):
        for x in range(0, self.n_cells):
            for y in range(0, self.n_cells):
                pygame.draw.rect(surface,
                                 (self.temperature_map[x, y] * 255, 0, 0),
                                 (x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height))

    def step(self):
        # Propagate heat
        new_temperature_map = self.temperature_map.copy() * self.heat_slowness
        new_temperature_map[1:, :] += self.temperature_map[:-1, :]
        new_temperature_map[:-1, :] += self.temperature_map[1:, :]
        new_temperature_map[:, 1:] += self.temperature_map[:, :-1]
        new_temperature_map[:, :-1] += self.temperature_map[:, 1:]
        new_temperature_map /= self.heat_slowness + 4
        self.temperature_map = new_temperature_map
