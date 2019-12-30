import numpy as np

# big_world = np.zeros([9, 9], int)
# world = np.zeros([7, 7], int)
# new_world = np.zeros(big_world.shape, int)
# neighbors = np.zeros(big_world.shape, int)
#
# world[2, 4] = 1
# world[3, 4] = 1
# world[4, 4] = 1
# world[4, 3] = 1
# world[3, 2] = 1
#
# # world[0, 3] = 1
#
# while True:
#     big_world[1:-1, 1:-1] = world
#     big_world[0, 1:-1] = world[-1, :]
#     big_world[-1, 1:-1] = world[0, :]
#     big_world[:, 0] = big_world[:, -1]
#     big_world[:, -1] = big_world[:, 0]
#
#     neighbors[...] = 0
#     neighbors[:-1, :] += big_world[1:, :]
#     neighbors[1:, :] += big_world[:-1, :]
#     neighbors[:, :-1] += big_world[:, 1:]
#     neighbors[:, 1:] += big_world[:, :-1]
#
#     neighbors[1:, 1:] += big_world[:-1, :-1]
#     neighbors[:-1, :-1] += big_world[1:, 1:]
#     neighbors[1:, :-1] += big_world[:-1, 1:]
#     neighbors[:-1, 1:] += big_world[1:, :-1]
#
#     print(big_world)
#     print(neighbors)
#
#     new_world[...] = 0
#     new_world[np.logical_and(big_world == 0, neighbors == 3)] = 1
#     new_world[np.logical_and(big_world == 1, np.logical_or(neighbors == 2, neighbors == 3))] = 1
#     world[...] = new_world[1:-1, 1:-1]
#     print(world)
#
#     input(">>>")

big_world = np.zeros([5, 5], int)
world = np.zeros([3, 3], int)
world[0, 0] = 1
world[0, -1] = 2
world[-1, 0] = 3
world[-1, -1] = 4
print(world)

big_world[1:-1, 1:-1] = world
big_world[0, 1:-1] = world[-1, :]
big_world[-1, 1:-1] = world[0, :]
big_world[:, 0] = big_world[:, -2]
big_world[:, -1] = big_world[:, 1]
print(big_world)