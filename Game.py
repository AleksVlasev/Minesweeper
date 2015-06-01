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

	def __init__(self, x_pos, y_pos, has_mine=False, has_flag=False, pressed=False, covered=True, neighboring_mines=0):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.has_mine = has_mine
		self.has_flag = has_flag
		self.pressed = pressed
		self.covered = covered
		self.neighboring_mines = neighboring_mines

	def place_mine(self):
		self.has_mine = True

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
			self.pressed = True
			self.covered = False
			if self.has_mine:
				print("Yikes, you uncovered a mine. BOOM!")
				return False
			else:
				return True

	def place_flag(self):
		if not self.pressed:
			self.covered = False
			self.has_flag = True
		else:
			print("Oops, you've already selected this cell")


class Field(object):

	def __init__(self, height, width, num_mines):
		self.height = height
		self.width = width
		self.num_mines = num_mines
		self.field = self.generate_boxes()

	def generate_boxes(self):
		return [[Box(i, j) for j in range(0, self.width)] for i in range(0, self.height)]

	def place_mines(self, x, y):
		remaining = [[i, j] for j in range(0, self.width) for i in range(0, self.height)]
		remaining.pop(remaining.index([x, y]))
		self.field[x][y].covered = False
		self.field[x][y].pressed = True
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
		table.border = False
		field_faces = self.get_field_faces()
		for i in range(0, self.height):
			table.add_row([side_cells[i]]+field_faces[i])
		print(table)

def choose(string, cond=(lambda x: False), values=[]):
	chosen = False
	while not chosen:
		answer = input(string)
		if answer in values or map(cond, answer):
			chosen = True
	return answer

def between(expression, X, Y):
	if X <= expression <= Y:
		return True
	else:
		return False

def choose_range(string="a number", X=0, Y=1):
	return choose("Input {} between {} and {}: ".format(string, X, Y), (lambda x: between(x, X, Y)))



if __name__ == '__main__':
	# height = int(choose_range("height", 5, 20))
	# width = int(choose_range("width", 5, 20))
	# num_mines = int(choose_range("number of mines", 1, height * width - 1))
	# print("Initializing...")
	height = 10
	width = 10
	num_mines = 20
	game = Field(height, width, num_mines)

	print("Please input the first cell you will play")
	i_play = int(choose_range("row number", 1, height)) - 1
	j_play = int(choose_range("column number", 1, width)) - 1
	# game.print_field()
	game.place_mines(i_play, j_play)
	game.update_neighboring_mines()

	win_condition = True
	while win_condition:
		print("\n")
		game.print_field()
		ans = choose("\nSelect cell (s) or flag it (f):", values=['s', 'f'])
		i_play = int(choose_range("row number", 1, height)) - 1
		j_play = int(choose_range("column number", 1, width)) - 1
		if ans == 's':
			win_condition = game.field[i_play][j_play].press()
		else:
			game.field[i_play][j_play].place_flag()

