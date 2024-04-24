from tkinter import *
from time import sleep, time
from random import randint

def up(event):
    global direction,diri,a
    if diri != 'd':
        direction = [0, -20]
        diri = 'u'
        move()
        a = 1
def down(event):
    global direction, diri,a
    if diri != 'u':
        direction = [0, 20]
        diri = 'd'
        move()
        a = 1
def left(event):
    global direction, diri,a
    if diri != 'r':
        direction = [-20, 0]
        diri = 'l'
        move()
        a = 1
def right(event):
    global direction, diri,a
    if diri != 'l':
        direction = [20, 0]
        diri = 'r'
        move()
        a = 1
    
def food_gen():
     global snake
     x = randint(0,19) * 20
     y = randint(0,19) * 20
     return [x, y]

def pr():
    global snake, items
    global food_pos
    n = len(snake)
    for i in range(1,n+1):
        canvas.coords(items[-i], snake[-i][0], snake[-i][1], snake[-i][0] + 20, snake[-i][1] + 20)
    canvas.coords(food, food_pos[0], food_pos[1], food_pos[0] + 20, food_pos[1] + 20)

def die():
    pass
    global d
    canvas['bg'] = 'grey'
    d = True

def move():
    global snake, items
    global food_pos
    n = len(snake)
    for i in range(1,n):
        snake[-i][0] = snake[-i-1][0]
        snake[-i][1] = snake[-i-1][1]
    snake[0][0] = snake[1][0] + direction[0]
    snake[0][1]= snake[1][1] + direction[1]
    if snake[0][0] < 0 or snake[0][0] > 390 or snake[0][1] < 0 or snake[0][1] > 390:
        return die()
    if snake[0][0] == food_pos[0] and snake[0][1] == food_pos[1]:
        snake.append([snake[-1][0], snake[-1][1]])
        items.append (canvas.create_rectangle (snake[-1][0], snake[-1][1], snake[-1][0] + 20, snake[-1][1] + 20, fill = 'white'))#,outline = 'white'))
        for i in range(100):
            x,y = food_gen()
            if not [x, y] in snake:
                break
            if i == 99:
                return die()
        food_pos = [x,y]

def clear():
    global snake, a,d, root, canvas, items, diri, direction, food, food_pos
    colors =['orange','brown']
    s = 0
    for elem in items:
        canvas.delete(elem)
        canvas['bg'] = colors[s]
        canvas.update()
        s = (s +1)%2
        sleep(0.12)
    items = []
    snake = [[0,0],[-1,0]]
    items.append (canvas.create_rectangle (snake[0][0], snake[0][1], snake[0][0] + 20, snake[0][1] + 20, fill = 'white'))#, outline = 'white'))
    items.append (canvas.create_rectangle (snake[-1][0], snake[-1][1], snake[-1][0] + 20, snake[-1][1] + 20, fill = 'white'))#, outline = 'white')) 
    canvas.delete(food)
    food_pos = food_gen()
    food = canvas.create_rectangle(food_pos[0], food_pos[1], food_pos[0] + 20, food_pos[1] + 20, fill = 'red')#, outline = 'red')
    a = 1
    d = False
    diri = 'r'
    direction = [20,0]
    canvas['bg'] = 'black'
    
def game ():
    global snake, a,d, root, canvas, items, diri, direction, food, food_pos, best, wait
    diction = {1:'a', 2:'w', 3:'d', 4:'s'}
    d = False
    while d == False:
        if a == 0:
            move()
        else: a = 0
        if snake[0] in snake[1:]:
            die()
        pr()
        root.update()
        sleep(0.13)
        l['text'] =  f' result: {len(snake)}'
        if len(snake) > best:
            best = len(snake)
            res['text'] = f'Your Best: {best}'     
    clear()
    canvas.update()

snake = []
direction = [20,0]
diri = 'r'
items = []
d = False
a = 1
best = 0

root = Tk()
root.geometry('400x425')
root['bg'] = 'black'
canvas = Canvas(root, width = 400, height = 400, bg = 'black')
canvas.pack()
pri = Label(root, text = 'Управление через W A S D', font = 'Calibri 17', fg = 'orange', bg = 'black')
pri.place(x = 67, y = 200)
sn = Label(root, text = 'SNAKE', font = 'Calibri 45', fg = 'snow', bg = 'black')
sn.place(x = 110, y = 80)
qwer = Label(root, text = '2020', font = 'Calibri 17', fg = 'grey', bg = 'black')
qwer.place(x = 170, y = 390)
root.update()
sleep(8)
qwer.destroy()
pri.destroy()
sn.destroy()
root['bg'] = 'snow'
food_pos = 0
food = 0
root.title('Snake')
l = Label(root, text = f' result: {len(snake)}', font = 'Calibri 11')
res = Label(root, text = f'Your Best: {best}', font = 'Calibri 11')

l.place(x =172, y = 402)
res.place(x = 0, y = 402)

root.bind(f'<w>', up)
root.bind(f'<s>', down)
root.bind(f'<a>', left)
root.bind(f'<d>', right)
root.bind(f'<W>', up)
root.bind(f'<S>', down)
root.bind(f'<A>', left)
root.bind(f'<D>', right)

clear()
while True:
    game()
    sleep(2.5)
