import math
from PlayerClasses import Player

INFINITY = math.inf
class AI(Player):	
	depth = 0
	currentDepth = 0
	showScores = False
	def __init__(self, chip='X', difficulty=1, showScores='n'):
		super(AI, self).__init__(chip)
		self.setDifficulty(difficulty)
		self.logScores(showScores)		

	def setDifficulty(self, difficulty):
		self.depth = difficulty

	def logScores(self, showScores):
		if showScores == 'y':
			self.showScores = True

	def playTurn(self, board):
		move = self.alphaBetaSearch(board)
		board.addChip(self.chip, move[0], move[1])
		return move

	# returns tuple of (row, column)
	def generateMoves(self, board):
		possibleMoves = [] #list of possible positions
		for column in range(board.boardWidth):
			move = board.canAddChip(column)
			if move[0]: #if chip can be added
				possibleMoves.append((move[1], column)) # (row, column)
		return possibleMoves
	

	def evaluateHeuristic(self, board):
		
		horizontalScore = 0
		verticalScore = 0
		diagonal1Score = 0
		diagonal2Score = 0

		'''	// Vertical
		    // Check each column for vertical score
		    // 
		    // 3 pssible situations per column
		    //  0  1  2  3  4  5  6
		    // [x][ ][ ][ ][ ][ ][ ] 0
		    // [x][x][ ][ ][ ][ ][ ] 1
		    // [x][x][x][ ][ ][ ][ ] 2
		    // [x][x][x][ ][ ][ ][ ] 3
		    // [ ][x][x][ ][ ][ ][ ] 4
		    // [ ][ ][x][ ][ ][ ][ ] 5
    	'''

		for row in range(board.boardHeight - 3):
			for column in range(board.boardWidth):
				score = self.scorePosition(board, row, column, 1, 0)
				verticalScore += score

		'''
			// Horizontal
		    // Check each row's score
		    // 
		    // 4 possible situations per row
		    //  0  1  2  3  4  5  6
		    // [x][x][x][x][ ][ ][ ] 0
		    // [ ][x][x][x][x][ ][ ] 1
		    // [ ][ ][x][x][x][x][ ] 2
		    // [ ][ ][ ][x][x][x][x] 3
		    // [ ][ ][ ][ ][ ][ ][ ] 4
		    // [ ][ ][ ][ ][ ][ ][ ] 5
    	'''
		for row in range(board.boardHeight):
			for column in range(board.boardWidth - 3):
				score = self.scorePosition(board, row, column, 0, 1)
				horizontalScore += score

		'''	// Diagonal points 1 (negative-slope)
		    //
		    // 
		    //  0  1  2  3  4  5  6
		    // [x][ ][ ][ ][ ][ ][ ] 0
		    // [ ][x][ ][ ][ ][ ][ ] 1
		    // [ ][ ][x][ ][ ][ ][ ] 2
		    // [ ][ ][ ][x][ ][ ][ ] 3
		    // [ ][ ][ ][ ][ ][ ][ ] 4
		    // [ ][ ][ ][ ][ ][ ][ ] 5
    	'''
		for row in range(board.boardHeight-3):
			for column in range(board.boardWidth - 3):
				score = self.scorePosition(board, row, column, 1, 1)
				diagonal1Score += score

		'''
		    // Diagonal points 2 (positive slope)
		    //
		    // 
		    //  0  1  2  3  4  5  6
		    // [ ][ ][ ][x][ ][ ][ ] 0
		    // [ ][ ][x][ ][ ][ ][ ] 1
		    // [ ][x][ ][ ][ ][ ][ ] 2
		    // [x][ ][ ][ ][ ][ ][ ] 3
		    // [ ][ ][ ][ ][ ][ ][ ] 4
		    // [ ][ ][ ][ ][ ][ ][ ] 5
		'''
		for row in range(3, board.boardHeight):
			for column in range(board.boardWidth - 3):
				score = self.scorePosition(board, row, column, -1, 1)
				diagonal2Score += score

		return horizontalScore + verticalScore + diagonal1Score + diagonal2Score
	
	def scorePosition(self, board, row, column, deltaROW, deltaCOL):
		'''
			Hueristic evaluation for current state
			+1000, +100, +10, +1 for 4-,3-,2-,1-in-a-line for AI player
			-1000, -100, -10, -1 for 4-,3-,2-,1-in-a-line for human player
			0 otherwise
		'''
		humanScore = 0
		AIScore = 0
		humanPoints = 0
		AIPoints = 0
		for i in range(4):
			currentChip = board.getChip(row, column)
			if currentChip == self.chip: #if current chip is AI
				AIPoints += 1
			elif currentChip == 'O': #player chip
				humanPoints += 1
			# empty otherwise
			row += deltaROW
			column += deltaCOL

		if humanPoints == 1: 
			humanScore = -1 # -1 point
		elif humanPoints == 2:
			humanScore = -10 # -10 points
		elif humanPoints == 3:
			humanScore = -100 # -100 points
		elif humanPoints == 4:
			humanScore = -1000 # -1000 points
		# 0 otherwise

		if AIPoints == 1: 
			AIScore = 1 # 1 point
		elif AIPoints == 2:
			AIScore = 10 # 10 points
		elif AIPoints == 3:
			AIScore = 100 # 100 points
		elif AIPoints == 4:
			AIScore = 1000 # 1000 points
		# 0 otherwise

		return humanScore + AIScore



	def alphaBetaSearch(self, state):
		self.currentDepth = 0
		scores = []
		bestAction = None
		v = max_value = -INFINITY
		alpha = -INFINITY
		beta = INFINITY
		actions = self.generateMoves(state)
		for action in actions:
			state.addChip(self.chip, action[0], action[1])
			v = self.minValue(state, alpha, beta)
			scores.append(v)
			if self.showScores: print("SCORE: ", v)
			if v > max_value:
				bestAction = action
				max_value = v
				alpha = max(alpha, max_value)
			self.currentDepth -= 1
			state.removeChip(action[0], action[1])
		if len(scores) == 1:    
			bestAction = actions[0]
		return bestAction

	def maxValue(self, state, alpha, beta):
		self.currentDepth += 1
		actions = self.generateMoves(state)
		if not actions or self.currentDepth >= self.depth: #if list of next moves is empty or or reached root
			score = self.evaluateHeuristic(state)
			return score
		else:
			v = -INFINITY
			for action in actions:
				state.addChip(self.chip, action[0], action[1])
				v = max(v, self.minValue(state, alpha, beta) )
				if v >= beta:
					self.currentDepth -= 1
					state.removeChip(action[0], action[1])
					return v
				alpha = max(v, alpha)
				self.currentDepth -= 1
				state.removeChip(action[0], action[1])
			return v

	def minValue(self, state, alpha, beta):
		self.currentDepth += 1
		actions = self.generateMoves(state)
		if not actions or self.currentDepth >= self.depth: #if list of next moves is empty or or reached root
			score = self.evaluateHeuristic(state)
			return score
		else:
			v = INFINITY
			for action in actions:
				state.addChip('O', action[0], action[1])
				v = min(v, self.maxValue(state, alpha, beta) )
				if v <= alpha:
					self.currentDepth -= 1
					state.removeChip(action[0], action[1])
					return v
				beta = min(v, beta)
				self.currentDepth -= 1
				state.removeChip(action[0], action[1])
			return v