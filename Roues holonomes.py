from tkinter import *
from PIL import Image, ImageTk #attention à l'ordre d'import car tkinter contient aussi Image
import numpy as np
from math import cos, sin, sqrt, pi, asin
import time

class Deplacement:
    def __init__(self, x, y, angle, duree_action=2, points=0, desc=""):
        self.x = x
        self.y = y
        self.angle = angle # angle 0 est l'orientation initiale du robot
        self.points=points
        self.description_points = desc
        self.duree_action = duree_action #durée nécessaire pour accomplir l'action
        #Temp pour créer la stratégie :
        self.duree_action = 0.1

def rad(degre):
    return pi*degre/180

def signe(a):
    if a < 0:
        return -1
    else:
        return 1

def Clic_gauche(event):
    global save_x, save_y
    print(event.x, event.y)
    save_x = event.x
    save_y = event.y

def Clic_droit(event):
    global save_x, save_y
    print("diff", event.x-save_x, event.y-save_y)
    save_x = event.x
    save_y = event.y

def deplacement():
    #actuellement pas de vitesse de rotation max
    global xo, yo, x_obj, y_obj, angle, angle_robot, angle_inte, angle_exte, angle_obj, robot, objectif_en_cours, v_const, temps_total, r_roue, x0, y0, r, r_inte, points_total
    pas_de_temps = 0.05 #s
    temps_total += pas_de_temps
    temps.set(str(round(temps_total)) + ' s')


    #Déterminer le déplacement prévu
    d = max(sqrt((x_obj-xo)**2 + (y_obj-yo)**2), 0.0001) #distance en pixels entre la position actuelle et la position de l'objectif en cours
    dt = d
    t = d/v_const #temps en s qu'on mettrait pour y aller à cette vitesse constante
    if t > pas_de_temps:#si cela prend plus de temps que le pas de temps de l'affichage alors on va moins loin
        t = pas_de_temps #s
        dt = v_const * t #pixels
    #Déterminer les vitesses du centre du robot et la vitesse angulaire en pixel/s et degré/s
    Vox = abs(x_obj-xo)*(dt/d)/t
    Voy = abs(y_obj-yo)*(dt/d)/t
    omega_z = abs(angle_obj - angle)*(dt/d)/t #attention aux modulos de nombres flottants ! # Est-ce la bonne unité ?
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
    delta_angle = signe(angle_obj - angle) * omega_z * t # degrés
    angle += delta_angle
    # texte_angle.set(str(round(angle)))

    #Mettre à jour les coordonnées
    Canevas.coords(robot, r*cos(rad(angle_robot+angle)) + xo, r*sin(rad(angle_robot+angle)) + yo, r*cos(rad(120-angle_robot+angle)) + xo, r*sin(rad(120-angle_robot+angle)) + yo, r*cos(rad(120+angle_robot+angle)) + xo, r*sin(rad(120+angle_robot+angle)) + yo, r*cos(rad(-(120+angle_robot-angle))) + xo, r*sin(rad(-(120+angle_robot-angle))) + yo, r*cos(rad(-(120-angle_robot-angle))) + xo, r*sin(rad(-(120-angle_robot-angle))) + yo, r*cos(rad(-angle_robot+angle)) + xo, r*sin(rad(-angle_robot+angle)) + yo)
    Canevas.coords(roue_avant_gauche, r_inte*cos(rad(angle_inte+angle)) + xo, r_inte*sin(rad(angle_inte+angle)) + yo, r_inte*cos(rad(-angle_inte+angle)) + xo, r_inte*sin(rad(-angle_inte+angle)) + yo, r*cos(rad(-angle_exte+angle)) + xo, r*sin(rad(-angle_exte+angle)) + yo, r*cos(rad(angle_exte+angle)) + xo, r*sin(rad(angle_exte+angle)) + yo)
    Canevas.coords(roue_arriere, r_inte*cos(rad(-(120-angle_inte-angle))) + xo, r_inte*sin(rad(-(120-angle_inte-angle))) + yo, r_inte*cos(rad(-(120+angle_inte-angle))) + xo, r_inte*sin(rad(-(120+angle_inte-angle))) + yo, r*cos(rad(-(120+angle_exte-angle))) + xo, r*sin(rad(-(120+angle_exte-angle))) + yo, r*cos(rad(-(120-angle_exte-angle))) + xo, r*sin(rad(-(120-angle_exte-angle))) + yo)
    Canevas.coords(roue_avant_droite, r_inte*cos(rad(120-angle_inte+angle)) + xo, r_inte*sin(rad(120-angle_inte+angle)) + yo, r_inte*cos(rad(120+angle_inte+angle)) + xo, r_inte*sin(rad(120+angle_inte+angle)) + yo, r*cos(rad(120+angle_exte+angle)) + xo, r*sin(rad(120+angle_exte+angle)) + yo, r*cos(rad(120-angle_exte+angle)) + xo, r*sin(rad(120-angle_exte+angle)) + yo)
    Canevas.coords(texte_angle,xo,yo)
    Canevas.itemconfigure(texte_angle, text=str(round(angle)))

    recursif = fenetre.after(int(pas_de_temps*1000),deplacement)
    #Si on a atteint l'objectif
    # print(xo - x_obj, yo - y_obj, angle%360 - angle_obj%360)
    if xo == x_obj and yo == y_obj and angle%360 == angle_obj%360:
        time.sleep(objectifs[objectif_en_cours].duree_action)
        temps_total += objectifs[objectif_en_cours].duree_action
        if objectifs[objectif_en_cours].points >0:
            points_total += objectifs[objectif_en_cours].points
            texte_points.set(str(points_total)+" points. +"+str(objectifs[objectif_en_cours].points)+" : "+objectifs[objectif_en_cours].description_points)
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
    if temps_total >= 100: #si plus de 100 secondes
        fenetre.after_cancel(recursif)
        print("Fin au temps")
        return "Fin du temps"


