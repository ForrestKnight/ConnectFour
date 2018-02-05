from PlayerClasses import Player, Human
from AIClass import AI
from GameBoard import GameBoard

class GameClient:
	board = None
	human = None
	ai = None
	winnerFound = False
	humansTurn = True
	currentRound = 1
	MAX_ROUNDS = 42 #max number of turns before game baord is full

	def __init__(self):
		self.board = GameBoard()
		self.human = Human('O')
		difficulty = int(input("Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))
		showScores = input("Show scores? (y/n)> ")
		self.ai = AI('X', difficulty, showScores)

	def play(self):
		print("Playing game...")
		self.board.printBoard()
		winner = "It's a DRAW!"
		while self.currentRound <= self.MAX_ROUNDS and not self.winnerFound:
			if self.humansTurn:
				print("Player's turn...")
				playedChip = self.human.playTurn(self.board)
				self.winnerFound = self.board.isWinner(self.human.chip)
				if self.winnerFound: winner = "PLAYER wins!"
				self.humansTurn = False
				print("Player played chip at column ", playedChip[1]+1)
			else:
				print("AI's turn...")
				playedChip = self.ai.playTurn(self.board)
				self.winnerFound = self.board.isWinner(self.ai.chip)
				if self.winnerFound: winner = "AI wins!"
				self.humansTurn = True
				print("AI played chip at column ", playedChip[1]+1)
			self.currentRound += 1
			self.board.printBoard()
		return winner

	def reset(self):
		#reset variables
		self.currentRound = 1
		self.winnerFound = False
		self.humansTurn = True
		self.board.resetBoard()
		difficulty = int(input("Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))
		self.ai.setDifficulty(difficulty)

def endGame(winner):
	print(winner, end=" ")
	userInput = input("Play again? (y/n)\n")
	return True if userInput == 'y' else False

if __name__ == "__main__":
	gameClient = GameClient()
	winner = gameClient.play()
	playAgain = endGame(winner)
	while playAgain:
		gameClient.reset()
		winner = gameClient.play()
		playAgain = endGame(winner)
