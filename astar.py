import pygame
import argparse
import math
import time
import colors
import os
from PIL import Image
from queue import PriorityQueue

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
MAPS_DIR = "maps"
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
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Cardinal directions
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
        ]
        for drow, dcol in directions:
            new_row, new_col = self.row + drow, self.col + dcol
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows:
                if abs(drow) + abs(dcol) == 2:  # Diagonal movement
                    if not grid[new_row][new_col].is_barrier() and not (grid[self.row][new_col].is_barrier() or grid[new_row][self.col].is_barrier()):
                        self.neighbors.append(grid[new_row][new_col])
                else:
                    if not grid[new_row][new_col].is_barrier():
                        self.neighbors.append(grid[new_row][new_col])

    def __lt__(self, other):
        return False
    
def h(n1, n2, heuristic):
    x1, y1 = n1
    x2, y2 = n2
    dx, dy = abs(x1 - x2), abs(y1 - y2)

    if heuristic.lower() == "manhattan":
        return dx + dy
    elif heuristic.lower() == "euclidean":
        return math.sqrt(dx ** 2 + dy ** 2)
    elif heuristic.lower() == "octile":
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()

def algorithm(draw, grid, start_pos, end_pos, heurisitc):
    start_time = time.time() # Start timer
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
            end_time = time.time()
            print(f"Path successfully found. Algorithm execution time: {end_time - start_time:.4f} seconds")
            return True
        
        for neighbor in current.neighbors:
            # Determine g_score based on cardinal/diagonal
            temp_g_score = g_score[current] + (1 if abs(neighbor.row - current.row) + abs(neighbor.col - current.col) == 1 else math.sqrt(2))

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

    end_time = time.time()
    print(f"Unable to find a path. Algorithm execution time: {end_time - start_time:.4f} seconds")
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
    parser.add_argument("heuristic", type=str, choices=["manhattan", "euclidean", "octile"], help="Choose the heuristic function.")
    parser.add_argument("--size", type=int, default=50, help="Grid size. Grid is square, so 'size' value will apply to height AND width of the grid.")
    parser.add_argument("--use_map", type=str, help="Choose an image to use for a predefined map. Image dimensions required to match grid size. Overrides --size.")
    args = parser.parse_args()

    start_pos = None
    end_pos = None
    run = True

    # Open a map file and set the grid size
    if args.use_map:
        map_path = os.path.join(MAPS_DIR, args.use_map) 
        if not os.path.exists(map_path):
            print(f"ERR: Could not find the map image at: {args.use_map}")
            quit()
        map_img = Image.open(map_path)
        args.size = map_img.width

    grid = make_grid(args.size, width)

    # Set the grid using the specified map data.
    if args.use_map:
        map_pixels = Image.open(map_path).load()
        for y in range(map_img.height):
            for x in range(map_img.width):
                if map_pixels[x,y] == colors.BLACK:
                    grid[x][y].set_barrier()

    while run:
        draw(WIN, grid, args.size, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # If LMB pressed
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, args.size, width)
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
                row, col = get_clicked_pos(pos, args.size, width)
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
                    algorithm(lambda: draw(win, grid, args.size, width), grid, start_pos, end_pos, args.heuristic) 

                if event.key == pygame.K_c:
                    start_pos = None
                    end_pos = None
                    grid = make_grid(args.size, width)

    pygame.quit()

main(WIN, WIDTH)