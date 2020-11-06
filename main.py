import pygame as pg
import numpy as np
import math


RULES = {
    "birth": (3,),
    "survive": (2, 3)
}
WORLD_SIZE = (400, 400)
WINDOW_SIZE = (800, 800)
FPS = 60
show_neighbors = False

pg.init()
window = pg.display.set_mode(WINDOW_SIZE)
clock = pg.time.Clock()
small_surf = pg.Surface(WORLD_SIZE)
world_display = np.zeros(WORLD_SIZE, int)
neighbors = np.zeros(WORLD_SIZE, int)

# all random
# world = np.random.choice([False, True], WORLD_SIZE, p=[0.8, 0.2])

# central hole
world = np.random.choice([False, True], WORLD_SIZE, p=[0.4, 0.6])
world[50:350, 50:350] = False

# glider:
# world = np.zeros(WORLD_SIZE, bool)
# world[3, 6] = 1
# world[4, 6] = 1
# world[5, 6] = 1
# world[5, 5] = 1
# world[4, 4] = 1

# Using a 2d surfarray is faster than a 3d surfarray. This, however, means that
# the colors have to be converted to integers.


def rgb_to_int(r, g, b):
    # There seems to be a bug in the __int__() method of pygame.Color objects.
    # So until that is fixed I do the conversion manually.
    return (r << 16) + (g << 8) + b


COLORS_NEIGHBORS = [
    rgb_to_int(0, 0, 0),
    rgb_to_int(170, 0, 255),
    rgb_to_int(0, 0, 255),
    rgb_to_int(0, 170, 255),
    rgb_to_int(0, 255, 170),
    rgb_to_int(0, 255, 0),
    rgb_to_int(170, 255, 0),
    rgb_to_int(255, 170, 0),
    rgb_to_int(255, 0, 0)
]
COLORS_DEAD_ALIVE = [
    rgb_to_int(0, 0, 0),
    rgb_to_int(255, 255, 255)
]

running = True
ups = 60
time_per_update = 1 / ups * 1000  # milliseconds
time_since_last_update = 0
while running:
    dt = clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_f:
                print(clock.get_fps())
            elif event.key == pg.K_s:
                show_neighbors = not show_neighbors
            elif event.key == pg.K_UP:
                ups = min(ups + 10, FPS)
                time_per_update = 1 / ups * 1000
            elif event.key == pg.K_DOWN:
                ups = max(ups - 10, 0)
                if ups > 0:
                    time_per_update = 1 / ups * 1000
                else:
                    time_per_update = math.inf

    if ups > 0:
        time_since_last_update += dt
    if time_since_last_update < time_per_update:
        continue
    time_since_last_update -= time_per_update

    neighbors[...] = 0
    # W:
    neighbors[:, :-1] += world[:, 1:]
    neighbors[:, -1] += world[:, 0]
    # E:
    neighbors[:, 1:] += world[:, :-1]
    neighbors[:, 0] += world[:, -1]
    # S:
    neighbors[:-1, :] += world[1:, :]
    neighbors[-1, :] += world[0, :]
    # N:
    neighbors[1:, :] += world[:-1, :]
    neighbors[0, :] += world[-1, :]
    # SW:
    neighbors[:-1, :-1] += world[1:, 1:]
    neighbors[-1, :-1] += world[0, 1:]
    neighbors[:-1, -1] += world[1:, 0]
    neighbors[-1, -1] += world[0, 0]
    # NE:
    neighbors[1:, 1:] += world[:-1, :-1]
    neighbors[0, 1:] += world[-1, :-1]
    neighbors[1:, 0] += world[:-1, -1]
    neighbors[0, 0] += world[-1, -1]
    # SE:
    neighbors[:-1, 1:] += world[1:, :-1]
    neighbors[-1, 1:] += world[0, :-1]
    neighbors[:-1, 0] += world[1:, -1]
    neighbors[-1, 0] += world[0, -1]
    # NW:
    neighbors[1:, :-1] += world[:-1, 1:]
    neighbors[0, :-1] += world[-1, 1:]
    neighbors[1:, -1] += world[:-1, 0]
    neighbors[0, -1] += world[-1, 0]

    world[...] = np.logical_or(
        np.isin(neighbors, RULES["birth"]),
        np.logical_and(
            world,
            np.isin(neighbors, RULES["survive"])
        )
    )

    if show_neighbors:
        for n in range(9):
            # FIXME: Geht das auch schneller?
            world_display[neighbors == n] = COLORS_NEIGHBORS[n]
    else:
        world_display[world] = COLORS_DEAD_ALIVE[1]
        world_display[np.logical_not(world)] = COLORS_DEAD_ALIVE[0]

    pg.surfarray.blit_array(small_surf, world_display)
    pg.transform.scale(small_surf, WINDOW_SIZE, window)
    pg.display.flip()
