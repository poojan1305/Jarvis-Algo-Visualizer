import pygame
import math
from queue import PriorityQueue
import sys

WIDTH = 500

#setting up the display window
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algo")

RED = (255, 0 ,0)
GREEN  = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#this class is created to know color of each spot and 
#their respective distances
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    #some functions to know status of each node
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE            

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE    

    #these methods will actually change the colors
    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED    

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    #to draw window on the screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        #down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col ].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        #up
        if self.row > 0 and not grid[self.row - 1][self.col ].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        #right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])
        #left
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

    #to compare 2 nodes
    def __lt__(self, other):
        return False                       

#heuristic function 
#finding manhattan distance
#basically an 'L' shape between start and end points
#this is because we cannot go diagonally
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw() 

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()  #to get the minimum element
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  
        open_set_hash.remove(current)

        #to make final path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current 
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + heuristic(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open() 

        draw()

        if current != start:
            current.make_closed()  

    return False                   

#this basically is to store each node 
def make_grid(rows, width):
    grid = []
    gap = width // rows   #integer division gives the width of each node

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i , j ,gap, rows)
            grid[i].append(node)

    return grid

#to draw grid lines
def draw_grid(win, rows, width):
    gap = width // rows

    #we are drawing lines so that there is a differnece between 
    #each node 
    #we shift through x axis and continously draw lines 
    #along y_axis
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    #fills the frame with WHITE color 
    #we do this everytime we create a frame
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

#this function converts mouse position into 
# row and column format for calculation purpose
            
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

flag = 0
def closing():
    flag = 1
    print("flag is now 1")

def astar_main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            
            #when we left click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()


            #when we right click
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end == None    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    print(flag)
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start,end)  
                    run = False      

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)           


    return
    #pygame.quit()   

#astar_main(WIN, WIDTH)                 

