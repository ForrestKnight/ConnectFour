class GameBoard:
	board = []
	boardWidth = 7
	boardHeight = 6

	def __init__(self):
		self.setBoard()
		
	def setBoard(self):
		for row in range(self.boardHeight):
			self.board.append([])
			for column in range(self.boardWidth):
				self.board[row].append('-')

	def resetBoard(self):
		for row in range(self.boardHeight):
			for column in range(self.boardWidth):
				self.board[row][column] = '-'

	def printBoard(self):
		for i in range(self.boardHeight):
			print("| ", end="")
			print(*self.board[i], sep=" | ", end="")
			print(" |\n")

	def isValidColumn(self, column):
		return False if column < 0 or column >= self.boardWidth else True

	def getChip(self, row, column):
		return self.board[row][column]

	'''Check if there is room to add in a chip
		return row if chip can be added'''
	def canAddChip(self, column):
		for i in range( (self.boardHeight-1), -1, -1): #from 5 to 0
			if self.board[i][column] == '-':
				return True, i
		return False, -1

	def addChip(self, chip, row, column):
		'''check if there is room for a chip to add
			starting from bottom, return true if spot empty, 	false otherwise
		'''
		self.board[row][column] = chip

	def removeChip(self, row, column):
		self.board[row][column] = '-'

	def isWinner(self, chip):
		
		ticks = 0
		# vertical
		for row in range(self.boardHeight - 3):
			for column in range(self.boardWidth):
				ticks = self.checkAdjacent(chip, row, column, 1, 0)
				if ticks == 4: return True
		# horizontal
		for row in range(self.boardHeight):
			for column in range(self.boardWidth - 3):
				ticks = self.checkAdjacent(chip, row, column, 0, 1)
				if ticks == 4: return True
		# positive slope diagonal
		for row in range(self.boardHeight-3):
			for column in range(self.boardWidth - 3):
				ticks = self.checkAdjacent(chip, row, column, 1, 1)
				if ticks == 4: return True
		#negative slope diagonal
		for row in range(3, self.boardHeight):
			for column in range(self.boardWidth - 5):
				ticks = self.checkAdjacent(chip, row, column, -1, 1)
				if ticks == 4: return True
		return False

	def checkAdjacent(self, chip, row, column, deltaROW, deltaCOL):
		count = 0
		for i in range(4):
			currentChip = self.getChip(row, column)
			if currentChip == chip:
				count += 1
			row += deltaROW
			column += deltaCOL
		return count