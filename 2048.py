import pygame as pg
import random as r
import numpy as np

pg.font.init()

class filler:
	def __init__(self):
		self.a = -1
		self.b = -1
		self.value = -1
		self.last = 0
	def update(self):
		pass

class tile:
	def __init__(self, x, y):
		global res
		self.a = x
		self.b = y
		self.x = x * res
		self.y = y * res
		self.value = r.randint(1, 2) * 2
		self.vectors = []
		self.moved = False
		self.last = 0

	def move(self, x, y):
		global res, animation_tick
		# self.a = x
		# self.b = y
		m1 = (x - self.a) / animation_tick * res
		m2 = (y - self.b) / animation_tick * res
		self.a = x
		self.b = y

		#m1, m2 = 0, 0
		self.vectors.append([m1, m2, animation_tick])

	def update(self):
		global res, color, conv
		#self.x = self.a * res
		#self.y = self.b * res

		for i in range(len(self.vectors)):
			elem = self.vectors[i]
			if elem[2] > 0:
				self.vectors[i][2] -= 1
				self.x += elem[0]
				self.y += elem[1]
			else:
				if i in self.vectors:
					self.vectors.remove(i)
				if self in tails:
					tails.remove(self)
		a = res / 20
		pg.draw.rect(scr, color[self.value], (self.x + a, self.y + a, res - a, res - a))
		mod = res / 6 * len(str(self.value)) / 2 
		scr.blit(conv[self.value], (int(self.x + res / 2 - mod), int(self. y + res * 0.4)))
	def get(self):
		return 1



def generate():
	global arr, n, tails
	
	l = []
	for i in range(n):
		for j in range(n):
			if arr[i, j].value == -1:
				l.append([i, j])
			arr[i, j].moved = False
			arr[i, j].last = 0
	if len(l) == 0:
		global cond
		cond = False
		return
	a, b = r.choice(l)
	arr[a, b] = tile(a, b)
	#pr()

def up():
	global arr, tails
	f = False
	for _ in range(4):
		for i in range(1, n):
			for j in range(n):
				if arr[i, j].value != -1:
					if arr[i - 1, j].value == arr[i, j].value:
						if (not arr[i, j].moved) and (not arr[i - 1, j].moved):
							arr[i, j] = filler()
							arr[i - 1, j].value *= 2
							arr[i - 1, j].moved = True
							f = True

					elif arr[i - 1, j].value == -1:
						arr[i, j], arr[i - 1, j] = arr[i - 1, j], arr[i, j]
						arr[i - 1, j].move(i - 1, j)
						f = True
	if f:
		generate()

def left():
	global arr, tails
	f = False
	for _ in range(4):
		for i in range(n):
			for j in range(1, n):
				if arr[i, j].value != -1:
					if arr[i, j - 1].value == arr[i, j].value:
						if (not arr[i, j].moved) and (not arr[i, j - 1].moved):
							f = True
							arr[i, j] = filler()
							arr[i, j - 1].value *= 2
							arr[i, j - 1].moved = True

					elif arr[i, j - 1].value == -1:
						arr[i, j], arr[i, j - 1] = arr[i, j - 1], arr[i, j]
						arr[i, j - 1].move(i, j - 1)
						f = True
	if f:
		generate()

def down():
	global arr, tails
	f = False
	for _ in range(4):
		for i in [*range(n - 1)][::-1]:
			for j in range(n):
				if arr[i, j].value != -1:
					if arr[i + 1, j].value == arr[i, j].value:
						if (not arr[i, j].moved) and (not arr[i + 1, j].moved):
							arr[i, j] = filler()
							arr[i + 1, j].value *= 2
							arr[i + 1, j].moved = True
							f = True

					elif arr[i + 1, j].value == -1:
						arr[i, j], arr[i + 1, j] = arr[i + 1, j], arr[i, j]
						arr[i + 1, j].move(i + 1, j)
						f = True
	if f:
		generate()

def right():
	global arr, tails
	f = False
	for _ in range(4):
		for i in range(n):
			for j in [*range(n - 1)][::-1]:
				if arr[i, j].value != -1:
					if arr[i, j + 1].value == arr[i, j].value:
						if (not arr[i, j].moved) and (not arr[i, j + 1].moved):
							arr[i, j] = filler()
							arr[i, j + 1].value *= 2
							arr[i, j + 1].moved = True
							f = True

					elif arr[i, j + 1].value == -1:
						arr[i, j], arr[i, j + 1] = arr[i, j + 1], arr[i, j]
						arr[i, j + 1].move(i, j + 1)
						arr[i, j + 1].moved = True
						f = True
	if f:
		generate()


n = 5
res = 100
animation_tick = 20
w, h = res * n, res * n
scr = pg.display.set_mode((w, h))
timer = pg.time.Clock()

#font_path = r'C:/Users/neeed/Downloads/Шрифты/Kaorigel-Z9YK.ttf'
Font = pg.font.SysFont('Calibri', res // 3, bold=True)
conv = {}
for i in range(12):
	conv[2 ** i] = Font.render(str(2 ** i), True, (255, 255, 255))
arr = [[filler() for i in range(n)] for j in range(n)]
arr = np.array(arr)
tails = []
cond = True
color = {2 : (238, 228, 218), 4 : (237, 224, 200), 8 : (239, 174, 115), 
16 : (239, 146, 99), 32 : (247, 125, 98), 64 : (247, 97, 65), 128 : (239, 207, 115), 
256 : (239, 202, 98), 512 : (238, 198, 82), 1024 : (238, 198, 65), 
2048 : (238, 194, 49)}



generate()
while cond:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			cond = False
			continue
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_d:
				down()
			elif event.key == pg.K_s:
				right()
			elif event.key == pg.K_a:
				up()
			elif event.key == pg.K_w:
				left()
	for i in range(n):
		for j in range(n):
			arr[i, j].update()
	pg.display.flip()
	timer.tick(60)
	scr.fill((255, 255, 255))

pg.quit()