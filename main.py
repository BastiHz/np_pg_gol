# - Profilen und dann die Geschwindigkeit verbessern. Ich will
#   800 * 800 Zellen @ 60 FPS. Letzter Stand (ohne Nachbarn zu plotten):
#   rund 44 FPS
# - schnelles addieren ohne neues array zu erzeugen: np.add(a, b, out=a),
#   zumindest laut dem surfarray Tutorial. Hilft das? Scheint nicht so.
# - Geschwindigkeitstest machen. Ist das schneller als pg.draw.rect() oder
#   blitten von vorbereiteten quadratischen Surfaces?
# Erkenntnis: Ein 2d-surfarray läuft viel schneller als ein 3d.


# Regeln aus Wikipedia
# Any live cell with two or three neighbors survives.
# Any dead cell with three live neighbors becomes a live cell.
# All other live cells die in the next generation. Similarly, all other dead cells stay dead.


import pygame as pg
import numpy as np

WORLD_WIDTH = 400
WORLD_HEIGHT = 400
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SHOW_NEIGHBORS = True

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

if SHOW_NEIGHBORS:
    COLORS = [
        int("{0:02x}{1:02x}{2:02x}".format(0, 0, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(170, 0, 255), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 0, 255), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 170, 255), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 255, 170), 16),
        int("{0:02x}{1:02x}{2:02x}".format(0, 255, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(170, 255, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(255, 170, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(255, 0, 0), 16)
    ]
else:
    COLORS = [
        int("{0:02x}{1:02x}{2:02x}".format(0, 0, 0), 16),
        int("{0:02x}{1:02x}{2:02x}".format(255, 255, 255), 16)
    ]

running = True
while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_f:
                print(clock.get_fps())

    big_world[1:-1, 1:-1] = visible_world
    big_world[0, 1:-1] = visible_world[-1, :]
    big_world[-1, 1:-1] = visible_world[0, :]
    big_world[:, 0] = big_world[:, -2]
    big_world[:, -1] = big_world[:, 1]

    # TODO: kann ich das Zählen der Nachbarn schneller machen?
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
    temp_world[np.logical_and(big_world == 0, neighbors == 3)] = 1
    temp_world[np.logical_and(big_world == 1, np.logical_or(neighbors == 2, neighbors == 3))] = 1
    visible_world[...] = temp_world[1:-1, 1:-1]

    if SHOW_NEIGHBORS:
        visible_neighbors[...] = neighbors[1:-1, 1:-1]
        # FIXME: Geht das auch schneller?
        for i in range(9):
            world_display[visible_neighbors == i] = COLORS[i]
    else:
        for i in range(2):
            world_display[visible_world == i] = COLORS[i]

    pg.surfarray.blit_array(small_surf, world_display)
    pg.transform.scale(small_surf, [WINDOW_WIDTH, WINDOW_HEIGHT], window)

    pg.display.flip()
