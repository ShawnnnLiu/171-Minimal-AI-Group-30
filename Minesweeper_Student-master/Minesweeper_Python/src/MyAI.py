#<<<<<<< HEAD
# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import queue

class MyAI(AI):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.boardRows = colDimension
        self.boardColumns = rowDimension
        self.totalMines = totalMines
        self.currentX = startX
        self.currentY = startY

        self.totalSafeSpots = (rowDimension * colDimension) - totalMines
        self.gameBoard = [[-2 for _ in range(self.boardColumns)] for _ in range(self.boardRows)]
        self.probabilityBoard = [[-2 for _ in range(self.boardColumns)] for _ in range(self.boardRows)]
        self.safeQueue = queue.Queue()
        self.visitedCells = []
        self.exploredSpotsCount = 0

        self.neighborOffsets = [(-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (1, -1), (1, 1)]

    def isWithinBounds(self, x, y):
        return 0 <= x < self.boardRows and 0 <= y < self.boardColumns

    def addSafeNeighbors(self, x, y, number):
        """Add neighbors of a cell to the safe queue if applicable."""
        for offsetX, offsetY in self.neighborOffsets:
            newX, newY = x + offsetX, y + offsetY
            if self.isWithinBounds(newX, newY) and (newX, newY) not in self.visitedCells and (newX, newY) not in self.safeQueue.queue:
                if number == 0:
                    self.probabilityBoard[newX][newY] = 0
                    self.safeQueue.put((newX, newY))
                elif self.probabilityBoard[newX][newY] != 0:
                    self.probabilityBoard[newX][newY] = max(1, self.probabilityBoard[newX][newY] + 1)

    def handleVacantCells(self, row, col):
        """Check and handle vacant cells around a given cell."""
        vacant, flagged = self.identifyNeighbors(row, col)
        if vacant and len(vacant) == self.gameBoard[row][col] - len(flagged):
            vacantX, vacantY = vacant.pop(0)
            self.decrementProbabilityAround(row, col)
            self.removeFromQueue(vacantX, vacantY)
            return vacantX, vacantY, AI.Action.FLAG
        return None

    def identifyNeighbors(self, row, col):
        """Identify vacant and flagged neighbors around a given cell."""
        vacant, flagged = [], []
        for offsetX, offsetY in self.neighborOffsets:
            newX, newY = row + offsetX, col + offsetY
            if self.isWithinBounds(newX, newY):
                if self.gameBoard[newX][newY] == -2:
                    vacant.append((newX, newY))
                elif self.gameBoard[newX][newY] == -1:
                    flagged.append((newX, newY))
        return vacant, flagged

    def decrementProbabilityAround(self, row, col):
        """Decrement the probability values of the neighbors around a given cell."""
        for offsetX, offsetY in self.neighborOffsets:
            newX, newY = row + offsetX, col + offsetY
            if self.isWithinBounds(newX, newY) and self.probabilityBoard[newX][newY] > 0:
                self.probabilityBoard[newX][newY] -= 1

    def removeFromQueue(self, x, y):
        """Remove a specific cell from the queue."""
        newQueue = queue.Queue()
        while not self.safeQueue.empty():
            item = self.safeQueue.get()
            if item != (x, y):
                newQueue.put(item)
        self.safeQueue = newQueue

    def processZeroCase(self, number):
        self.addSafeNeighbors(self.currentX, self.currentY, number)

        for row in range(self.boardRows):
            for col in range(self.boardColumns):
                if (self.probabilityBoard[row][col] == 0 and 
                    (row, col) not in self.visitedCells and 
                    (row, col) not in self.safeQueue.queue):
                    self.safeQueue.put((row, col))
                    continue

                if self.gameBoard[row][col] == -2:
                    continue

                result = self.handleVacantCells(row, col)
                if result:
                    return result

                flaggedCount = len(self.identifyNeighbors(row, col)[1])
                if self.gameBoard[row][col] == flaggedCount:
                    self.markSafeNeighbors(row, col)

        if not self.safeQueue.empty():
            coordinate = self.safeQueue.get()
            return coordinate[0], coordinate[1], AI.Action.UNCOVER
        else:
            for row in range(len(self.gameBoard)):
                for col in range(len(self.gameBoard[row])):
                    if self.gameBoard[row][col] == -2:
                        return row, col, AI.Action.UNCOVER
            
            return 1, 1, AI.Action.LEAVE

    def markSafeNeighbors(self, row, col):
        """Mark all neighbors of a cell as safe if they are unflagged."""
        for offsetX, offsetY in self.neighborOffsets:
            newX, newY = row + offsetX, col + offsetY
            if self.isWithinBounds(newX, newY) and self.gameBoard[row][col] >= 0:
                self.probabilityBoard[newX][newY] = 0
                if (newX, newY) not in self.visitedCells and (newX, newY) not in self.safeQueue.queue:
                    self.safeQueue.put((newX, newY))

    def getAction(self, number: int) -> "Action Object":
        if self.exploredSpotsCount == self.totalSafeSpots:
            return Action(AI.Action.LEAVE, 1, 1)
        
        x, y = self.currentX, self.currentY
        self.gameBoard[x][y] = number 
        self.probabilityBoard[x][y] = 0 
        
        self.currentX, self.currentY, actionType = self.processZeroCase(number)

        if actionType != AI.Action.FLAG:
            self.exploredSpotsCount += 1
        self.visitedCells.append((self.currentX, self.currentY))
        return Action(actionType, self.currentX, self.currentY)





			
