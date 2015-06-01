__author__ = 'Vlasev'

X = 15
m = 15
n = 20
N = 30

from random import randrange
from prettytable import PrettyTable

faces = {'unexplored': '#', 'flagged': 'F', 'mine': 'X', '0': ' ', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
		 '6': '6', '7': '7', '8': '8'}

class Box(object):

	size = X

	def __init__(self, x_pos, y_pos, has_mine=False, has_flag=False, pressed=False, covered=False, neighboring_mines=0):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.has_mine = has_mine
		self.has_flag = has_flag
		self.pressed = pressed
		self.covered = covered
		self.neighboring_mines = neighboring_mines

	def place_mine(self):
		self.has_mine = True

	def place_flag(self):
		self.has_mine = True

	def count_mines(self):
		for box in self.neighbors():
			if box.has_mine:
				self.neighboring_mines += 1

	def get_neighbors(self):
		return []

	def get_face(self):
		if self.has_flag:
			return faces['flagged']
		elif self.covered:
			return faces['unexplored']
		elif self.has_mine:
			return faces['mine']
		else:
			return faces[str(self.neighboring_mines)]

	def press(self):
		if not self.pressed and not self.has_flag:
			self.covered = False
			if self.has_mine:
				return False
			else:
				return True


class Field(object):

	def __init__(self, height, width, num_mines):
		self.height = height
		self.width = width
		self.num_mines = num_mines
		self.field = self.generate_boxes()

	def generate_boxes(self):
		return [[Box(i, j) for j in range(0, self.width)] for i in range(0, self.height)]

	def place_mines(self):
		remaining = [[i, j] for j in range(0, self.width) for i in range(0, self.height)]
		for k in range(0, self.num_mines):
			num = randrange(0, len(remaining))
			x_pos = remaining[num][0]
			y_pos = remaining[num][1]
			self.field[x_pos][y_pos].place_mine()
			# print("Placing a mine on {}, {}".format(x_pos, y_pos))
			remaining.pop(num)

	def update_neighboring_mines(self):
		for i in range(0, self.height):
			for j in range(0, self.width):
				count = 0
				for t in range(-1, 2):
					for s in range(-1, 2):
						if -1 < i + t < self.height and -1 < j + s < self.width:
							if self.field[i + t][j + s].has_mine:
								count += 1
				self.field[i][j].neighboring_mines = count

	def get_field_faces(self):
		field_faces = []
		for row in self.field:
			temp = []
			for box in row:
				temp.append(box.get_face().rjust(2))
			field_faces.append(temp)
		return field_faces

	def print_field(self):
		top_cells = ['  '] + [str(x).rjust(3, 'c') for x in range(1, self.width + 1)]
		side_cells = [str(x).rjust(3, 'r') for x in range(1, self.height + 1)]
		table = PrettyTable(top_cells)
		table.hrules = True
		table.align = "c"
		# table.border = False
		field_faces = self.get_field_faces()
		for i in range(0, m):
			table.add_row([side_cells[i]]+field_faces[i])
		print(table)




if __name__ == '__main__':
	game = Field(m, n, N)
	# game.print_field()
	game.place_mines()
	game.update_neighboring_mines()
	game.print_field()
