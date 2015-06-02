__author__ = 'Vlasev'

'''I wanted to recreate Minesweeper as an exercise in software engineering and I intended to create a full
GUI but since I don't quite know enough about it, I decided to make a simple command line rendition. While I think
the OOP nature of this implementation is not strictly necessary (we can do things with a nested list too),
it was a fun way to encapsulate the meaning of different parts.

We have the Box class which is basically each cell of the minefield. It contains the information necessary to play the game - 
things like whether the cells is covered (or if we've uncovered it already), whether it has a mine or a flag, etc. Then we
have the Field class that handles the whole minefield as one. It is from here that we actually play the game.

The game itself is played from main which contains statements that direct the flow of the game - picking the dimensions
and number of mines, selecting individual cells, planting flags, etc.
'''

from random import randrange
from prettytable import PrettyTable

faces = {'covered': '#', 'flagged': 'F', 'mine': 'X', '0': ' ', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
		 '6': '6', '7': '7', '8': '8'}

class Box(object):

	def __init__(self, x_pos, y_pos, has_mine=False, has_flag=False, covered=True, neighboring_mines=0):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.has_mine = has_mine
		self.has_flag = has_flag
		self.covered = covered
		self.neighboring_mines = neighboring_mines

	def place_mine(self):
		self.has_mine = True

	def get_face(self, par=0):
		'''For the most part we need par=0 but for the LOSE screen we need par=1.
		When par=1 we draw flags, mines and only then numbers of neighboring mines etc'''
		if par == 0:
			if self.has_flag:
				return faces['flagged']
			elif self.covered:
				return faces['covered']
			elif self.has_mine:
				return faces['mine']
			else:
				return faces[str(self.neighboring_mines)]
		if par == 1:
			if self.has_flag:
				return faces['flagged']
			elif self.has_mine:
				return faces['mine']
			elif self.covered:
				return faces['covered']
			else:
				return faces[str(self.neighboring_mines)]

	def uncover(self, count):
		'''if the cell is covered and doesn't have a flag, uncover it and if it has a mine, go boom!'''
		if self.covered and not self.has_flag:
			self.covered = False
			if self.has_mine:
				print("Yikes, you uncovered a mine. BOOM!")
				return False, count
			else:
				return True, count - 1
		'''if the cell has a flag we don't actually uncover the cell'''
		elif self.has_flag:
			print("You cannot press because there is a flag here!")
			return True, count
		'''similarly for uncovered cells'''
		else:
			# print("Oops, you have already uncovered this box!")
			return True, count

	def place_flag(self):
		if self.covered:
			self.has_flag = not self.has_flag
		else:
			# print("Oops, you have already uncovered this box")
			return count


