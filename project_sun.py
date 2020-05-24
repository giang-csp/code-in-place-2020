
import tkinter
import time
import random

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk
from PIL import Image


CANVAS_WIDTH = 1366
CANVAS_HEIGHT = 768
SUN_DIMENSION = 40
SUN_START_POSITION = CANVAS_HEIGHT / 2 - SUN_DIMENSION // 2
BLOCK_WIDTH = 40
BLOCK_DISTANCE = SUN_DIMENSION * 3
X_1ST_BLOCK = 100
CHANGE_X = 5
CHANGE_Y = 5
RIBBON_WIDTH = CANVAS_WIDTH
RIBBON_HEIGHT = 150


y1_list = []
for i in range(CANVAS_HEIGHT):
    if i == 0:
        for j in range(5):
            y1_list.append(i)
    if CANVAS_HEIGHT // 4 <= i <= CANVAS_HEIGHT //1.5 and i % 50 == 0:
        y1_list.append(i)

def main():

    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Adventure of the Sun _by Giang_')

    '''
    Step 1: create world of blocks
    (x1, y1) = coordinate of top left of a block
    (x2, y2) = coordinate of bottom right of a block
    '''
    for i in range(int((CANVAS_WIDTH - SUN_DIMENSION) // BLOCK_DISTANCE)):
        x1 = X_1ST_BLOCK + BLOCK_DISTANCE * i
        x2 = x1 + BLOCK_WIDTH

        # set y1 and y2
        y1 = get_y1(y1_list)
        if y1 == 0:
            y2 = y1 + random.randint(CANVAS_HEIGHT // 4, CANVAS_HEIGHT // 2)
            print(y1, y2)
        else:
            y2 = CANVAS_HEIGHT
        block = canvas.create_rectangle(x1, y1, x2, y2, fill='medium turquoise', outline='medium turquoise')

    '''
    Step 2: create the sun and preparation process
    '''
    image = ImageTk.PhotoImage(Image.open("small_sun.png"))
    sun = canvas.create_image(0, SUN_START_POSITION, anchor="nw", image=image)

    for i in range(3):
        i = 3 - i
        count_down(i, canvas)
    ready = canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, anchor='center', font='Courier 100', text='READY!')
    canvas.update()
    time.sleep(1)
    canvas.delete(ready)

    '''
    Step 3: the sun can flyyyyyy
    '''
    while True:
        canvas.move(sun, CHANGE_X, CHANGE_Y)
        coord_list = canvas.coords(sun)

        # when the sun reaches the right-end of the canvas => the game finishes.
        if coord_list[0] > CANVAS_WIDTH - SUN_DIMENSION:
            ribbon(canvas)
            canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, anchor='center', font='Courier 70', text='Congrats! You Win! >:D<')
            break

        # when the bird reaches the bottom-end of the canvas => the game is over.
        if coord_list[1] > CANVAS_HEIGHT - SUN_DIMENSION:
            ribbon(canvas)
            canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, anchor='center', font='Courier 70', text='Game Over!')
            break

        mouse_y = canvas.winfo_pointery()
        canvas.moveto(sun, coord_list[0], mouse_y)

        # when the bird hits the block => the game is over
        if hit_block(canvas, block, sun):
            ribbon(canvas)
            canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, anchor='center', font='Courier 70', text='Game Over :(')
            break

        canvas.update()
        time.sleep(1/40)
    canvas.mainloop()

'''
Supporting defs
'''

def get_y1(y1_list):
    length = int(len(y1_list))
    length -= 1
    index = random.randint(0, length)
    y1 = y1_list[index]
    y1 = int(y1)
    return y1

def ribbon(canvas):
    ribbon = canvas.create_rectangle(0, CANVAS_HEIGHT//2 - RIBBON_HEIGHT//2, CANVAS_WIDTH, CANVAS_HEIGHT//2 + RIBBON_HEIGHT//2, fill='light salmon', outline='light salmon')
    return ribbon

def count_down(number,canvas):
    number = str(number)
    create_rib = ribbon(canvas)
    count_down = canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, anchor='center', font='Courier 70', text=number)
    canvas.update()
    time.sleep(1)
    canvas.delete(count_down)
    canvas.delete(create_rib)


def hit_block(canvas, block, sun):
    bird_coords = canvas.coords(sun)
    x1 = bird_coords[0]
    y1 = bird_coords[1]
    x2 = bird_coords[0] + SUN_DIMENSION
    y2 = bird_coords[1] + SUN_DIMENSION
    results = canvas.find_overlapping(x1, y1, x2, y2)
    return len(results) > 1

def mouse_moved(event):
    print('x = ' + str(event.x), 'y = ' + str(event.y))

def make_canvas(width, height, title=None):
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()

    canvas.bind("<Motion>", mouse_moved)
    return canvas
    pass

if __name__ == '__main__':
    main()