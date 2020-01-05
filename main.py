# - Profilen und dann die Geschwindigkeit verbessern. Ich will
#   800 * 800 Zellen @ 60 FPS. Letzter Stand (ohne Nachbarn zu plotten):
#   rund 44 FPS. Achtung: beim Testen die UPS nicht begrenzen!
# - schnelles addieren ohne neues array zu erzeugen: np.add(a, b, out=a),
#   zumindest laut dem surfarray Tutorial. Hilft das? Scheint nicht so.


import pygame as pg
import numpy as np
import math


RULES = {
    "birth": (3,),
    "survive": (2, 3)
}
WORLD_SIZE = (800, 800)
WINDOW_SIZE = (800, 800)
FPS = 60
show_neighbors = True

pg.init()
window = pg.display.set_mode(WINDOW_SIZE)
clock = pg.time.Clock()
small_surf = pg.Surface(WORLD_SIZE)
world_display = np.zeros(WORLD_SIZE, int)
neighbors = np.zeros(WORLD_SIZE, int)

# glider:
# world[3, 6] = 1
# world[4, 6] = 1
# world[5, 6] = 1
# world[5, 5] = 1
# world[4, 4] = 1

world = np.random.choice([False, True], WORLD_SIZE, p=[0.9, 0.1])

# Using a 2d surfarray is faster than a 3d surfarray. This, however, means that
# the colors have to be converted to integers:
COLORS = {
    "rainbow": [
        int("{0:02x}{1:02x}{2:02x}".format(0, 0, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(170, 0, 255), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 0, 255), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 170, 255), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 255, 170), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 255, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(170, 255, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(255, 170, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(255, 0, 0), 16)
    ],
    "bw": [
        int("{0:02x}{1:02x}{2:02x}".format(0, 0, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(255, 255, 255), 16)
    ]
}

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
        np.logical_and(
            np.logical_not(world),
            np.isin(neighbors, RULES["birth"])),
        np.logical_and(
            world,
            np.isin(neighbors, RULES["survive"])
        )
    )

    if show_neighbors:
        for i in range(9):
            # FIXME: Geht das auch schneller?
            world_display[neighbors == i] = COLORS["rainbow"][i]
    else:
        world_display[world] = COLORS["bw"][1]
        world_display[np.logical_not(world)] = COLORS["bw"][0]

    pg.surfarray.blit_array(small_surf, world_display)
    pg.transform.scale(small_surf, WINDOW_SIZE, window)
    pg.display.flip()
