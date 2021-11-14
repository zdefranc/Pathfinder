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
WATER_BLUE2 = (80, 180, 148)
WATER_BLUE3 = (60, 155, 120)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE1 = (128, 0, 255)
PURPLE2 = (100, 0, 200)
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
PATH_OPEN = PURPLE1
PATH_WATER = PURPLE2
PATHFOUND = YELLOW

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
        return tile1.currentDistanceScore < tile2.currentDistanceScore

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

    def setPathOpen(self):
        self.tileType = PATH_OPEN

    def setPathWater(self):
        self.tileType = PATH_WATER

    def setWater(self):
        self.tileType = WATER

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

    def setEstimatedDistanceScore(self,endTile):
        self.estimatedDistanceScore = abs(endTile.col - self.col) + abs(endTile.row - self.row)

    def setNeighbourCurrentDistanceScore(self, neighbourTile):
        distance = WATER_SCORE if neighbourTile.isTileType(WATER) else OPEN_TILE_SCORE
        if not neighbourTile.currentDistanceScore or self.currentDistanceScore + distance < neighbourTile.currentDistanceScore:
            neighbourTile.currentDistanceScore = self.currentDistanceScore + distance

    def getNeighbours(self, grid, pathfinding = False):
        self.neighbours = []
        if self.col < self.totalRows -1 and not self.isTileType(BARRIER):
            if not pathfinding:
                self.setNeighbourCurrentDistanceScore(grid[self.col + 1][self.row])
            self.neighbours.append(grid[self.col + 1][self.row])

        if self.col > 0 and not self.isTileType(BARRIER) and not self.isTileType(BARRIER):
            if not pathfinding:
                self.setNeighbourCurrentDistanceScore(grid[self.col - 1][self.row])
            self.neighbours.append(grid[self.col - 1][self.row])

        if self.row < self.totalRows -1 and not self.isTileType(BARRIER):
            if not pathfinding:
                self.setNeighbourCurrentDistanceScore(grid[self.col][self.row + 1])
            self.neighbours.append(grid[self.col][self.row + 1])

        if self.row > 0 and not self.isTileType(BARRIER):
            if not pathfinding:
                self.setNeighbourCurrentDistanceScore(grid[self.col][self.row - 1])
            self.neighbours.append(grid[self.col][self.row - 1])
    
    def canBePlacedInQueue(self):
        return (not self.isTileType(COVERED_OPEN) and not self.isTileType(COVERED_WATER) and not 
            self.isTileType(START) and not self.isTileType(ACTIVE_OPEN) and not 
            self.isTileType(ACTIVE_WATER) and not self.isTileType(BARRIER))

def readyGrid(draw, grid):
    for row in grid:
        for tile in row:
            if tile.isTileType(COVERED_OPEN) or tile.isTileType(ACTIVE_OPEN) or tile.isTileType(PATH_OPEN):
                tile.reset()
            elif tile.isTileType(COVERED_WATER) or tile.isTileType(ACTIVE_WATER) or tile.isTileType(PATH_WATER):
                tile.setWater()
    draw()

def aStar(draw, grid):
    readyGrid(draw, grid)
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
        startTile.setCurrentDistanceScore(0)

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
                neighbourTile.setEstimatedDistanceScore(endTile)
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
            time.sleep(0.03)
    pathfinderTile = endTile
    pathfinderTile.getNeighbours(grid,True)
    bestScore = math.inf
    startTile.setCurrentDistanceScore(0)
    while not pathfinderTile.currentDistanceScore == 1:
        for neighbourTile in pathfinderTile.neighbours:
            if neighbourTile.isTileType(COVERED_OPEN) or neighbourTile.isTileType(COVERED_WATER):
                if neighbourTile.currentDistanceScore < bestScore:
                    pathfinderTile = neighbourTile
                    bestScore = neighbourTile.currentDistanceScore
        if(not pathfinderTile.isTileType(START)):
            if pathfinderTile.isTileType(COVERED_OPEN):
                pathfinderTile.setPathOpen()
            else:
                pathfinderTile.setPathWater()
    draw()

def resetGrid(grid):
    for row in grid:
        for tile in row:
            tile.reset()

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
                    clickedTile.setWater
                elif event.key == pygame.K_SPACE and startTile and endTile:
                    aStar(lambda: draw(window, grid, totalWidth, COLS, ROWS),grid)
                elif event.key == pygame.K_r:
                    endTile = None
                    startTile = None
                    resetGrid(grid)

        draw(window, grid, totalWidth, COLS, ROWS)


main(WINDOW,WIDTH)
