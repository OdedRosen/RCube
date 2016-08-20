import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Cube:

	# color codes (static):
	moves = ['L','l','M','m','R','r','U','u','E','e','D','d','F','f','S','s','B','b']
	cubecolors = ['#FFD500', '#0051BA', '#C41E3A', '#FFFFFF', '#009E60', '#FF5800']
	face_moves = {'L': 4, 'l': 4, 'R': 1, 'r': 1, 'U': 2, 'u': 2, 'D': 5, 'd': 5, 'F': 0, 'f': 0, 'B': 3, 'b': 3}
	face_moves_dir = {'L': 1, 'l': 0, 'R': 1, 'r': 0, 'U': 1, 'u': 0, 'D': 1, 'd': 0, 'F': 1, 'f': 0, 'B': 1, 'b': 0}
	rotate_rules = {
		'L': [(0,0,2,0), (0,3,2,3), (0,6,2,6), (2,0,3,0), (2,3,3,3), (2,6,3,6), 
				(3,0,5,0), (3,3,5,3), (3,6,5,6), (5,0,0,0), (5,3,0,3), (5,6,0,6)],
		'l': [(0,0,5,0), (0,3,5,3), (0,6,5,6), (5,0,3,0), (5,3,3,3), (5,6,3,6), 
				(3,0,2,0), (3,3,2,3), (3,6,2,6), (2,0,0,0), (2,3,0,3), (2,6,0,6)],
		'M': [(0,1,2,1), (0,4,2,4), (0,7,2,7), (2,1,3,1), (2,4,3,4), (2,7,3,7), 
				(3,1,5,1), (3,4,5,4), (3,7,5,7), (5,1,0,1), (5,4,0,4), (5,7,0,7)],
		'm': [(0,1,5,1), (0,4,5,4), (0,7,5,7), (5,1,3,1), (5,4,3,4), (5,7,3,7), 
				(3,1,2,1), (3,4,2,4), (3,7,2,7), (2,1,0,1), (2,4,0,4), (2,7,0,7)],
		'R': [(0,2,5,2), (0,5,5,5), (0,8,5,8), (5,2,3,2), (5,5,3,5), (5,8,3,8), 
				(3,2,2,2), (3,5,2,5), (3,8,2,8), (2,2,0,2), (2,5,0,5), (2,8,0,8)],
		'r': [(0,2,2,2), (0,5,2,5), (0,8,2,8), (2,2,3,2), (2,5,3,5), (2,8,3,8), 
				(3,2,5,2), (3,5,5,5), (3,8,5,8), (5,2,0,2), (5,5,0,5), (5,8,0,8)],
		
		'U': [(0,0,1,0), (0,1,1,3), (0,2,1,6), (1,0,3,8), (1,3,3,7), (1,6,3,6), 
				(3,8,4,6), (3,7,4,3), (3,6,4,0), (4,6,0,0), (4,3,0,1), (4,0,0,2)],
		'u': [(0,0,4,6), (0,1,4,3), (0,2,4,0), (4,6,3,8), (4,3,3,7), (4,0,3,6),
				(3,8,1,0), (3,7,1,3), (3,6,1,6), (1,0,0,0), (1,3,0,1), (1,6,0,2)],
		'E': [(0,3,4,7), (0,4,4,4), (0,5,4,1), (4,7,3,5), (4,4,3,4), (4,1,3,3), 
				(3,5,1,1), (3,4,1,4), (3,3,1,7), (1,1,0,3), (1,4,0,4), (1,7,0,5)],
		'e': [(0,3,1,1), (0,4,1,4), (0,5,1,7), (1,1,3,5), (1,4,3,4), (1,7,3,3), 
				(3,5,4,7), (3,4,4,4), (3,3,4,1), (4,7,0,3), (4,4,0,4), (4,1,0,5)],
		'D': [(0,6,4,8), (0,7,4,5), (0,8,4,2), (4,8,3,2), (4,5,3,1), (4,2,3,0), 
				(3,2,1,2), (3,1,1,5), (3,0,1,8), (1,2,0,6), (1,5,0,7), (1,8,0,8)],
		'd': [(0,6,1,2), (0,7,1,5), (0,8,1,8), (1,2,3,2), (1,5,3,1), (1,8,3,0), 
				(3,2,4,8), (3,1,4,5), (3,0,4,2), (4,8,0,6), (4,5,0,7), (4,2,0,8)],

		'F': [(1,0,2,6), (1,1,2,7), (1,2,2,8), (2,6,4,2), (2,7,4,1), (2,8,4,0), 
				(4,2,5,2), (4,1,5,1), (4,0,5,0), (5,2,1,0), (5,1,1,1), (5,0,1,2)],
		'f': [(1,0,5,2), (1,1,5,1), (1,2,5,0), (5,2,4,2), (5,1,4,1), (5,0,4,0), 
				(4,2,2,6), (4,1,2,7), (4,0,2,8), (2,6,1,0), (2,7,1,1), (2,8,1,2)],
		'S': [(1,3,2,3), (1,4,2,4), (1,5,2,5), (2,3,4,5), (2,4,4,4), (2,5,4,3), 
				(4,5,5,5), (4,4,5,4), (4,3,5,3), (5,5,1,3), (5,4,1,4), (5,3,1,5)],
		's': [(1,3,5,5), (1,4,5,4), (1,5,5,3), (5,5,4,5), (5,4,4,4), (5,3,4,3), 
				(4,5,2,3), (4,4,2,4), (4,3,2,5), (2,3,1,3), (2,4,1,4), (2,5,1,5)],
		'B': [(1,6,5,8), (1,7,5,7), (1,8,5,6), (5,8,4,8), (5,7,4,7), (5,6,4,6), 
				(4,8,2,0), (4,7,2,1), (4,6,2,2), (2,0,1,6), (2,1,1,7), (2,2,1,8)],
		'b': [(1,6,2,0), (1,7,2,1), (1,8,2,2), (2,0,4,8), (2,1,4,7), (2,2,4,6), 
				(4,8,5,8), (4,7,5,7), (4,6,5,6), (5,8,1,6), (5,7,1,7), (5,6,1,8)]
	}

	reciprocal_move = {
		'L': 'l',
		'l': 'L',
		'M': 'm',
		'm': 'M',
		'R': 'r',
		'r': 'R',
		'U': 'u',
		'u': 'U',
		'E': 'e',
		'e': 'E',
		'D': 'd',
		'd': 'D',
		'F': 'f',
		'f': 'F',
		'S': 's',
		's': 'S',
		'B': 'b',
		'b': 'B'
	}

	# constructor, copy constructor, copy+move constructor:
	def __init__(self, copy_from = None, move = None):
		if (copy_from is None):
			self._data = [[f for i in range(0,9)] for f in range(0,6)]
		else:
			self._data = copy_from.get_data_copy()
		if (move is not None):
			self.move(move)

	def set_cell(self, f, i, new_color):
		self._data[f][i] = new_color

	def is_solved(self):
		return all(self.face_is_solved(face, f) for f, face in enumerate(self._data))

	def face_is_solved(self, face, f):
		c = face[8]
		return all(cell == c for cell in face)

	def get_data_copy(self):
		return [[self._data[f][i] for i in range(0,9)] for f in range(0,6)];

	def data_as_string(self):
		return ''.join([str(i) for f in self._data for i in f])

	def data_as_list(self):
		return [i for f in self._data for i in f]
	
	def move_one(self, code):
		if code in Cube.face_moves:
			self.rotate_face(Cube.face_moves[code], Cube.face_moves_dir[code])
		self.rotate_slice(code)

	def move(self, move_list):
		for code in move_list:
			self.move_one(code)

	# partial move, use only internally:
	def rotate_slice(self, code):
		dataCopy = self.get_data_copy()
		for (f,i,f2,i2) in Cube.rotate_rules[code]:
			self._data[f][i] = dataCopy[f2][i2]

	# partial move, use only internally:
	def rotate_face(self, f, clockwise=1):
		current_face = list(self._data[f]) #copy
		new_face = self._data[f] #pointer
		if ((f != 1 and clockwise == 1) or (f == 1 and clockwise == 0)):
			new_face[0] = current_face[6]
			new_face[1] = current_face[3]
			new_face[2] = current_face[0]
			new_face[3] = current_face[7]
			new_face[5] = current_face[1]
			new_face[6] = current_face[8]
			new_face[7] = current_face[5]
			new_face[8] = current_face[2]
		else:
			new_face[0] = current_face[2]
			new_face[1] = current_face[5]
			new_face[2] = current_face[8]
			new_face[3] = current_face[1]
			new_face[5] = current_face[7]
			new_face[6] = current_face[0]
			new_face[7] = current_face[3]
			new_face[8] = current_face[6]

	def paint_surface(self, ax, face, i, cell_color):
		if (face == 0 or face == 2):
			a = i%3
			b = 2-(i/3)
		if (face == 1 or face == 4):
			a = 2-(i%3)
			b = i/3
		if (face == 3 or face == 5):
			a = i%3
			b = i/3
		
		rng1 = np.arange(a,a+1.25, 0.25)
		rng2 = np.arange(b,b+1.25, 0.25)
		a1, a2 = np.meshgrid(rng1, rng2)
		
		if (face%3 == 0): # f=0,3
			X = a1
			Y = face - (face%3)
			Z = a2
		if (face%3 == 1): # f=1,4
			X = 3 - 3*(face/3)
			Y = a2
			Z = a1
		if (face%3 == 2): #f=2,5
			X = a1
			Y = a2 
			Z = 3 - 3*(face/3)
		
		ax.plot_surface(X, Y, Z, color=Cube.cubecolors[cell_color], shade=False)

	def paint(self):
		# init 3d axis:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		
		# add cube surfaces:
		for f in range(0,6):
			for i in range(0,9):
				self.paint_surface(ax, f, i, self._data[f][i])

		# get rid of the panes
		ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
		ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

		# get rid of the spines
		ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
		ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
		ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

		# get rid of the ticks
		ax.set_xticks([]) 
		ax.set_yticks([]) 
		ax.set_zticks([])
		
		# paint:
		plt.show()
