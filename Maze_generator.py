import pygame as pg
from random import *
pg.init()
w, h = int(450), int(450)
sc = pg.display.set_mode((w, h))
size = 20
col, row = w // size, h // size
tiles = []

class Stack:
    def __init__(self):
        self.stack = []

    def put(self, obj):
        self.stack.append(obj)

    def take(self):
        if len(self.stack):
            a = self.stack[-1]
            self.stack.pop(-1)
            return a
        return (0, 0)
    
class tile:
    def __init__(self, x, y):
        global col, row
        self.x = x
        self.y = y
        self.nb = [0, 1, 2, 3]
        if x == 0:
            self.nb.remove(3)
        if x == col - 1:
            self.nb.remove(1)
        if y == 0:
            self.nb.remove(0)
        if y == row - 1:
            self.nb.remove(2)
        self.visited = False
        self.walls = [0, 1, 2, 3]
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        #self.color = (50, 50, 50)
        
    def draw(self):
        global size, col, rows
        if not self.visited:
            pg.draw.rect(sc, self.color, (self.x * size, self.y * size,\
                size, size))
            
        if 0 in self.nb:
            pg.draw.line(sc, (255, 100, 100), (self.x * size, self.y * size),\
                ((self.x + 1) * size, self.y * size))
            
        if 1 in self.nb:
            pg.draw.line(sc, (255, 100, 100), ((self.x + 1) * size, self.y * size),\
                ((self.x + 1) * size, (self.y + 1) * size))
            
        if 2 in self.nb:
            pg.draw.line(sc, (255, 100, 100), (self.x * size, (self.y + 1) * size),\
                ((self.x + 1) * size, (self.y + 1) * size))
            
        if 3 in self.nb:
            pg.draw.line(sc, (255, 100, 100), (self.x * size, self.y * size),\
                (self.x * size, (self.y + 1) * size))

    def visit(self):
        self.visited = True

    def remove(self, wall):
        self.walls.remove(wall)
        self.nb.remove(wall)

tiles = [[tile(j, i) for i in range(row)] for j in range(col)]
cond = True
#current = (col // 2, row // 2)
current = (col // 2, row // 2)
#  ||  0 ||  r
#   3 ##  1  o 
#  ||  2 ||  w
#   c  o  l

timer = pg.time.Clock()
st = Stack()
d = {0 : (0, -1), 1 : (1, 0), 2 : (0, 1), 3 : (-1, 0)}
st.put(current)

def way():
    global st
    for i in range(len(st.stack)- 1):
        elem = st.stack[i]
        #color = ((i * 5) % 255, 100, 255)
        elem1 = st.stack[i + 1]
        pg.draw.line(sc, (255, 255, 255), (int((elem[0] + 0.5) * size), 
            int((elem[1] + 0.5) * size)), (int((elem1[0] + 0.5) * size), 
            int((elem1[1] + 0.5) * size)), 5 )
        
while cond:
    for l in tiles:
        for elem in l:
            elem.draw()
    a = current[0] * size
    b = current[1] * size
    if current == (0, 0) and tiles[-1][-1].visited:
        pg.draw.rect(sc, (255, 0, 0), (0, 0, size, size))
        pg.draw.rect(sc, (0, 255, 0), (w, h, -size, -size))    
    way()
    pg.display.flip()
    tiles[current[0]][current[1]].visit()
    l = []
    
    for elem in tiles[current[0]][current[1]].nb:
        mod1 = d[elem]
        if not tiles[current[0] + mod1[0]][current[1] + mod1[1]].visited:
            l.append(elem)
            
    if len(l):
        a = choice(l)
        mod = d[a]
        tiles[current[0]][current[1]].remove(a)
        tiles[current[0] + mod[0]][current[1] + mod[1]].remove((a + 2) % 4)
        st.put((current[0] + mod[0], current[1] + mod[1]))
        current = (current[0] + mod[0], current[1] + mod[1])
    else:
        current = st.take()
        
    timer.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            cond = False
    sc.fill((0,0,0))
pg.quit()
