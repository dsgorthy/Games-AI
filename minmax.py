from copy import deepcopy

vals = ["A", "B", "C", "D", "E", "F", "G", "H"]

class Node(object):
	def __init__(self, red_state, blue_state, color, edge_to_add, depth):
		self.added_edge = deepcopy(edge_to_add)
		self.rs = red_state
		self.bs = blue_state
		self.color = color
		self.children = []
		self.loss = False
		self.red_loss = 0
		self.blue_loss = 0

		if (color == "blue"):
			self.bs[edge_to_add[0]].append(edge_to_add[1])
			self.bs[edge_to_add[1]].append(edge_to_add[0])
			self.next_color = "red"
			if (is_loss(self.bs[edge_to_add[0]], self.bs[edge_to_add[1]])):
				self.loss = True
				self.blue_loss = 1
				return
		else:
			self.rs[edge_to_add[0]].append(edge_to_add[1])
			self.rs[edge_to_add[1]].append(edge_to_add[0])
			self.next_color = "blue"
			if (is_loss(self.rs[edge_to_add[0]], self.rs[edge_to_add[1]])):
				self.loss = True
				self.red_loss = 1
				return

		if (depth == 0):
			return

		edges = self.get_possible_edges()
		for edge in edges:
			new_child = Node(deepcopy(red_state), deepcopy(blue_state), self.next_color, edge, depth-1)
			self.add_child(new_child)
			self.red_loss += new_child.red_loss
			self.blue_loss += new_child.blue_loss


	def get_possible_edges(self):
		edges = []
		for p1 in vals:
			for p2 in vals:
				edge = (p1, p2)
				if (p1 > p2):
					edge = (p2, p1)

				if ((p1 != p2) and (edge not in edges) and (p2 not in self.rs[p1]) and (p2 not in self.bs[p1])):
					edges.append(edge)

		return edges


	def add_child(self, obj):
		self.children.append(obj)


def is_loss(a, b):
	sb = set(b)
	return any(el in sb for el in a)


if __name__ == "__main__":

	#root = Node({"A":[], "B":[], "C":[], "D":[]}, {"A":[], "B":[], "C":[], "D":[]}, "red", ("A", "B"), 6)

	root = Node({"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": []},
			 {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": []},
			  "red", ("A", "B"),4)

	for node in root.children:
		print(node.added_edge)
		print(node.red_loss)
		print(node.blue_loss)
		print(" ")