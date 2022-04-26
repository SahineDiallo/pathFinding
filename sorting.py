from platform import node
import pygame

#Colors
WHITE = (245, 246, 247)
RED = (237, 24, 59)
BLACK = (23, 23, 23)
ORANGE = (247, 55, 7)
BLUE  = (15, 26, 247)
GREEN = (96, 204, 96)
PURPLE = (131, 46, 191)
YELLOW = (230, 172, 14)
BEIGE = (235, 148, 101)

states_dict = {'start': YELLOW, 'end': BEIGE, 'closed': RED, 'open': GREEN, 'barrier': BLACK, 'path': PURPLE}

#Set the pygame initials
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm Visualization")

class Node():
    def __init__(self, row, col, width, total_rows):
        self.x = row * width
        self.y = col * width
        self.total_rows = total_rows
        self.neighbors = []
        self.width = width
        self.color = WHITE

    def is_state(self, state):
        return self.color == states_dict[state]

    def make_state(self, state):
        self.color = states_dict[state]

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width), border_radius=1)

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False

def heuristic(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1 - x2) + abs(y1 + y2)