#Tkinter
hauteur,largeur=769, 1000

fenetre=Tk()
fenetre.title("")

Canevas=Canvas(fenetre,height=hauteur,width=largeur)
Canevas.pack()

# Bouton1 = Button(fenetre,  text = 'Quitter',  command = fenetre.destroy)
# Bouton1.pack(side="top")
temps=StringVar()
Label(fenetre,textvariable=temps).pack()
temps.set("0 s")
texte_points=StringVar()
Label(fenetre,textvariable=texte_points).pack()
texte_points.set("0 point")
# texte_angle=StringVar()
# Label(fenetre,textvariable=texte_angle).pack()
# texte_angle.set("0 degrés")


#Plateau
image = Image.open("C:/Users/jeanb/OneDrive/Documents/Python/Tkinter codes/Roues-holonomes/plateau de départ.png")  # Replace with your image file path
resized_image = image.resize((largeur,hauteur))
img = ImageTk.PhotoImage(resized_image)
plateau = Canevas.create_image( 0, 0, image = img, anchor = "nw")

#Robot avec polygone, bonnes proportions par rapport au plateau
# Construction autour de 0,0
r = (275+64/2)/sqrt(3) #rayon en mm
r_inte = r-26 #inte et exte font référence au diamètre des sommets des roues, avec r_exte = r
angle_robot = asin(32/r)*180/pi #degré
angle_exte = asin(29/r)*180/pi #degré
angle_inte = asin(29/r_inte)*180/pi #degré
r *= 873/3000 #rayon en pixels : 3000 mm de plateau réels correspondent ici à 873 pixels
r_inte *= 873/3000 #rayon en pixels
x0, y0 = 99, 338
robot = Canevas.create_polygon(r*cos(rad(angle_robot)) + x0, r*sin(rad(angle_robot)) + y0, r*cos(rad(120-angle_robot)) + x0, r*sin(rad(120-angle_robot)) + y0, r*cos(rad(120+angle_robot)) + x0, r*sin(rad(120+angle_robot)) + y0, r*cos(rad(-(120+angle_robot))) + x0, r*sin(rad(-(120+angle_robot))) + y0, r*cos(rad(-(120-angle_robot))) + x0, r*sin(rad(-(120-angle_robot))) + y0, r*cos(rad(-angle_robot)) + x0, r*sin(rad(-angle_robot)) + y0, fill="black")
roue_avant_gauche = Canevas.create_polygon(r_inte*cos(rad(angle_inte)) + x0, r_inte*sin(rad(angle_inte)) + y0, r_inte*cos(rad(-angle_inte)) + x0, r_inte*sin(rad(-angle_inte)) + y0, r*cos(rad(-angle_exte)) + x0, r*sin(rad(-angle_exte)) + y0, r*cos(rad(angle_exte)) + x0, r*sin(rad(angle_exte)) + y0, fill="blue")
roue_arriere = Canevas.create_polygon(r_inte*cos(rad(-(120-angle_inte))) + x0, r_inte*sin(rad(-(120-angle_inte))) + y0, r_inte*cos(rad(-(120+angle_inte))) + x0, r_inte*sin(rad(-(120+angle_inte))) + y0, r*cos(rad(-(120+angle_exte))) + x0, r*sin(rad(-(120+angle_exte))) + y0, r*cos(rad(-(120-angle_exte))) + x0, r*sin(rad(-(120-angle_exte))) + y0, fill="red")
roue_avant_droite = Canevas.create_polygon(r_inte*cos(rad(120-angle_inte)) + x0, r_inte*sin(rad(120-angle_inte)) + y0, r_inte*cos(rad(120+angle_inte)) + x0, r_inte*sin(rad(120+angle_inte)) + y0, r*cos(rad(120+angle_exte)) + x0, r*sin(rad(120+angle_exte)) + y0, r*cos(rad(120-angle_exte)) + x0, r*sin(rad(120-angle_exte)) + y0, fill="blue")
# roues = [roue_avant_gauche, roue_avant_droite, roue_arriere]

