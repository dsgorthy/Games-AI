
class Mastermind():

	possible_colors = ["R", "B", "O", "W"]
	# ["R", "B", "O"] : XXO
	guess_dict = {}

	def __init__(self, code):
		self.code = code
		self.possibilities = []
		for l1 in self.possible_colors:
			for l2 in self.possible_colors:
				for l3 in self.possible_colors:
					self.possibilities.append(l1+l2+l3)

	def valid_board(self):
		if (len(self.code) != 3):
			return False

		for color in self.code:
			if (color not in self.possible_colors):
				return False

		return True

	def valid_code(self, guess, possible_code, num_x, num_o):
		guess_remainder = ""
		possible_code_remainder = ""
		# Check for right color, right position (X)
		for i in range(0, 3):
			if (guess[i] == possible_code[i]):
				num_x -= 1
			else:
				guess_remainder += guess[i]
				possible_code_remainder += possible_code[i]

		# Did not find enough in right place of right color
		if (num_x != 0):
			return False

		o_found = 0
		# Check for right color, wrong position (O)
		for letter in guess_remainder:
			if letter in possible_code_remainder:
				o_found += 1

		return (o_found == num_o)


	def eliminate(self, guess, result):
		possibilities_to_remove = []
		self.guess_dict[guess] = result
		num_x = result.count('X')
		num_o = len(result) - num_x

		for possible_code in self.possibilities:
			if not (self.valid_code(guess, possible_code, num_x, num_o)):
				possibilities_to_remove.append(possible_code)

		for poss in possibilities_to_remove:
			self.possibilities.remove(poss)


if __name__ == "__main__":

	print("Possible colors: R, B, O, W")
	code = input("Enter board in the format CCC: ")

	board = Mastermind(code)

	if not board.valid_board():
		print("The code you entered was not in the correct format, exiting.")
		exit()

	result = ""
	while (len(board.possibilities) > 0):
		guess = board.possibilities.pop(0)
		print("I'm guessing", guess)
		result = input("How'd I do? ")

		if (result == "XXX"):
			print("Correctly guessed:", guess)
			exit()

		board.eliminate(guess, result)

	print("Hm, I ran out of possible guesses. Something must have gone wrong!")