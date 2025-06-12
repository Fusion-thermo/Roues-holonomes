from tkinter import *
from PIL import Image, ImageTk #attention à l'ordre d'import car tkinter contient aussi Image
import numpy as np
from math import cos, sin, sqrt, pi, asin

class Objectif:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle # angle 0 est la position initiale

def rad(degre):
    return pi*degre/180

def signe(a):
    return a/abs(a)

def Clic_gauche(event):
    print(event.x, event.y)

def deplacement():
    #actuellement pas de vitesse de rotation max
    global xo, yo, x_obj, y_obj, angle, angle_inte, angle_exte, angle_obj, robot, objectif_en_cours, v_const, temps_total, r_roue, x0, y0, r, r_inte
    pas_de_temps = 0.1 #s
    temps_total += pas_de_temps


    #Déterminer le déplacement prévu
    d = sqrt((x_obj-xo)**2 + (y_obj-yo)**2) #distance en pixels entre la position actuelle et la position de l'objectif en cours
    dt = d
    t = d/v_const #temps en s qu'on mettrait pour y aller à cette vitesse constante
    if t > pas_de_temps:#si cela prend plus de temps que le pas de temps de l'affichage alors on va moins loin
        t = pas_de_temps #s
        dt = v_const * t #pixels
    #Déterminer les vitesses du centre du robot et la vitesse angulaire en pixel/s et degré/s
    Vox = abs(x_obj-xo)*(dt/d)/t
    Voy = abs(y_obj-yo)*(dt/d)/t
    omega_z = abs(angle_obj%360 - angle%360)*(dt/d)/t #attention aux modulos de nombres flottants ! # Est-ce la bonne unité ?
    #Déterminer les vitesses forcées des trois roues en pixels/s
    Vaf = 0.5*Vox - sqrt(3)*0.5*Voy - dt*omega_z
    Vbf = 0.5*Vox + sqrt(3)*0.5*Voy - dt*omega_z
    Vcf = -Vox - dt*omega_z
    #Déterminer la vitesse de rotation des moteurs des trois roues en degré/s
    omega_a = (3*873)*Vaf/r_roue
    omega_b = (3*873)*Vbf/r_roue
    omega_c = (3*873)*Vcf/r_roue

    #Calcul des nouvelles coordonnées
    xo += signe(x_obj - xo) * Vox * t
    yo += signe(y_obj - yo) * Voy * t
    delta_angle = signe(angle_obj%360 - angle%360) * omega_z * t # degrés
    angle += delta_angle
    angle_inte += delta_angle
    angle_exte += delta_angle
    print(omega_z,delta_angle,angle,angle_inte,angle_exte)

    #Mettre à jour les coordonnées
    # print("maj")
    Canevas.coords(robot, r*cos(rad(angle)) + xo, r*sin(rad(angle)) + yo, r*cos(rad(120-angle)) + xo, r*sin(rad(120-angle)) + yo, r*cos(rad(120+angle)) + xo, r*sin(rad(120+angle)) + yo, r*cos(rad(-(120+angle))) + xo, r*sin(rad(-(120+angle))) + yo, r*cos(rad(-(120-angle))) + xo, r*sin(rad(-(120-angle))) + yo, r*cos(rad(-angle)) + xo, r*sin(rad(-angle)) + yo)
    Canevas.coords(roue_avant_gauche, r_inte*cos(rad(angle_inte)) + xo, r_inte*sin(rad(angle_inte)) + yo, r_inte*cos(rad(-angle_inte)) + xo, r_inte*sin(rad(-angle_inte)) + yo, r*cos(rad(-angle_exte)) + xo, r*sin(rad(-angle_exte)) + yo, r*cos(rad(angle_exte)) + xo, r*sin(rad(angle_exte)) + yo)
    Canevas.coords(roue_arriere, r_inte*cos(rad(-(120-angle_inte))) + xo, r_inte*sin(rad(-(120-angle_inte))) + yo, r_inte*cos(rad(-(120+angle_inte))) + xo, r_inte*sin(rad(-(120+angle_inte))) + yo, r*cos(rad(-(120+angle_exte))) + xo, r*sin(rad(-(120+angle_exte))) + yo, r*cos(rad(-(120-angle_exte))) + xo, r*sin(rad(-(120-angle_exte))) + yo)
    Canevas.coords(roue_avant_droite, r_inte*cos(rad(120-angle_inte)) + xo, r_inte*sin(rad(120-angle_inte)) + yo, r_inte*cos(rad(120+angle_inte)) + xo, r_inte*sin(rad(120+angle_inte)) + yo, r*cos(rad(120+angle_exte)) + xo, r*sin(rad(120+angle_exte)) + yo, r*cos(rad(120-angle_exte)) + xo, r*sin(rad(120-angle_exte)) + yo)

    recursif = fenetre.after(int(pas_de_temps*1000),deplacement)
    #Si on a atteint l'objectif
    if xo == x_obj and yo == y_obj and angle%360 == angle_obj:
        objectif_en_cours+=1
        #Si on a terminé tous les objectifs
        if objectif_en_cours == len(objectifs):
            print("Fin car tous les objectifs ont été remplis")
            fenetre.after_cancel(recursif)
            return "Fin de la stratégie"
        else:
            x_obj = objectifs[objectif_en_cours].x
            y_obj = objectifs[objectif_en_cours].y
            angle_obj = objectifs[objectif_en_cours].angle
    if temps_total >= 100000: #si plus de 100 secondes
        fenetre.after_cancel(recursif)
        print("Fin au temps")
        return "Fin du temps"


