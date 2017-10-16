import random

class SIM_board():

	possible_nodes = ["A", "B", "C", "D", "E", "F", "G", "H"]
	computer_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}
	player_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}

	def __init__(self):
		pass

	# Valid -> Return true and add to list
	# Not valid -> Return false
	# 
	def move(self, player, p1, p2):
		if (p1 == p2):
			return False

		# Check if p1, p2 in possible nodes
		if (p1 not in self.possible_nodes) or (p2 not in self.possible_nodes):
			return False

		potential_move = (p1, p2)
		sorted(potential_move)

		# Check if line has been used
		if (potential_move[1] in self.computer_nodes[potential_move[0]]) or (potential_move[1] in self.player_nodes[potential_move[0]]):

			return False

		if (player == "comp"):
			self.computer_nodes[potential_move[0]].append(potential_move[1])
			self.computer_nodes[potential_move[1]].append(potential_move[0])
		else:
			self.player_nodes[potential_move[0]].append(potential_move[1])
			self.player_nodes[potential_move[1]].append(potential_move[0])

		return True


	def player_lost(self, player, last_point1, last_point2):

		if (player == "comp"):
			return lists_overlap(self.computer_nodes[last_point1], self.computer_nodes[last_point2])
		else:
			return lists_overlap(self.player_nodes[last_point1], self.player_nodes[last_point2])


	def computer_choice(self):


		# Return point1, point2
		return random.choice(board.possible_nodes), random.choice(board.possible_nodes)


def lists_overlap(a, b):
	sb = set(b)
	return any(el in sb for el in a)


if __name__ == "__main__":

	computer_name = "comp"
	player_name = "player"
	board = SIM_board()
	point1 = "Z"
	point2 = "Z"

	color = input("Are you playing Red? (Y/N): ")

	# player chose red, go first
	if (color == "Y"):
		truth = False

		while not truth:
			point1 = input("Player, enter first point: ")
			point2 = input("Player, enter second point: ")
			truth = board.move("player", point1, point2)

	still_playing = True	
	while (still_playing):
		# Computer moves
		entered_valid_move = False
		while not entered_valid_move:
			point1, point2 = board.computer_choice()
			entered_valid_move = board.move("comp", point1, point2)
		print("The computer entered the move ", point1, ", ", point2)

		if (board.player_lost("comp", point1, point2)):
			print("The computer lost!")
			exit()

		# Player moves
		entered_valid_move = False
		while not entered_valid_move:
			point1 = input("Player, enter first point: ")
			point2 = input("Player, enter second point: ")
			entered_valid_move = board.move("player", point1, point2)

		if (board.player_lost("player", point1, point2)):
			print("The player lost!")
			exit()
