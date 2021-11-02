# Welcome Kiddo To Our Little Cute Project

import pygame

WIDTH = 600

WINDOW = pygame.display.set_mode((WIDTH,WIDTH))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

START = GREEN
END = RED
BARRIER = BLACK
OPEN = WHITE

# def gridSetup (window, rows, width): 
#     grid = []
#     gap = width//rows
#     for i in range (rows):
#         grid.append([])
#         for j in range (rows):
#             node = 

class Tile:
    def init(self, column, row, width, totalCols, totalRows):
        self.col = column
        self.row = row
        self.x = width * column
        self.y = width * row
        self.width = width
        self.totalRows = totalRows
        self.totalCols = totalCols
        self.neighbours = []

    def getColour(self): 
       return self.colour

    def isStatus(self, status):
        return self.colour == status

    def reset(self):
	    self.color = OPEN

    def setStart(self):
	    self.color = START

    def setBarrier(self):
	    self.color = BARRIER

    def setEnd(self):
	    self.color = END

    def getNeighbours(self, grid):
        self.neighbours = []
        if self.col < self.totalRows -1 and not self.isStatus(END):
            self.neighbours.append(grid[self.col + 1][self.row])

        if self.col > 0 and not self.isStatus(BARRIER):
            self.neighbour.append(grid[self.col - 1][self.row])

        if self.row < self.totalRows -1 and not self.isStatus(END):
            self.neighbours.append(grid[self.col][self.row + 1])

        if self.row > 0 and not self.isStatus(BARRIER):
            self.neighbour.append(grid[self.col][self.row - 1])

    
# def AStar(grid):

def constructGrid(rows, cols, totalWidth):
    grid = []
    squareWidth = totalWidth // rows
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            grid[i].append(Tile(i, j, squareWidth, cols, rows))
    return grid

def drawGrid(window, totalWidth, rows, cols):
    gap = totalWidth/rows
    for i in range(rows):
        pygame.draw.line(window,GREY, (0, i * gap) ,(totalWidth, i * gap))

    for i in range(cols):
        pygame.draw.line(window,GREY, (i * gap, 0) ,(i * gap, totalWidth))

def drawTiles(window, grid):
    for rows in grid:
        for i in rows:
            pygame.draw.rect(window, i.colour, (i.x, i.y, i.width, i.width))

def draw(window, grid, totalWidth, cols, rols):
    window.fill(WHITE)

    drawTiles(window, grid)
    drawGrid(window, totalWidth, cols, rols)
    pygame.display.pygame.update()

def main(window, totalWidth):
    pygame.init()
    run = True
    COLS = 50
    ROWS = 50
    grid = constructGrid(ROWS, COLS, totalWidth)

    while True:
        draw(window, grid, totalWidth, COLS, ROWS)


main(WINDOW,WIDTH)