#Tkinter
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

#Robot avec polygone, bonnes proportions par rapport au plateau
# Construction autour de 0,0
r = (275+64/2)/sqrt(3) #rayon en mm
r_inte = r-26 #inte et exte font référence au diamètre des sommets des roues, avec r_exte = r
angle = asin(32/r)*180/pi #degré
angle_exte = asin(29/r)*180/pi #degré
angle_inte = asin(29/r_inte)*180/pi #degré
r *= 873/3000 #rayon en pixels : 3000 mm de plateau réels correspondent ici à 873 pixels
r_inte *= 873/3000 #rayon en pixels
x0, y0 = 99, 338
robot = Canevas.create_polygon(r*cos(rad(angle)) + x0, r*sin(rad(angle)) + y0, r*cos(rad(120-angle)) + x0, r*sin(rad(120-angle)) + y0, r*cos(rad(120+angle)) + x0, r*sin(rad(120+angle)) + y0, r*cos(rad(-(120+angle))) + x0, r*sin(rad(-(120+angle))) + y0, r*cos(rad(-(120-angle))) + x0, r*sin(rad(-(120-angle))) + y0, r*cos(rad(-angle)) + x0, r*sin(rad(-angle)) + y0, fill="black")
roue_avant_gauche = Canevas.create_polygon(r_inte*cos(rad(angle_inte)) + x0, r_inte*sin(rad(angle_inte)) + y0, r_inte*cos(rad(-angle_inte)) + x0, r_inte*sin(rad(-angle_inte)) + y0, r*cos(rad(-angle_exte)) + x0, r*sin(rad(-angle_exte)) + y0, r*cos(rad(angle_exte)) + x0, r*sin(rad(angle_exte)) + y0, fill="green")
roue_arriere = Canevas.create_polygon(r_inte*cos(rad(-(120-angle_inte))) + x0, r_inte*sin(rad(-(120-angle_inte))) + y0, r_inte*cos(rad(-(120+angle_inte))) + x0, r_inte*sin(rad(-(120+angle_inte))) + y0, r*cos(rad(-(120+angle_exte))) + x0, r*sin(rad(-(120+angle_exte))) + y0, r*cos(rad(-(120-angle_exte))) + x0, r*sin(rad(-(120-angle_exte))) + y0, fill="red")
roue_avant_droite = Canevas.create_polygon(r_inte*cos(rad(120-angle_inte)) + x0, r_inte*sin(rad(120-angle_inte)) + y0, r_inte*cos(rad(120+angle_inte)) + x0, r_inte*sin(rad(120+angle_inte)) + y0, r*cos(rad(120+angle_exte)) + x0, r*sin(rad(120+angle_exte)) + y0, r*cos(rad(120-angle_exte)) + x0, r*sin(rad(120-angle_exte)) + y0, fill="blue")
# roues = [roue_avant_gauche, roue_avant_droite, roue_arriere]

#Stratégie
objectifs=[Objectif(249,507,60)]

#Paramètres
v_const = 80 #vitesse constante du robot : 80 pixels/s
objectif_en_cours = 0 #indice de l'objectif en cours dans la liste
x_obj = objectifs[objectif_en_cours].x
y_obj = objectifs[objectif_en_cours].y
angle_obj = objectifs[objectif_en_cours].angle
xo, yo, angle = x0, y0, 0
temps_total = 0
r_roue = 0.058 #m






Canevas.bind('<Button-1>',  Clic_gauche)

deplacement()

fenetre.mainloop()