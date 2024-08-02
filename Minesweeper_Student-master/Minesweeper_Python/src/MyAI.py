<<<<<<< HEAD
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
		self.board[startX][startY] = False  # Mark this tile as uncovered
		self.tilesUncovered += 1
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        # Check if the last action was to uncover a mine
		if number == -1:
			return Action(AI.Action.LEAVE)

		# Attempt to uncover the next unknown tile
		for i in range(self.rowDimension):
			for j in range(self.colDimension):
				if self.board[i][j] is None:  # If tile status is unknown
					self.board[i][j] = False  # Assume it will be uncovered
					return Action(AI.Action.UNCOVER, i, j)

		# If no actions are available, just leave the game
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################