class Field(object):

	def __init__(self, height, width, num_mines):
		self.height = height
		self.width = width
		self.num_mines = num_mines
		self.field = self.generate_boxes()

	def generate_boxes(self):
		return [[Box(i, j) for j in range(0, self.width)] for i in range(0, self.height)]
	
	'''This function makes sure that when we click for the first time at position (x, y) there 
	are no mines there. The minefield is generated only after we've uncovered a cell.'''
	def place_mines(self, x, y):
		remaining = [[i, j] for j in range(0, self.width) for i in range(0, self.height)]
		remaining.pop(remaining.index([x, y]))
		self.field[x][y].covered = False
		for k in range(0, self.num_mines):
			num = randrange(0, len(remaining))
			x_pos = remaining[num][0]
			y_pos = remaining[num][1]
			self.field[x_pos][y_pos].place_mine()
			# print("Placing a mine on {}, {}".format(x_pos, y_pos))
			remaining.pop(num)

	'''this function goes through a cell's neighbors to find if they have mines. IMHO this function
	is rather ugly and needs a rewrite.'''
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
	
	'''This function looks at the faces of all the boxes on each turn in order to print them. It
	can obviously be improved as to update some list of faces somewhere so we don't have to resample
	all of them on every turn.'''
	def get_field_faces(self, par=0):
		field_faces = []
		for row in self.field:
			temp = []
			for box in row:
				temp.append(box.get_face(par).rjust(2))
			field_faces.append(temp)
		return field_faces

	'''This function prints a nice representation of the field with prettytable'''
	def print_field(self, par=0):
		top_cells = ['  '] + [str(x).rjust(3, 'c') for x in range(1, self.width + 1)]
		side_cells = [str(x).rjust(3, 'r') for x in range(1, self.height + 1)]
		table = PrettyTable(top_cells)
		table.hrules = True
		table.align = "c"
		# table.border = False
		field_faces = self.get_field_faces(par)
		for i in range(0, self.height):
			table.add_row([side_cells[i]]+field_faces[i])
		print(table)
	
	'''This function contains the recursive logic of uncovering a box. If the box is all good, we
	didn't step on a mine and the box has zero neighboring mines, then we recursively uncover 
	the neighboring boxes too until we uncover boxes with neighboring mines.'''
	def play_box(self, i, j, count, visited):
		try:
			temp = count
			# print(temp)
			win = True
			# print('entering {} and {}, having visited {}'.format(i, j, visited))
			if [i, j] not in visited:
				if 0 <= i <= self.height - 1 and 0 <= j <= self.width - 1:
					box = self.field[i][j]
					if not box.covered:
						return win, temp
					else:
						win, temp = box.uncover(count)
						visited.append([i, j])
						if win and box.neighboring_mines == 0:
							win, temp = self.play_box(i - 1, j, temp, visited)
							win, temp = self.play_box(i + 1, j, temp, visited)
							win, temp = self.play_box(i, j - 1, temp, visited)
							win, temp = self.play_box(i, j + 1, temp, visited)
						return win, temp
				else:
					# print("Out of bounds sucka!")
					return win, temp
			else:
				return win, temp
		except TypeError:
			print("Type Error at ({}, {}) while we have visited {} so far".format(i, j, visited))

'''Repeatedly ask for an input among certain values until it is given.'''
def choose_values(string, values=[]):
	chosen = False
	while not chosen:
		answer = input(string)
		if answer in values:
			chosen = True
	return answer

'''Repeatedly ask for an input between chosen values x and y where x < y.'''
def choose_range(string="a number", x=0, y=1):
	chosen = False
	while not chosen:
		num = int(input("Input {} between {} and {}: ".format(string, x, y)))
		if x <= num <= y:
			chosen = True
	return num

if __name__ == '__main__':
	height = int(choose_range("height", 5, 10))
	width = int(choose_range("width", 5, 20))
	num_mines = int(choose_range("number of mines", 1, height * width - 1))
	print("Initializing...")
	# height = 10
	# width = 20
	# num_mines = 10
	game = Field(height, width, num_mines)

	print("Please input the first cell you will play")
	i_play = int(choose_range("row number", 1, height)) - 1
	j_play = int(choose_range("column number", 1, width)) - 1
	# game.print_field()
	count = height * width-1
	win_condition = True
	game.place_mines(i_play, j_play)
	game.update_neighboring_mines()
	win_condition, count = game.play_box(i_play, j_play, count, [])

	while win_condition and count > num_mines:
		# print("the count is: {}".format(count))
		print("\n")
		game.print_field()
		ans = choose_values("\nSelect cell (s) or flag it (f): ", ['s', 'f'])
		i_play = int(choose_range("row number", 1, height)) - 1
		j_play = int(choose_range("column number", 1, width)) - 1
		if ans == 's':
			visited = []
			win_condition, count = game.play_box(i_play, j_play, count, [])
		else:
			game.field[i_play][j_play].place_flag()
	if win_condition:
		game.print_field()
		input("\nYou have won! Press any key to exit")
	else:
		game.print_field(1)
		input("\nYou have lost. Press any key to exit")

