import pygame
import sys
import math
import random
from collections import deque
from Procedural_Tree_Generation import perlin_noise
from datetime import datetime
import time

class Window:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))

    def fill(self):
        self.screen.fill((0, 0, 0))


def image_to_grid(x, y, cell_size):
    # Converts a physical coordinate on the screen into a grid coordinate
    grid_x = int(x / cell_size)
    grid_y = int(y / cell_size)
    return grid_x, grid_y


def generate_random_point_around(x, y, min_dist):
    # Generates a random point relative to the annulus of another point
    # The region of the annulus has a radius from "min_dist" to "min_dist x 2"
    v1 = random.randrange(1000) / 1000  # A little trick to get range between 0 - 1 in decimals (In this case, given to 3 decimals)
    v2 = random.randrange(1000) / 1000  # A little trick to get range between 0 - 1 in decimals (In this case, given to 3 decimals)

    radius = min_dist * (1 + v1)  # Radius is between 1 - 2 times of "min_dist"
    angle = 2 * 3.1415926535 * v2  # Random angle (0 - 2pi radians)

    # Trig to solve for new point
    new_x = x + math.cos(angle) * radius
    new_y = y + math.sin(angle) * radius

    return new_x, new_y


def in_neighborhood(x, y, min_dist, grid, cell_size):

    grid_x, grid_y = image_to_grid(x, y, cell_size)
    for ny in range(grid_y - 2, grid_y + 2 + 1):
        for nx in range(grid_x - 2, grid_x + 2 + 1):
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):  # Border check (Using grid index format)
                if len(grid[ny][nx]) > 0:  # Check to make sure there is/are neighbor(s) here
                    for coord_nx, coord_ny in grid[ny][nx]:
                        dist = math.sqrt((x - coord_nx) ** 2 + (y - coord_ny) ** 2)  # Calculate distance to neighbor
                        if dist < min_dist:
                            return True  # at least 1 too close neighbor

    return False  # no too close neighbor(s)


def convert_range(high, low, num):
    # Converts range into 0 - 1
    # Used ratios and sorta a property of similar triangles
    range = high - low
    return (num - low) / range


def generate_poisson(point_gen_cnt, min_radius, max_radius, perlin_noise):
    # Note that "perlin noise" is technically the screen itself

    cell_size = max_radius
    process_li = []
    sample_points = deque()
    # The relationship between "grid" and "perlin_noise" is that "perlin_noise" is a coordinate system
    # while "grid" is a grid used to split up "perlin_noise" into chunks
    grid_w = int(len(perlin_noise[0])/cell_size + 0.9999999)  # Convert into grid index format
    grid_h = int(len(perlin_noise)/cell_size + 0.9999999)  # Convert into grid index format
    grid = [[[] for i in range(grid_w)] for i in range(grid_h)]  # It should be noted that we can store several points and not just one in a single chunk

    # Generate random point onscreen
    x, y = random.randrange(len(perlin_noise[0])), random.randrange(len(perlin_noise))
    sample_points.append((x, y))
    process_li.append((x, y))
    grid_x, grid_y = image_to_grid(x, y, cell_size)
    grid[grid_y][grid_x].append((x, y))

    while process_li:
        x, y = process_li.pop()
        min_dist = min_radius + convert_range(0.8 ** 2, 0.2 ** 2, (1 - perlin_noise[int(y)][int(x)]) ** 2) * (max_radius - min_radius)  # The raise to power of 2 is used to create more polarity
        for i in range(point_gen_cnt):
            new_x, new_y = generate_random_point_around(x, y, min_dist)
            if 0 <= new_x <= len(perlin_noise[0]) and 0 <= new_y <= len(perlin_noise):  # Check to see if its within the borders
                if in_neighborhood(new_x, new_y, min_dist, grid, cell_size) == False:  # Check to see if no neighbors are too close
                    process_li.append((new_x, new_y))
                    sample_points.append((new_x, new_y))
                    # Convert the new coordinate into grid format and add it into the grid
                    grid_x, grid_y = image_to_grid(new_x, new_y, cell_size)
                    grid[grid_y][grid_x].append((new_x, new_y))

    return sample_points


startTime = datetime.now()  # RECORDING SOFTWARE FOR CHECKING RUNTIME
screen = Window(700, 525)
pygame.init()
clock = pygame.time.Clock()
points = generate_poisson(20, 3, 20, perlin_noise)

screen.fill()
for x, y in points:
    pygame.draw.rect(screen.screen, (255, 255, 255), (int(x), int(y), 2, 2))
pygame.display.update()

print(datetime.now() - startTime)  # Print Runtime

while True:

    # Check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    clock.tick(70)  # Fps (Don't know why/how it does it)