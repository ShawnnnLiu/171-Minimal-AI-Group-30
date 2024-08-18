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


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        # Initialize board dimensions and mines information
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines

		# Initialize board state: None means unknown, True for flagged, False for cleared
		self.board = [[None for _ in range(colDimension)] for _ in range(rowDimension)]
		self.minesFlagged = 0
		self.tilesUncovered = 0

		# Starting point is typically uncovered by the game before the AI starts
		self.startX = startX
		self.startY = startY

		# For suspicion table
		self.suspicionTable = [[0 for _ in range(colDimension)] for _ in range(rowDimension)]
		self.uncovered = []
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def print_suspicion_table(self):
		print("Suspicion Table:")
		for row in self.suspicion_table:
			print(" ".join(f"{cell:2}" for cell in row))
		print()  # Adds a blank line after the table for readability


	def update_suspicion_table(self, row, col, number):
		for i in range(max(0, row - 1), min(self.row_dimension, row + 2)):
			for j in range(max(0, col - 1), min(self.col_dimension, col + 2)):
				if (i, j) not in self.uncovered:
					self.suspicion_table[i][j] += number
		self.print_suspicion_table()

	def find_lowest_suspicion_tile(self):
		min_suspicion = float('inf')
		min_tile = None
		for i in range(self.row_dimension):
			for j in range(self.col_dimension):
				if (i, j) not in self.uncovered and self.suspicion_table[i][j] < min_suspicion:
					min_suspicion = self.suspicion_table[i][j]
					min_tile = (i, j)
		return min_tile
		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        # Check if the last action was to uncover a mine
		if number == -1:
			if self.awaitingFlag == False:
				return Action(AI.Action.LEAVE)
			else:
				self.awaitingFlag = False
		elif number == 0:
			self.update_suspicion_table(self.uncovered[-1][0], self.uncovered[-1][1], -10)
		else:
			self.update_suspicion_table(self.uncovered[-1][0], self.uncovered[-1][1], number)

			

		if not self.uncovered:
			self.uncovered.append((self.startX, self.startY))
			Action(AI.Action.UNCOVER, self.startX, self.startY)
		else:
			coord = self.find_lowest_suspicion_tile()
			print("LOWEST SUSPICION TILE: " + coord)
			self.uncovered.append(coord)
			Action(AI.Action.UNCOVER, coord[0], coord[1])


		# If no actions are available, just leave the game
		
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################