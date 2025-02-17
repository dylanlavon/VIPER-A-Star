import pygame
import colors
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = colors.WHITE
        self.neighbors = []
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == colors.RED
    
    def is_open(self):
        return self.color == colors.GREEN
    
    def is_barrier(self):
        return self.color == colors.BLACK
    
    def is_start(self):
        return self.color == colors.ORANGE
    
    def is_end(self):
        return self.color == colors.TURQUOISE
    
    def reset(self):
        self.color = colors.WHITE

    def set_closed(self):
        self.color = colors.RED

    def set_open(self):
        self.color = colors.GREEN
    
    def set_barrier(self):
        self.color = colors.BLACK

    def set_start(self):
        self.color = colors.ORANGE
    
    def set_end(self):
        self.color = colors.TURQUOISE

    def set_path(self):
        self.color = colors.PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False
    
# Using Manhattan Distance
def h(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_gridlines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, colors.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, colors.GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(colors.WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_gridlines(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start_pos = None
    end_pos = None
    run = True
    started = False

    while run:
        draw(WIN, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started: continue

            # If LMB pressed
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start_pos and node != end_pos:
                    start_pos = node
                    start_pos.set_start()
                elif not end_pos and node != start_pos:
                    end_pos = node
                    end_pos.set_end()
                elif node != start_pos and node != end_pos:
                    node.set_barrier()

            # If RMB pressed
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start_pos:
                    start_pos = None
                if node == end_pos:
                    end_pos = None

    pygame.quit()

main(WIN, WIDTH)