
import pygame
from queue import PriorityQueue
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
GREY = (200, 204, 200)

states_dict = {'start': YELLOW, 'end': BLUE, 'closed': RED, 'open': GREEN, 'barrier': BLACK, 'path': PURPLE}

#Set the pygame initials
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm Visualization")

class Node():
    def __init__(self, row, col, width, total_rows):
        self.x = row * width
        self.y = col * width
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.neighbors = []
        self.width = width
        self.color = WHITE

    def is_state(self, state):
        return self.color == states_dict[state]

    def make_state(self, state):
        self.color = states_dict[state]

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width), border_radius=1)

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_state('barrier'):
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_state('barrier'):
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_state('barrier'):
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_state('barrier'):
            self.neighbors.append(grid[self.row][self.col + 1])



    def __lt__(self, other):
        return False

def heuristic(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    gap = width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            n = Node(i, j, gap, rows)
            grid[i].append(n)

    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for i in range(rows):
            pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, width))

def draw_path(draw, current, came_from, end, start):
    while current in came_from:
        current = came_from[current]
        if current != end and current != start:
            current.make_state('path')
        draw()

def algorithm(draw, grid, start, end):
    count = 0 #this will hellp check wich node is put first
    open_set = PriorityQueue()
    came_from = {}
    open_set.put((0, count, start))

    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            #draw the path
            draw_path(draw, end, came_from, end, start)
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = heuristic(neighbor.get_pos(), end.get_pos()) + temp_g_score

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_state('open')

        draw()
        if current != start:
            current.make_state('closed')

    return False
        


def draw(win, grid, width, rows):
    #fill the window
    win.fill(WHITE)

    #draw the grid
    for row in grid:
        for node in row:
            node.draw(win)

    #draw the grid lines 
    draw_grid_lines(win, rows, width)

    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    start, end = None, None
    run = True
    started = False
    grid = make_grid(ROWS, width)

    while run:
        draw(win, grid, width, ROWS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and end != node:
                    start = node
                    node.make_state('start')

                elif not end and node != start:
                    end = node
                    node.make_state('end')

                elif node != start and end != node:
                    node.make_state('barrier')

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda:draw(win, grid, width, ROWS), grid, start, end)

                        
    pygame.quit()

main(WIN, WIDTH)

