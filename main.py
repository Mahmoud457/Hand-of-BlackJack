import random
from tkinter import *
import os, os.path
from PIL import Image, ImageTk
class Card:
    def __init__(self, value, suit, image, points):
        self.value = value
        self.suit = suit
        self.image = image
        self.points = points
    def show(self):
        print("{} of {} in {} points are {}".format(self.value, self.suit, self.image, self.points))
    def imgshow(self, x, y, placement):
        img = Image.open(self.image)
        img = img.resize((82,125))
        photoImg = ImageTk.PhotoImage(img)
        cimg = Label(placement, image = photoImg)
        cimg.image = photoImg
        cimg.grid(column=x, row= y, padx=5, pady=5)
    def point(self):
        return self.points
class Deck:
    def __init__(self):
        self.cards = []
        self.build()


    def build(self):
        self.imglist = []
        self.p = 0
        self.path = r"FILE LOCATION HERE"  #Enter file path for cards
        for f in os.scandir(self.path):
            if ".png" in f.name:
                self.imglist.append(f.name)
        self.imglist.sort(key=takef)
        for v in range(1, 14):
            for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
                if v > 10:
                    o = 10
                else:
                    o = int(v)
                self.cards.append(Card(v, s, self.imglist[self.p], o))
                self.p += 1
    def show(self):
        for c in self.cards:
            c.show()
    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
    def draw(self):
        return self.cards.pop()
def takef(elem):
    if elem[1] in ["0", "1", "2", "3"]:
        return int(elem[0:2])
    else:
        return int(elem[0])
class Player:
    def __init__(self, hplace, name):
        self.s=0
        self.hand = []
        self.name = name
        self.phand = LabelFrame(win, text=self.name, padx=200, pady=50, bg="green")
        self.phand.pack(side=hplace, padx=10, pady=10)
        self.yturn = True
        self.win = "n"
    def draw(self, deck):
        if self.yturn == True and p2.win != "w":
            self.hand.append(deck.draw())
    def showHand(self):
        self.p=5
        for x in self.hand:
            x.imgshow(self.p, 10, self.phand)
            self.p+=3
    def checkP(self):
        self.min = 0
        self.max = 0
        for x in self.hand:
            if x.point() == 1:
                self.min+=1
                self.max+=11
            else:
                self.min+=x.point()
                self.max+=x.point()
        if self.max and self.min > 21:
            self.win = "b"
            self.yturn = False
            self.endturn()
        elif self.min == 21:
            self.win = "w"
            self.yturn = False
            self.endturn()
        elif self.max == 21:
            self.yturn = False
            self.win = "w"
            self.endturn()
        elif len(self.hand) == 5:
            self.yturn = False
            self.win = "w"
            self.endturn()
        else:
            self.win = "l"
            if self.max < 21:
                self.total = self.max
            else:
                self.total = self.min
    def endturn(self):
        if self.win == "w":
            print(self.name, "win")
        if self.win=="l":
            p2.play()
        elif self.win == "b":
            print(self.name, "bust")
    def play(self):#only for cpu
        if p1.yturn == False and p1.win=="l":
            while True:
                if self.win != "b" and self.win != "w":
                    if self.total < p1.total:
                        self.draw(deck)
                        self.showHand()
                        self.checkP()
                    elif self.total > p1.total and self.total<21:
                        print("House wins")
                        break
                    else:
                        print("draw")
                        break
                else:
                    break

    def e(self):
        self.yturn = False

def turn1():
    for x in range(0, 2):
        p1.draw(deck)
        p1.showHand()
        p2.draw(deck)
        p2.showHand()
    p1.checkP()
    p2.checkP()


deck = Deck()
deck.shuffle()
win = Tk()
p1 = Player(hplace=BOTTOM, name="Player")
p2 = Player(hplace=TOP, name="House")
win.geometry("800x800")
win.title("BlackJack")
win.configure(bg="green")
turn1()
hit = Button(win, text="Hit", command=lambda: [p1.draw(deck), p1.showHand(), p1.checkP()])
hit.config(height= 2, width = 4, bg="yellow")
hit.place(x=50, y=450)
stand = Button(win, text = "Stand", command=lambda: [p1.e(), p1.endturn()])
stand.config(height =2, width = 4, bg ="red")
stand.place(x=100, y=450)
win.mainloop()
