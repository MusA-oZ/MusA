from tkinter import *
from random import randrange

#############################
#                           #
#        Fonctions :        #
#                           #
#############################

def move():
    global x1, y1, dx, dy, flag
    x1, y1 = x1 + dx, y1 + dy
    if direction  == 'gauche':
        x1  = x1 - dx
    if direction  == 'droite':
        x1  = x1 + dx
    if y1 >470:
        y1, dx, dy = 470, -15, 0
    if x1 <10:
        x1, dx, dy = 10, 0, -15
    if y1 <10:
        y1, dx, dy = 10, 15, 0
    can.coords(rectangle, x1, y1, x1 + 10, y1 + 10)
    if flag >0:
        fen.after(70, move)

def start_it():
    global flag
    if flag ==0:
        flag =1
    move()

def newGame():
    pX = randrange(5,495)
    pY = randrange(5,495)
    can.create_oval(pX, pY, pX + 5, pY + 5, outline = 'white', fill = 'green')
    move()
    start_it()

def avance(gd, hb):
    global x1, y1
    x1, y1 = x1 + gd, y1 + hb
    can1.coords(oval1, x1,y1, x1+30,y1+30)

def left(event):
    direction = 'gauche'

def right(event):
    direction = 'droite'

def up(event):
    direction = 'haut'

def down(event):
    avance(0, 10)

#######################################
#                                     #
#        Programme principal :        #
#                                     #
#######################################

x1 = 245
y1 = 245
dx, dy = 15, 0
flag = 0
direction = ''


fen = Tk()
can = Canvas(fen, width = 500, height = 500, bg = '#046380')
can.pack(side = TOP, padx = 5, pady = 5)
rectangle = can.create_rectangle(x1, y1, x1 + 10, y1 + 10, outline = 'white', fill = '#C03000')
b1 = Button(fen, text = 'New Game', command = newGame)
b1.pack(side = LEFT, padx  = 5, pady = 5)
b2 = Button(fen, text = 'Quitter', command = fen.destroy)
b2.pack(side = RIGHT, padx = 5, pady  = 5)
b3 = Button(fen, text = 'Scores')
b3.pack(side = RIGHT, padx = 5, pady = 5)
tex1 = Label(fen, text='Cliquez sur \'New Game\' pour commener.', fg='#333333')
tex1.pack(padx = 0, pady = 11)
fen.bind('<Right>', right)
fen.bind('<Left>', left)
fen.bind('<Up>' , up)
fen.bind('<Down>', down)
fen.mainloop()