import pygame
import argparse
import math
import colors
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
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbors.append(grid[self.row][self.col - 1 ])

    def __lt__(self, other):
        return False
    
def h(n1, n2, heuristic):
    x1, y1 = n1
    x2, y2 = n2

    if heuristic.lower() == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    elif heuristic.lower() == "euclidean":
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()

def algorithm(draw, grid, start_pos, end_pos, heurisitc):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_pos)) # Start with the start node in the open set
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row} # Keeps track of the current shortest distance from start node to this node
    g_score[start_pos] = 0
    f_score = {node: float("inf") for row in grid for node in row} # Keeps track of the predicted distance from this node to the end node
    f_score[start_pos] = h(start_pos.get_pos(), end_pos.get_pos(), heurisitc)

    open_set_hash = {start_pos}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end_pos:
            reconstruct_path(came_from, end_pos, draw)
            end_pos.set_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end_pos.get_pos(), heurisitc)

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
        draw()

        if current != start_pos:
            current.set_closed()

    return False

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
    parser = argparse.ArgumentParser()
    parser.add_argument("heuristic", choices=["manhattan", "euclidean"], help="Choose the heuristic function.")
    args = parser.parse_args()

    ROWS = 50
    grid = make_grid(ROWS, width)

    start_pos = None
    end_pos = None
    run = True

    while run:
        draw(WIN, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_pos and end_pos:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start_pos, end_pos, args.heuristic) 

                if event.key == pygame.K_c:
                    start_pos = None
                    end_pos = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)