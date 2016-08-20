from cube import Cube

class SearchNode:
	
	def __init__(self, cube, parent, path):
		self._cube = cube
		self._path = path


	def is_goal(self):
		return self._cube.is_solved()

	def get_depth(self):
		return len(self._path)

	def get_next_legal_moves(self):
		moves = list(Cube.moves)
		if len(self._path) > 0:
			last_move = self._path[-1]
			moves.remove(Cube.reciprocal_move[last_move])
		return moves

	def expand_to(self, move):
		c = Cube(self._cube, move)
		return SearchNode(c, self, self._path + move)

	def expand(self):
		return [self.expand_to(m) for m in self.get_next_legal_moves()]

	def state_to_string(self):
		return self._cube.data_as_string()

	def get_path(self):
		return self._path

	def get_cube(self):
		return self._cube