#Stratégie grand robot
# objectifs=[
objectifs = [Deplacement(247,333,-60), Deplacement(205,585,75), Deplacement(157,615,75,0,5,"échantillon dans l'abri de chantier"), Deplacement(272,374,-60), Deplacement(231,618,75), Deplacement(194,648,75,0,5,"échantillon dans l'abri de chantier"), Deplacement(268,294,-60), Deplacement(178,557,75), Deplacement(130,587,75,0,5,"échantillon dans l'abri de chantier"), #abri de chantier
             Deplacement(270,507,-60), Deplacement(231,195,-150,points=6,desc="échantillon dans la vitrine au bon emplacement"), Deplacement(284,560,-60),Deplacement(372,195,-150,points=6,desc="échantillon dans la vitrine au bon emplacement"),Deplacement(283,472,-60,0),Deplacement(313,522,-60),Deplacement(300,195,-150,points=6,desc="échantillon dans la vitrine au bon emplacement"), #vitrine
             Deplacement(x0+30,y0,-150,points=20,desc="les deux robots sont rentrés au campement ou au site de fouille")] #retour, points si les deux robots sont rentrés

#Paramètres
v_const = 80 #vitesse constante du robot : 80 pixels/s
v_const = 200 #TEMP pour créer la stratégie
objectif_en_cours = 0 #indice de l'objectif en cours dans la liste
x_obj = objectifs[objectif_en_cours].x
y_obj = objectifs[objectif_en_cours].y
angle_obj = objectifs[objectif_en_cours].angle
xo, yo, angle = x0, y0, 0 #coordonnées du centre du robot et angle initial. 0 car la roue avant gauche (verte) est vers la droite. Sens direct=sens trigo mais en degrés
temps_total = 0 #en s, ne doit pas dépasser 100 s
r_roue = 0.058 #m
points_total = 0

Canevas.bind('<Button-1>',  Clic_gauche)
Canevas.bind('<Button-3>',  Clic_droit)
save_x, save_y = 0, 0

texte_angle = Canevas.create_text(x0, y0, text=str(angle), fill="white")


deplacement()

fenetre.mainloop()