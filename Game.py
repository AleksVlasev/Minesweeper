__author__ = 'Vlasev'

X = 15
m = 10
n = 15
N = 20

from random import randrange

faces = {'unexplored': '#', 'flagged': 'F', 'mine': '*', '0': ' ', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
		 '6': '6', '7': '7', '8': '8'}

class Box(object):

	size = X

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

	def place_flag(self):
		self.has_mine = True

	def count_mines(self):
		for box in self.neighbors():
			if box.has_mine:
				self.neighboring_mines += 1

	def neighbors(self):
		return []

	def press(self):
		if not self.pressed and not self.has_flag:
			self.covered = False
			if self.has_mine:
				return False
			else:
				return True


def generate_boxes(m=20, n=10):
	return [[Box(i, j) for j in range(0, n)] for i in range(0, m)]


def place_mines(m, n, N, field):
	remaining = [[i, j] for j in range(0, n) for i in range(0, m)]
	for k in range(0, N):
		num = randrange(0, len(remaining))
		x_pos = remaining[num][0]
		y_pos = remaining[num][1]
		field[x_pos, y_pos].place_mine()
		remaining.pop(num)


def update_neighboring_mines(field):
	for row in field:
		for box in row:
			box.count_mines()



