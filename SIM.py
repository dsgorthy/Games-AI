from copy import deepcopy

vals = ["A", "B", "C", "D", "E", "F", "G", "H"]

class Node(object):
	def __init__(self, computer_state, player_state, which, edge_to_add, depth):
		self.added_edge = deepcopy(edge_to_add)
		self.cs = deepcopy(computer_state)
		self.ps = deepcopy(player_state)
		self.children = []
		self.loss = False
		self.computer_loss = 0
		self.player_loss = 0

		if (which == "comp"):
			self.cs[edge_to_add[0]].append(edge_to_add[1])
			self.cs[edge_to_add[1]].append(edge_to_add[0])
			self.next_player = "player"
			if (lists_overlap(self.cs[edge_to_add[0]], self.cs[edge_to_add[1]])):
				self.loss = True
				self.computer_loss = 1
				return
		else:
			self.ps[edge_to_add[0]].append(edge_to_add[1])
			self.ps[edge_to_add[1]].append(edge_to_add[0])
			self.next_player = "comp"
			if (lists_overlap(self.ps[edge_to_add[0]], self.ps[edge_to_add[1]])):
				self.loss = True
				self.player_loss = 1
				return

		if (depth == 0):
			return

		edges = self.get_possible_edges()
		for edge in edges:
			new_child = Node(deepcopy(self.cs), deepcopy(self.ps), self.next_player, edge, depth-1)
			self.add_child(new_child)
			self.computer_loss += new_child.computer_loss
			self.player_loss += new_child.player_loss

	def get_possible_edges(self):
		edges = []
		for p1 in vals:
			for p2 in vals:
				edge = (p1, p2)
				if (p1 > p2):
					edge = (p2, p1)

				if ((p1 != p2) and (edge not in edges) and (p2 not in self.cs[p1]) and (p2 not in self.ps[p1])):
					edges.append(edge)

		return edges

	def add_child(self, obj):
		self.children.append(obj)


class SIM_board():

	#computer_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[]}
	#player_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[]}
	computer_loss_edges = []
	player_loss_edges = []

	#possible_nodes = ["A", "B", "C", "D", "E", "F", "G", "H"]
	computer_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}
	player_nodes = {"A":[], "B":[], "C":[], "D":[], "E":[], "F":[], "G":[], "H":[]}

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


	def computer_choice(self, p1, p2, depth):
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

		# Build decision tree
		decision_tree = Node(self.computer_nodes, self.player_nodes, "player", (p1,p2), depth)
		
		# Maximize player loss - to - computer loss ratio
		ratio = -1
		for choice in decision_tree.children:
			try:
				this_ratio = choice.player_loss/choice.computer_loss
				if (this_ratio > ratio):
					ratio = this_ratio
					best_move = choice.added_edge
			except:
				# No computer losses!
				return choice.added_edge

		return best_move


def lists_overlap(a, b):
	sb = set(b)
	return any(el in sb for el in a)


if __name__ == "__main__":

	moves = 0
	point1 = ""
	point2 = ""
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
		moves += 1

	still_playing = True	
	while (still_playing):
		# Computer moves
		entered_valid_move = False
		while not entered_valid_move:
			point1, point2 = board.computer_choice(point1, point2, int(moves/3))
			entered_valid_move = board.move("comp", point1, point2)
		print("The computer entered the move ", point1, ", ", point2)
		moves += 1

		if (board.player_lost("comp", point1, point2)):
			print("The computer lost!")
			exit()

		# Player moves
		entered_valid_move = False
		while not entered_valid_move:
			point1 = input("Player, enter first point: ")
			point2 = input("Player, enter second point: ")
			entered_valid_move = board.move("player", point1, point2)
		moves += 1

		if (board.player_lost("player", point1, point2)):
			print("The player lost!")
			exit()
