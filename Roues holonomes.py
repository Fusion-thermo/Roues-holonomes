from tkinter import *
from PIL import Image, ImageTk #attention à l'ordre d'import car tkinter contient aussi Image
import numpy as np
from math import cos, sin, sqrt, pi

def rad(degre):
    return pi*degre/180

def Clic_gauche(event):
    print(event.x, event.y)

def deplacement():
    global x, alpha, robot, resized_image_robot

    x+=10
    alpha+=10

    Canevas.coords(robot,x,x)

    fenetre.after(500,deplacement)


hauteur,largeur=769, 1000

fenetre=Tk()
fenetre.title("")

Canevas=Canvas(fenetre,height=hauteur,width=largeur)
Canevas.pack()

#Plateau
image = Image.open("C:/Users/jeanb/OneDrive/Documents/Python/Tkinter codes/Roues-holonomes/plateau de départ.png")  # Replace with your image file path
resized_image = image.resize((largeur,hauteur))
img = ImageTk.PhotoImage(resized_image)
plateau = Canevas.create_image( 0, 0, image = img, anchor = "nw")

#Robot avec image : pas possible pour une image de tourner
# image_robot = Image.open("C:/Users/jeanb/OneDrive/Documents/Python/Tkinter codes/Roues-holonomes/vue grand robot.png")  # Replace with your image file path
# resized_image_robot = image_robot.resize((100,100))
# rotated_image_robot = resized_image_robot.rotate(90)
# img_robot = ImageTk.PhotoImage(rotated_image_robot)
# robot = Canevas.create_image( 50, 50, image = img_robot)

#Robot avec polygone, vraies dimensions
# Construction autour de 0,0
r = (275+64/2)/sqrt(3) #rayon en mm
r = r*1 #rayon en pixels
robot = Canevas.create_polygon(r*cos(rad(10.4)), r*sin(rad(10.4)), r*cos(rad(109.6)), r*sin(rad(109.6)), r*cos(rad(130.4)), r*sin(rad(130.4)), r*cos(rad(-130.4)), r*sin(rad(-130.4)), r*cos(rad(-109.6)), r*sin(rad(-109.6)), r*cos(rad(-10.4)), r*sin(rad(-10.4)), fill="grey")
#Position et orientation correcte

Canevas.bind('<Button-1>',  Clic_gauche)



# deplacement()

fenetre.mainloop()