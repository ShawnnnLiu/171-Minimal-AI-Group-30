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
		self.suspicionTable[startX][startY] = 100000
		self.uncovered.append((startX, startY))

		# Truth board
		self.truth_board = [['.' for _ in range(colDimension)] for _ in range(rowDimension)]
		self.truth_board[startX][startY] = 0
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def client_coord_to_server(self, coord):
		return (coord[0]+1, self.colDimension-coord[1])
	
	def server_coord_to_client(self, coord):
		return (coord[0]-1, self.colDimension-coord[1])

	def print_suspicion_table(self):
		print("Suspicion Table:")
		for col in range(self.colDimension):
			print(" ".join(f"{self.suspicionTable[row][self.colDimension - 1 - col]:2}" for row in range(self.rowDimension)))
		print()  # Adds a blank line after the table for readability

	def print_truth_table(self):
		print("Truth Table:")
		for col in range(self.colDimension):
			print(" ".join(f"{self.truth_board[row][self.colDimension - 1 - col]:2}" for row in range(self.rowDimension)))
		print()  # Adds a blank line after the table for readability

	def update_suspicion_table(self, row, col, number):
		for j in range(max(0, col - 1), min(self.colDimension, col + 2)):
			for i in range(max(0, row - 1), min(self.rowDimension, row + 2)):
				if (i, j) not in self.uncovered:
					self.suspicionTable[i][j] += number
		#self.print_suspicion_table() # Remember to remove print line

	def update_truth_table(self, row, col, number):
		self.truth_board[row][col] = number
		#self.print_truth_table() # Remember to remove print line

	def find_lowest_suspicion_tile(self):
		min_suspicion = float('inf')
		min_tile = None
		for j in range(self.colDimension):
			for i in range(self.rowDimension):
				if (i, j) not in self.uncovered and self.suspicionTable[i][j] < min_suspicion:
					min_suspicion = self.suspicionTable[i][j]
					min_tile = (i, j)
		return (min_tile[0], min_tile[1])
		
	def getAction(self, number: int):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        # Check if the last action was to uncover a mine
		if number == -1:
			return Action(AI.Action.LEAVE)
		elif number == 0:
			self.update_suspicion_table(self.uncovered[-1][0], self.uncovered[-1][1], (-5))
		else:
			self.update_suspicion_table(self.uncovered[-1][0], self.uncovered[-1][1], number)

		self.update_truth_table(self.uncovered[-1][0], self.uncovered[-1][1], number)

		self.print_truth_table()
		coord = self.find_lowest_suspicion_tile()
		#print("LOWEST SUSPICION TILE: " + str(coord[0]) + " " + str(coord[1])) # Remember to remove print statement
		self.uncovered.append(coord)

		self.suspicionTable[coord[0]][coord[1]] = 100000
		return Action(AI.Action.UNCOVER, coord[0], coord[1])


		# If no actions are available, just leave the game
		
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


