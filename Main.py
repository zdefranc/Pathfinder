import pygame
import math
from queue import PriorityQueue
import time

WIDTH = 600

WINDOW = pygame.display.set_mode((WIDTH,WIDTH))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 140)
WATER_BLUE1 = (102, 205, 170)
WATER_BLUE2 = (103, 204, 171)
WATER_BLUE3 = (104, 205, 172)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 255)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
MARS = (255, 127, 80)

START = GREEN
END = RED
BARRIER = BLACK
WATER = WATER_BLUE1
OPEN = MARS
COVERED_OPEN = ORANGE
COVERED_WATER = WATER_BLUE2
ACTIVE_OPEN = GREY
ACTIVE_WATER = WATER_BLUE3

WATER_SCORE = 2
OPEN_TILE_SCORE = 1

class Tile:
    def __init__(self, column, row, width, totalCols, totalRows):
        self.col = column
        self.row = row
        self.x = width * column
        self.y = width * row
        self.width = width
        self.totalRows = totalRows
        self.totalCols = totalCols
        self.neighbours = []
        self.tileType = OPEN
        self.currentDistanceScore = None
        self.estimatedDistanceScore = None
        self.totalDistanceScore = None

    def __lt__(tile1,tile2):
        if tile1.totalDistanceScore != tile2.totalDistanceScore:
            return tile1.totalDistanceScore < tile2.totalDistanceScore
        else:
            return tile1.estimatedDistanceScore < tile2.estimatedDistanceScore

    def getTileType(self): 
        return self.tileType

    def isTileType(self, status):
        return self.tileType == status

    def reset(self):
        self.tileType = OPEN

    def setStart(self):
        self.tileType = START

    def setBarrier(self):
        self.tileType = BARRIER

    def setEnd(self):
        self.tileType = END

    def setActive(self):
        if not self.isTileType(END):
            if self.isTileType(OPEN):
                self.tileType = ACTIVE_OPEN
            else:
                self.tileType = ACTIVE_WATER

    def setCovered(self):
        if self.isTileType(ACTIVE_OPEN):
            self.tileType = COVERED_OPEN
        else:
            self.tileType = COVERED_WATER
    
    def setCurrentDistanceScore(self, score):
        self.currentDistanceScore = score

    def getEstimatedDistanceScore(self,endTile):
        self.estimatedDistanceScore = abs(endTile.col - self.col) + abs(endTile.row - self.row)

    def getNeighbourCurrentDistanceScore(self, neighbourTile):
        distance = WATER_SCORE if neighbourTile.isTileType(WATER) else OPEN_TILE_SCORE
        if not neighbourTile.currentDistanceScore or self.currentDistanceScore + distance < neighbourTile.currentDistanceScore:
            neighbourTile.currentDistanceScore = self.currentDistanceScore + distance

    def getNeighbours(self, grid):
        self.neighbours = []
        if self.col < self.totalRows -1 and not self.isTileType(BARRIER):
            self.getNeighbourCurrentDistanceScore(grid[self.col + 1][self.row])
            self.neighbours.append(grid[self.col + 1][self.row])

        if self.col > 0 and not self.isTileType(BARRIER) and not self.isTileType(BARRIER):
            self.getNeighbourCurrentDistanceScore(grid[self.col - 1][self.row])
            self.neighbours.append(grid[self.col - 1][self.row])

        if self.row < self.totalRows -1 and not self.isTileType(BARRIER):
            self.getNeighbourCurrentDistanceScore(grid[self.col][self.row + 1])
            self.neighbours.append(grid[self.col][self.row + 1])

        if self.row > 0 and not self.isTileType(BARRIER):
            self.getNeighbourCurrentDistanceScore(grid[self.col][self.row - 1])
            self.neighbours.append(grid[self.col][self.row - 1])
    
    def canBePlacedInQueue(self):
        return (not self.isTileType(COVERED_OPEN) and not self.isTileType(COVERED_WATER) and not 
            self.isTileType(START) and not self.isTileType(ACTIVE_OPEN) and not 
            self.isTileType(ACTIVE_WATER) and not self.isTileType(BARRIER))


def aStar(draw, grid):
    startTile = None
    endTile = None
    currentTile = None
    activeTileQueue = PriorityQueue()
    for row in grid:
        for tile in row:
            if tile.isTileType(START):
                startTile = tile
            elif tile.isTileType(END):
                endTile = tile
    if(startTile and endTile):
        currentTile = startTile
        currentTile.setCurrentDistanceScore(0)

        while(not currentTile.isTileType(END)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if not activeTileQueue.empty():
                currentTile = activeTileQueue.get()[1]
            if not currentTile.isTileType(END) and not currentTile.isTileType(START):
                currentTile.setCovered()
            currentTile.getNeighbours(grid)
            for neighbourTile in currentTile.neighbours:
                neighbourTile.getEstimatedDistanceScore(endTile)
                neighbourTile.totalDistanceScore = neighbourTile.estimatedDistanceScore + neighbourTile.currentDistanceScore
                if neighbourTile.canBePlacedInQueue():
                    neighbourTile.setActive()
                    activeTileQueue.put((neighbourTile.totalDistanceScore,neighbourTile))
            # Uncomment to view scores
            # print(currentTile.totalDistanceScore)
            # print(currentTile.estimatedDistanceScore)
            # print(currentTile.currentDistanceScore)
            # print("new")
            draw()
            time.sleep(0.1)
        #Draw path

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
            pygame.draw.rect(window, i.tileType, (i.x, i.y, i.width, i.width))

def draw(window, grid, totalWidth, cols, rols):
    window.fill(WHITE)

    drawTiles(window, grid)
    drawGrid(window, totalWidth, cols, rols)
    pygame.display.update()

def getClickedTile(grid, totalWidth, rows):
        gap = totalWidth/rows
        x, y = pygame.mouse.get_pos()

        tileIndexX = math.floor(x/gap)
        tileIndexY = math.floor(y/gap)

        return grid[tileIndexX][tileIndexY]


def main(window, totalWidth):
    run = True
    COLS = 50
    ROWS = 50
    grid = constructGrid(ROWS, COLS, totalWidth)
    startTile = None
    endTile = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if pygame.mouse.get_pressed()[0]:
                clickedTile = getClickedTile(grid,WIDTH,ROWS)
                if not startTile and clickedTile != endTile:
                    clickedTile.setStart()
                    startTile = clickedTile
                elif not endTile and clickedTile != startTile:
                    clickedTile.setEnd()
                    endTile = clickedTile
                elif clickedTile != startTile and clickedTile != endTile:
                    clickedTile.setBarrier()
                
            elif pygame.mouse.get_pressed()[2]:
                clickedTile = getClickedTile(grid,WIDTH,ROWS)
                clickedTile.reset()
                if clickedTile == startTile:
                    startTile = None
                elif clickedTile == endTile:
                    endTile = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    clickedTile = getClickedTile(grid, WIDTH, ROWS)
                    clickedTile.tileType = WATER
                elif event.key == pygame.K_SPACE and startTile and endTile:
                    aStar(lambda: draw(window, grid, totalWidth, COLS, ROWS),grid)

        draw(window, grid, totalWidth, COLS, ROWS)


main(WINDOW,WIDTH)
