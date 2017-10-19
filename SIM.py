from copy import deepcopy

vals = ["A", "B", "C", "D","E"]

class SIM_board():

	computer_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[]}
	player_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[]}
	computer_loss_edges = []
	player_loss_edges = []

	#possible_nodes = ["A", "B", "C", "D", "E", "F", "G", "H"]
	#computer_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}
	#player_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}

	def __init__(self):
		self.remaining_edges = []
		for p1 in vals:
			for p2 in vals:
				if (p1 != p2):
					self.remaining_edges.append((p1,p2))

	# Valid -> Return true and add to list
	# Not valid -> Return false
	# 
	def move(self, player, p1, p2):
		if (p1 == p2):
			return False

		# Check if p1, p2 in possible nodes
		if (p1 not in vals) or (p2 not in vals):
			return False

		potential_move = (p1, p2)
		sorted(potential_move)

		# Check if line has been used
		if (potential_move[1] in self.computer_nodes[potential_move[0]]) or (potential_move[1] in self.player_nodes[potential_move[0]]):
			return False

		if (player == "comp"):
			self.computer_nodes[potential_move[0]].append(potential_move[1])
			self.computer_nodes[potential_move[1]].append(potential_move[0])

			for p1 in vals:
				for p2 in vals:
					# Avoid repeats and edges that have been used
					if ((p1 != p2) and ((p1, p2) not in self.computer_loss_edges) and (p2 not in self.computer_nodes[p1]) and 
						(p1 not in self.computer_nodes[p2]) and (p1 not in self.player_nodes[p2]) and (p2 not in self.player_nodes[p1])):
						if self.player_lost("comp", p1, p2):
							self.computer_loss_edges.append((p1,p2))

		else:
			self.player_nodes[potential_move[0]].append(potential_move[1])
			self.player_nodes[potential_move[1]].append(potential_move[0])

			for p1 in vals:
				for p2 in vals:
					# Avoid repeats and edges that have been used
					if ((p1 != p2) and ((p1, p2) not in self.player_loss_edges) and (p2 not in self.computer_nodes[p1]) and 
						(p1 not in self.computer_nodes[p2]) and (p1 not in self.player_nodes[p2]) and (p2 not in self.player_nodes[p1])):
						if self.player_lost("player", p1, p2):
							self.player_loss_edges.append((p1,p2))

		self.remaining_edges.remove(potential_move)
		self.remaining_edges.remove((potential_move[1], potential_move[0]))

		return True


	def player_lost(self, player, last_point1, last_point2):

		if (player == "comp"):
			return lists_overlap(self.computer_nodes[last_point1], self.computer_nodes[last_point2])
		else:
			return lists_overlap(self.player_nodes[last_point1], self.player_nodes[last_point2])


	def computer_choice(self):
		all_choices = deepcopy(self.remaining_edges)
		# Remove all certain losses from list of choices
		for loss in self.computer_loss_edges:
			if (loss in all_choices):
				all_choices.remove(loss)

		# Certain loss, return first
		if (len(all_choices) == 0):
			return self.remaining_edges[0]

		not_loss = deepcopy(all_choices)
		# Remove all edges that will cause player to lose
		for player_loss in self.player_loss_edges:
			if (player_loss in not_loss):
				not_loss.remove(player_loss)

		# All edges will cause player to lose, return first
		if (len(not_loss) == 0):
			return all_choices[0]

		# Return one-sided if possible
		n1 = "Z"
		for p in self.computer_nodes.keys():
			if (n1 == "Z" and len(self.computer_nodes[p]) == 0):
				n1 = p
			elif (n1 != "Z" and len(self.computer_nodes[p]) == 0):
				return n1, p

		# INSERT DECISION TREE HERE

		# Return point1, point2
		return not_loss[0]


def lists_overlap(a, b):
	sb = set(b)
	return any(el in sb for el in a)


if __name__ == "__main__":

	computer_name = "comp"
	player_name = "player"
	board = SIM_board()

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
