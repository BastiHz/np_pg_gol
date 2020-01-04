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
WORLD_WIDTH = 400
WORLD_HEIGHT = 400
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 60
show_neighbors = True

pg.init()
window = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pg.time.Clock()
small_surf = pg.Surface([WORLD_WIDTH, WORLD_HEIGHT])
visible_world = np.zeros([WORLD_WIDTH, WORLD_HEIGHT], int)
big_world = np.zeros([WORLD_WIDTH + 2, WORLD_HEIGHT + 2], int)
temp_world = np.zeros(big_world.shape, int)
world_display = np.zeros([WORLD_WIDTH, WORLD_HEIGHT], int)
neighbors = np.zeros(big_world.shape, int)
visible_neighbors = np.zeros(visible_world.shape, int)

# glider:
# visible_world[3, 6] = 1
# visible_world[4, 6] = 1
# visible_world[5, 6] = 1
# visible_world[5, 5] = 1
# visible_world[4, 4] = 1

visible_world = np.random.choice([0, 1], visible_world.shape, p=[0.9, 0.1])

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
ups = 20
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

    big_world[1:-1, 1:-1] = visible_world
    big_world[0, 1:-1] = visible_world[-1, :]
    big_world[-1, 1:-1] = visible_world[0, :]
    big_world[:, 0] = big_world[:, -2]
    big_world[:, -1] = big_world[:, 1]

    # TODO: kann ich das Zählen der Nachbarn schneller machen?
    # Kann ich vieleicht darauf verzichten alles auf eine größere Welt zu
    # kopiere, indem ich da mit dem Zählen der Nachbarn schlauer mache? Ich
    # müsste die vier Ecken und die Ränder speziell behandeln, aber das dürfte
    # schneller ein, als immer die ganze Welt hin und her zu kopieren.
    # Teste die Geschwindigkeit! Benchmarke und Profile! Möglichst
    # reproduzierbar mit seed, ohne plotten, mit fester Anzahl an Updates.
    # Stelle sicher, dass das Ergebnis richtig ist. Am besten einmal das
    # richtige Ergebnisarray als Datei ablegen und dann die neuen Versionen
    # damit vergleichen.
    neighbors[...] = 0
    neighbors[:-1, :] += big_world[1:, :]
    neighbors[1:, :] += big_world[:-1, :]
    neighbors[:, :-1] += big_world[:, 1:]
    neighbors[:, 1:] += big_world[:, :-1]
    neighbors[1:, 1:] += big_world[:-1, :-1]
    neighbors[:-1, :-1] += big_world[1:, 1:]
    neighbors[1:, :-1] += big_world[:-1, 1:]
    neighbors[:-1, 1:] += big_world[1:, :-1]

    temp_world[...] = 0
    mask = np.logical_or(
        np.logical_and(big_world == 0, np.isin(neighbors, RULES["birth"])),
        np.logical_and(big_world == 1, np.isin(neighbors, RULES["survive"]))
    )
    temp_world[mask] = 1
    visible_world[...] = temp_world[1:-1, 1:-1]

    if show_neighbors:
        visible_neighbors[...] = neighbors[1:-1, 1:-1]
        for i in range(9):
            # FIXME: Geht das auch schneller?
            world_display[visible_neighbors == i] = COLORS["rainbow"][i]
    else:
        for i in range(2):
            world_display[visible_world == i] = COLORS["bw"][i]

    pg.surfarray.blit_array(small_surf, world_display)
    pg.transform.scale(small_surf, [WINDOW_WIDTH, WINDOW_HEIGHT], window)
    pg.display.flip()
