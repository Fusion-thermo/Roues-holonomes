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
    global xo_gr, yo_gr, x_obj_gr, y_obj_gr, angle_gr, angle_robot_gr, angle_inte_gr, angle_exte_gr, angle_obj_gr, robot_gr, objectif_en_cours, v_const, temps_total, r_roue, x0_gr, y0_gr, r, r_inte_gr, points_total
    pas_de_temps = 0.05 #s
    temps_total += pas_de_temps
    temps.set(str(round(temps_total)) + ' s')


    #Déterminer le déplacement prévu
    d_gr = max(sqrt((x_obj_gr-xo_gr)**2 + (y_obj_gr-yo_gr)**2), 0.0001) #distance en pixels entre la position actuelle et la position de l'objectif en cours
    dt_gr = d_gr
    t_gr = d_gr/v_const #temps en s qu'on mettrait pour y aller à cette vitesse constante
    if t_gr > pas_de_temps:#si cela prend plus de temps que le pas de temps de l'affichage alors on va moins loin
        t_gr = pas_de_temps #s
        dt_gr = v_const * t_gr #pixels
    #Déterminer les vitesses du centre du robot et la vitesse angulaire en pixel/s et degré/s
    Vox_gr = abs(x_obj_gr-xo_gr)*(dt_gr/d_gr)/t_gr
    Voy_gr = abs(y_obj_gr-yo_gr)*(dt_gr/d_gr)/t_gr
    omega_z_gr = abs(angle_obj_gr - angle_gr)*(dt_gr/d_gr)/t_gr #attention aux modulos de nombres flottants ! # Est-ce la bonne unité ?
    #Déterminer les vitesses forcées des trois roues en pixels/s
    Vaf_gr = 0.5*Vox_gr - sqrt(3)*0.5*Voy_gr - dt_gr*omega_z_gr
    Vbf_gr = 0.5*Vox_gr + sqrt(3)*0.5*Voy_gr - dt_gr*omega_z_gr
    Vcf_gr = -Vox_gr - dt_gr*omega_z_gr
    #Déterminer la vitesse de rotation des moteurs des trois roues en degré/s
    omega_a_gr = (3*873)*Vaf_gr/r_roue
    omega_b_gr = (3*873)*Vbf_gr/r_roue
    omega_c_gr = (3*873)*Vcf_gr/r_roue

    #Calcul des nouvelles coordonnées
    xo_gr += signe(x_obj_gr - xo_gr) * Vox_gr * t_gr
    yo_gr += signe(y_obj_gr - yo_gr) * Voy_gr * t_gr
    delta_angle_gr = signe(angle_obj_gr - angle_gr) * omega_z_gr * t_gr # degrés
    angle_gr += delta_angle_gr

    #Mettre à jour les coordonnées
    Canevas.coords(robot_gr, r_gr*cos(rad(angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(angle_robot_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120-angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120-angle_robot_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120+angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120+angle_robot_gr+angle_gr)) + yo_gr, r_gr*cos(rad(-(120+angle_robot_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120+angle_robot_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-(120-angle_robot_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120-angle_robot_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(-angle_robot_gr+angle_gr)) + yo_gr)
    Canevas.coords(roue_avant_gauche_gr, r_inte_gr*cos(rad(angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(angle_inte_gr+angle_gr)) + yo_gr, r_inte_gr*cos(rad(-angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(-angle_inte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(-angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(-angle_exte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(angle_exte_gr+angle_gr)) + yo_gr)
    Canevas.coords(roue_arriere_gr, r_inte_gr*cos(rad(-(120-angle_inte_gr-angle_gr))) + xo_gr, r_inte_gr*sin(rad(-(120-angle_inte_gr-angle_gr))) + yo_gr, r_inte_gr*cos(rad(-(120+angle_inte_gr-angle_gr))) + xo_gr, r_inte_gr*sin(rad(-(120+angle_inte_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-(120+angle_exte_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120+angle_exte_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-(120-angle_exte_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120-angle_exte_gr-angle_gr))) + yo_gr)
    Canevas.coords(roue_avant_droite_gr, r_inte_gr*cos(rad(120-angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(120-angle_inte_gr+angle_gr)) + yo_gr, r_inte_gr*cos(rad(120+angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(120+angle_inte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120+angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120+angle_exte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120-angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120-angle_exte_gr+angle_gr)) + yo_gr)
    Canevas.coords(texte_angle,xo_gr,yo_gr)
    Canevas.itemconfigure(texte_angle, text=str(round(angle_gr)))

    recursif = fenetre.after(int(pas_de_temps*1000),deplacement)
    #Si on a atteint l'objectif
    # print(xo_gr - x_obj_gr, yo_gr - y_obj_gr, angle%360 - angle_obj_gr%360)
    if xo_gr == x_obj_gr and yo_gr == y_obj_gr and angle_gr%360 == angle_obj_gr%360:
        time.sleep(objectifs_gr[objectif_en_cours].duree_action)
        temps_total += objectifs_gr[objectif_en_cours].duree_action
        if objectifs_gr[objectif_en_cours].points >0:
            points_total += objectifs_gr[objectif_en_cours].points
            texte_points.set(str(points_total)+" points. +"+str(objectifs_gr[objectif_en_cours].points)+" : "+objectifs_gr[objectif_en_cours].description_points)
        objectif_en_cours+=1
        #Si on a terminé tous les objectifs
        if objectif_en_cours == len(objectifs_gr):
            print("Fin car tous les objectifs ont été remplis")
            fenetre.after_cancel(recursif)
            return "Fin de la stratégie"
        else:
            x_obj_gr = objectifs_gr[objectif_en_cours].x
            y_obj_gr = objectifs_gr[objectif_en_cours].y
            angle_obj_gr = objectifs_gr[objectif_en_cours].angle
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
# Label(fenetre,textvariable=texte_angle_gr).pack()
# texte_angle.set("0 degrés")


#Plateau
image = Image.open("C:/Users/jeanb/OneDrive/Documents/Python/Tkinter codes/Roues-holonomes/plateau de départ.png")  # Replace with yo_grur image file path
resized_image = image.resize((largeur,hauteur))
img = ImageTk.PhotoImage(resized_image)
plateau = Canevas.create_image( 0, 0, image = img, anchor = "nw")

#Grand robot avec polygone, bonnes proportions par rapport au plateau
# Construction autour de 0,0
r_gr = (275+64/2)/sqrt(3) #rayo_grn en mm
r_inte_gr = r_gr-26 #inte et exte font référence au diamètre des sommets des roues, avec r_exte = r
angle_robot_gr = asin(32/r_gr)*180/pi #degré
angle_exte_gr = asin(29/r_gr)*180/pi #degré
angle_inte_gr = asin(29/r_inte_gr)*180/pi #degré
r_gr *= 873/3000 #rayo_grn en pixels : 3000 mm de plateau réels correspondent ici à 873 pixels
r_inte_gr *= 873/3000 #rayo_grn en pixels
x0_gr, y0_gr = 127, 304
robot_gr = Canevas.create_polygon(r_gr*cos(rad(angle_robot_gr)) + x0_gr, r_gr*sin(rad(angle_robot_gr)) + y0_gr, r_gr*cos(rad(120-angle_robot_gr)) + x0_gr, r_gr*sin(rad(120-angle_robot_gr)) + y0_gr, r_gr*cos(rad(120+angle_robot_gr)) + x0_gr, r_gr*sin(rad(120+angle_robot_gr)) + y0_gr, r_gr*cos(rad(-(120+angle_robot_gr))) + x0_gr, r_gr*sin(rad(-(120+angle_robot_gr))) + y0_gr, r_gr*cos(rad(-(120-angle_robot_gr))) + x0_gr, r_gr*sin(rad(-(120-angle_robot_gr))) + y0_gr, r_gr*cos(rad(-angle_robot_gr)) + x0_gr, r_gr*sin(rad(-angle_robot_gr)) + y0_gr, fill="black")
roue_avant_gauche_gr = Canevas.create_polygon(r_inte_gr*cos(rad(angle_inte_gr)) + x0_gr, r_inte_gr*sin(rad(angle_inte_gr)) + y0_gr, r_inte_gr*cos(rad(-angle_inte_gr)) + x0_gr, r_inte_gr*sin(rad(-angle_inte_gr)) + y0_gr, r_gr*cos(rad(-angle_exte_gr)) + x0_gr, r_gr*sin(rad(-angle_exte_gr)) + y0_gr, r_gr*cos(rad(angle_exte_gr)) + x0_gr, r_gr*sin(rad(angle_exte_gr)) + y0_gr, fill="blue")
roue_arriere_gr = Canevas.create_polygon(r_inte_gr*cos(rad(-(120-angle_inte_gr))) + x0_gr, r_inte_gr*sin(rad(-(120-angle_inte_gr))) + y0_gr, r_inte_gr*cos(rad(-(120+angle_inte_gr))) + x0_gr, r_inte_gr*sin(rad(-(120+angle_inte_gr))) + y0_gr, r_gr*cos(rad(-(120+angle_exte_gr))) + x0_gr, r_gr*sin(rad(-(120+angle_exte_gr))) + y0_gr, r_gr*cos(rad(-(120-angle_exte_gr))) + x0_gr, r_gr*sin(rad(-(120-angle_exte_gr))) + y0_gr, fill="red")
roue_avant_droite_gr = Canevas.create_polygon(r_inte_gr*cos(rad(120-angle_inte_gr)) + x0_gr, r_inte_gr*sin(rad(120-angle_inte_gr)) + y0_gr, r_inte_gr*cos(rad(120+angle_inte_gr)) + x0_gr, r_inte_gr*sin(rad(120+angle_inte_gr)) + y0_gr, r_gr*cos(rad(120+angle_exte_gr)) + x0_gr, r_gr*sin(rad(120+angle_exte_gr)) + y0_gr, r_gr*cos(rad(120-angle_exte_gr)) + x0_gr, r_gr*sin(rad(120-angle_exte_gr)) + y0_gr, fill="blue")

#Petit robot avec polygone, bonnes proportions par rapport au plateau
# Construction autour de 0,0
r_pr = (180+64/2)/sqrt(3) #rayo_grn en mm
r_inte_pr = r_pr-26 #inte et exte font référence au diamètre des sommets des roues, avec r_exte = r
angle_robot_pr = asin(32/r_pr)*180/pi #degré
angle_exte_pr = asin(29/r_pr)*180/pi #degré
angle_inte_pr = asin(29/r_inte_pr)*180/pi #degré
r_pr *= 873/3000 #rayo_grn en pixels : 3000 mm de plateau réels correspondent ici à 873 pixels
r_inte_pr *= 873/3000 #rayo_grn en pixels
x0_pr, y0_pr = 109, 390
robot_pr = Canevas.create_polygon(r_pr*cos(rad(angle_robot_pr)) + x0_pr, r_pr*sin(rad(angle_robot_pr)) + y0_pr, r_pr*cos(rad(120-angle_robot_pr)) + x0_pr, r_pr*sin(rad(120-angle_robot_pr)) + y0_pr, r_pr*cos(rad(120+angle_robot_pr)) + x0_pr, r_pr*sin(rad(120+angle_robot_pr)) + y0_pr, r_pr*cos(rad(-(120+angle_robot_pr))) + x0_pr, r_pr*sin(rad(-(120+angle_robot_pr))) + y0_pr, r_pr*cos(rad(-(120-angle_robot_pr))) + x0_pr, r_pr*sin(rad(-(120-angle_robot_pr))) + y0_pr, r_pr*cos(rad(-angle_robot_pr)) + x0_pr, r_pr*sin(rad(-angle_robot_pr)) + y0_pr, fill="black")
roue_avant_gauche_pr = Canevas.create_polygon(r_inte_pr*cos(rad(angle_inte_pr)) + x0_pr, r_inte_pr*sin(rad(angle_inte_pr)) + y0_pr, r_inte_pr*cos(rad(-angle_inte_pr)) + x0_pr, r_inte_pr*sin(rad(-angle_inte_pr)) + y0_pr, r_pr*cos(rad(-angle_exte_pr)) + x0_pr, r_pr*sin(rad(-angle_exte_pr)) + y0_pr, r_pr*cos(rad(angle_exte_pr)) + x0_pr, r_pr*sin(rad(angle_exte_pr)) + y0_pr, fill="green")
roue_arriere_pr = Canevas.create_polygon(r_inte_pr*cos(rad(-(120-angle_inte_pr))) + x0_pr, r_inte_pr*sin(rad(-(120-angle_inte_pr))) + y0_pr, r_inte_pr*cos(rad(-(120+angle_inte_pr))) + x0_pr, r_inte_pr*sin(rad(-(120+angle_inte_pr))) + y0_pr, r_pr*cos(rad(-(120+angle_exte_pr))) + x0_pr, r_pr*sin(rad(-(120+angle_exte_pr))) + y0_pr, r_pr*cos(rad(-(120-angle_exte_pr))) + x0_pr, r_pr*sin(rad(-(120-angle_exte_pr))) + y0_pr, fill="red")
roue_avant_droite_pr = Canevas.create_polygon(r_inte_pr*cos(rad(120-angle_inte_pr)) + x0_pr, r_inte_pr*sin(rad(120-angle_inte_pr)) + y0_pr, r_inte_pr*cos(rad(120+angle_inte_pr)) + x0_pr, r_inte_pr*sin(rad(120+angle_inte_pr)) + y0_pr, r_pr*cos(rad(120+angle_exte_pr)) + x0_pr, r_pr*sin(rad(120+angle_exte_pr)) + y0_pr, r_pr*cos(rad(120-angle_exte_pr)) + x0_pr, r_pr*sin(rad(120-angle_exte_pr)) + y0_pr, fill="blue")


#Stratégie grand robot
# objectifs=[
objectifs_gr = [Deplacement(247,333,-60), Deplacement(205,585,75), Deplacement(157,615,75,0,5,"échantillon dans l'abri de chantier"), Deplacement(272,374,-60), Deplacement(231,618,75), Deplacement(194,648,75,0,5,"échantillon dans l'abri de chantier"), Deplacement(268,294,-60), Deplacement(178,557,75), Deplacement(130,587,75,0,5,"échantillon dans l'abri de chantier"), #abri de chantier
             Deplacement(270,507,-60), Deplacement(231,195,-150,points=6,desc="échantillon dans la vitrine au bon emplacement"), Deplacement(284,560,-60),Deplacement(372,195,-150,points=6,desc="échantillon dans la vitrine au bon emplacement"),Deplacement(283,472,-60,0),Deplacement(313,522,-60),Deplacement(300,195,-150,points=6,desc="échantillon dans la vitrine au bon emplacement"), #vitrine
             Deplacement(116,300,-150,points=20,desc="les deux robots sont rentrés au campement ou au site de fouille")] #retour, points si les deux robots sont rentrés
objectifs_pr = [Deplacement(175,485,-60), Deplacement(161,620,75)]

#Paramètres généraux
v_const = 80 #vitesse constante du robot : 80 pixels/s
v_const = 200 #TEMP pour créer la stratégie
objectif_en_cours = 0 #indice de l'objectif en cours dans la liste
temps_total = 0 #en s, ne doit pas dépasser 100 s
r_roue = 0.058 #m
points_total = 0

#Initialisation des paramètres des robots
x_obj_gr = objectifs_gr[objectif_en_cours].x
y_obj_gr = objectifs_gr[objectif_en_cours].y
angle_obj_gr = objectifs_gr[objectif_en_cours].angle
xo_gr, yo_gr, angle_gr = x0_gr, y0_gr, 0 #coordonnées du centre du robot et angle initial. 0 car la roue avant gauche (verte) est vers la droite. Sens direct=sens trigo mais en degrés
x_obj_pr = objectifs_pr[objectif_en_cours].x
y_obj_pr = objectifs_pr[objectif_en_cours].y
angle_obj_pr = objectifs_pr[objectif_en_cours].angle
xo_pr, yo_pr, angle_pr = x0_pr, y0_pr, 0 #coordonnées du centre du robot et angle initial. 0 car la roue avant gauche (verte) est vers la droite. Sens direct=sens trigo mais en degrés


Canevas.bind('<Button-1>',  Clic_gauche)
Canevas.bind('<Button-3>',  Clic_droit)
save_x, save_y = 0, 0
texte_angle = Canevas.create_text(x0_pr, y0_pr, text=str(angle_pr), fill="white")



deplacement()

fenetre.mainloop()