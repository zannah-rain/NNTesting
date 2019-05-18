import numpy as np
import pygame


class HeatMap:

    def __init__(self, n_cells, cell_width, cell_height, heat_slowness):
        self.n_cells = n_cells
        self.temperature_map = np.zeros((n_cells, n_cells))
        for i in range(n_cells):
            for j in range(n_cells):
                self.temperature_map[i, j] = (abs(i - n_cells/2) + abs(j - n_cells/2)) ** 2
        self.temperature_map = (self.temperature_map.max() - self.temperature_map) / self.temperature_map.max()
        # self.temperature_map += np.random.rand(n_cells, n_cells)
        self.temperature_map = self.temperature_map / self.temperature_map.max()
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

    def transform_coordinates(self, x, y):
        return int(x / self.cell_width), int(y / self.cell_height)

    def get_temperature(self, x, y):
        x2, y2 = self.transform_coordinates(x, y)
        return self.temperature_map[x2, y2]

    def get_temperature_area(self, x, y, width, height):
        x2, y2 = self.transform_coordinates(x, y)

        # Might be missing some rows / columns if near the edge of the map
        basic_area = self.temperature_map[x2 - width:x2 + width + 1, y2 - height:y2 + height + 1]

        # Pad off the map areas with 0s
        # if x < width:
        #    basic_area = np.concatenate((np.zeros((height * 2 + 1, 1)), basic_area), axis=1)
        # if y < height:
        #    basic_area = np.concatenate((np.zeros((1, width * 2 + 1)), basic_area), axis=1)
        return basic_area
