import pygame
import sys
import math
import random
from collections import deque


class Window:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))

    def fill(self):
        self.screen.fill((255, 255, 255))


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


def in_neighborhood(grid, x, y, cell_size, min_dist):
    # This function checks to see if a new point has any neighbors which are too close
    # We check 24 neighbors  (25 in total) to do this
    # Why we check within a 5 x 5 radius is some what hard to explain
    # Due to the nature of how the "cell_size" is related to the "min_dist", we could visualize a solution
    # We would test worst case by drawing circles on the vertexes of the new point's cell
    grid_x, grid_y = image_to_grid(x, y, cell_size)
    for ny in range(grid_y - 2, grid_y + 2 + 1):
        for nx in range(grid_x - 2, grid_x + 2 + 1):
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):  # Border check
                if grid[ny][nx] != "":  # Check to see if there is a neighbor here
                    neighbor_x, neighbor_y = grid[ny][nx]
                    dist = math.sqrt((neighbor_x - x) ** 2 + (neighbor_y - y) ** 2)
                    if dist < min_dist:
                        return True  # at least 1 neighbor is too close

    return False  # no too close neighbor(s)


def generate_poisson(screen_w, screen_h, min_dist, point_gen_cnt):
    cell_size = min_dist / math.sqrt(2)

    grid_w = int(screen_w/cell_size + 0.9999999)
    grid_h = int(screen_h/cell_size + 0.9999999)
    grid = [["" for i in range(grid_w)] for i in range(grid_h)]

    process_li = deque()
    sample_points = deque()

    x, y = random.randrange(screen_w), random.randrange(screen_h)
    grid_x, grid_y = image_to_grid(x, y, cell_size)
    grid[grid_y][grid_x] = (x, y)
    sample_points.append((x, y))
    process_li.append((x, y))

    while process_li:
        x, y = process_li.popleft()
        for i in range(point_gen_cnt):
            new_x, new_y = generate_random_point_around(x, y, min_dist)
            if 0 <= new_x <= screen_w and 0 <= new_y <= screen_h:
                if in_neighborhood(grid, new_x, new_y, cell_size, min_dist) == False:
                    process_li.append((new_x, new_y))
                    sample_points.append((new_x, new_y))
                    grid_x, grid_y = image_to_grid(new_x, new_y, cell_size)
                    grid[grid_y][grid_x] = (new_x, new_y)

    return sample_points



screen = Window(700, 525)
pygame.init()
clock = pygame.time.Clock()

points = generate_poisson(screen.w, screen.h, 60, 30)

screen.fill()
for x, y in points:
    # pygame.draw.rect(screen.screen, (0,0,0), (x, y, 5, 5))
    pygame.draw.circle(screen.screen, (0,0,0), (int(x), int(y)), 10)
pygame.display.update()

while True:

    # Check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    clock.tick(70)  # Fps (Don't know why/how it does it)