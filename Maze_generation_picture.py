from tkinter import Tk, Canvas
from random import randint, choice
from time import time
import numpy as np
w,h = 40,40

l = [[0,1], [0,-1], [1,0], [-1,0]]
tiles = [[h//2, w//2], [h//2-1, w//2], [h//2+1, w//2]]
picture = np.zeros((w,h))

for elem in tiles:
    picture[elem[0], elem[1]] = 255

def moving():
    global tiles, l, w, h, picture
    x,y = randint(0,w), randint(0,h)
    while True:
        mod = choice(l)
        a = [(x + mod[0]) % w, (y + mod[1]) % h]
        
        for elem in l:
            b = [a[0] + elem[0], a[1] + elem[1]]
            if b in tiles:
                tiles.append(a)
                picture[a[0],a[1]] = 255
                return None
        x,y = a[0] % w,a[1] % h
                
for _ in range(int( w * h / 3)):
    moving()

from scipy.interpolate import CubicSpline

arr = picture

n = 520
data = np.zeros((n, n))
scl = int(len(data) / len(arr))
for i in range(len(arr)):
    for j in range(len(arr[0])):
        data[i*scl,j*scl] = arr[i,j]
    
    l = list(map( lambda a : a * scl, list(range(len(arr)))))
    l.append(l[-1] + scl)
    l1 = arr[i]
    l1 = np.append(l1, arr[i][0])
    f = CubicSpline(l, l1)
    for j in range(len(data[0])):
        b = f(j)
        b = (b + abs(b))/2 - 255
        b = (b - abs(b))/2 + 255
        data[i*scl,j] = b
        
for j in range(len(data[1])):
    l = list(map( lambda a: a * scl, list(range(len(arr)))))
    l1 = list(map(lambda elem: data[elem,j], l))
    l.append(l[-1] + scl)
    l1.append(data[0,j])
    f = CubicSpline(l, l1)
    for i in range(len(data[0])):
        b = f(i)
        b = (b + abs(b))/2 - 255
        b = (b - abs(b))/2 + 255
        data[i,j] = b

for i in range(n):
    for j in range(n):
        #a = data[i,j] - 25 
        #a = (a + abs(a))/2 + 25
        if data[i,j] >= 128:
            data[i,j] = 255
        else:
            data[i,j] = 0
        #data[i,j] = a

picture = data

img = np.zeros((n,n,3))#w,h,3))
img[:,:,0] = picture
img[:,:,1] = picture
img[:,:,2] = picture

from PIL import Image
img  = Image.fromarray(img.astype('uint8'))
img.save('maze.png')
