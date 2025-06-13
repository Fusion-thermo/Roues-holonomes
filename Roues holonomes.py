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
        #TEMP pour créer la stratégie :
        self.duree_action = duree_action/4

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
    print("diff", event.x-save_x, event.y-save_y, sqrt((event.x-save_x)**2 + (event.y-save_y)**2))
    save_x = event.x
    save_y = event.y

def deplacement():
    #actuellement pas de vitesse de rotation max
    global temps_total, points_total
    global xo_gr, yo_gr, x_obj_gr, y_obj_gr, angle_gr, angle_robot_gr, angle_obj_gr, robot_gr, timeout_gr, fin_strat_gr, timeout_gr_fini, objectif_en_cours_gr
    global xo_pr, yo_pr, x_obj_pr, y_obj_pr, angle_pr, angle_robot_pr, angle_obj_pr, robot_pr, timeout_pr, fin_strat_pr, timeout_pr_fini, objectif_en_cours_pr
    pas_de_temps = 0.025 #s
    temps_total += pas_de_temps
    temps.set(str(round(temps_total)) + ' s')
    timeout_gr = max(0, timeout_gr - pas_de_temps)
    timeout_pr = max(0, timeout_pr - pas_de_temps)


    #Déterminer le déplacement prévu GRAND ROBOT
    d_gr = sqrt((x_obj_gr-xo_gr)**2 + (y_obj_gr-yo_gr)**2) #distance en pixels entre la position actuelle et la position de l'objectif en cours
    dt_gr = d_gr
    t_gr = d_gr/v_const #temps en s qu'on mettrait pour y aller à cette vitesse constante
    if t_gr > pas_de_temps:#si cela prend plus de temps que le pas de temps de l'affichage alors on va moins loin
        t_gr = pas_de_temps #s
        dt_gr = v_const * t_gr #pixels
    #Déterminer les vitesses du centre du robot et la vitesse angulaire en pixel/s et degré/s
    if d_gr>0:
        Vox_gr = abs(x_obj_gr-xo_gr)*(dt_gr/d_gr)/t_gr
        Voy_gr = abs(y_obj_gr-yo_gr)*(dt_gr/d_gr)/t_gr
        omega_z_gr = abs(angle_obj_gr - angle_gr)*(dt_gr/d_gr)/t_gr
        t_alpha_gr = t_gr
        if omega_z_gr > omega_max:
            omega_z_gr = omega_max
            t_alpha_gr = abs(angle_obj_gr - angle_gr)*(dt_gr/d_gr)/omega_z_gr
            if t_alpha_gr > pas_de_temps:
                t_alpha_gr = pas_de_temps
    elif abs(angle_obj_gr - angle_gr) > 0: #si rotation pure
        Vox_gr = 0
        Voy_gr = 0
        alpha_gr = abs(angle_obj_gr - angle_gr)
        t_alpha_gr = alpha_gr/omega_max
        if t_alpha_gr > pas_de_temps:
            t_alpha_gr = pas_de_temps
            alpha_gr = omega_max*t_alpha_gr
        omega_z_gr = alpha_gr/t_alpha_gr
    else:
        Vox_gr = 0
        Voy_gr = 0
        omega_z_gr = 0
        t_alpha_gr = 0
    #Déterminer les vitesses forcées des trois roues en pixels/s
    if d_gr > 0:
        Vaf_gr = 0.5*Vox_gr - sqrt(3)*0.5*Voy_gr - dt_gr*omega_z_gr
        Vbf_gr = 0.5*Vox_gr + sqrt(3)*0.5*Voy_gr - dt_gr*omega_z_gr
        Vcf_gr = -Vox_gr - dt_gr*omega_z_gr
    else:#si rotation pure
        Vaf_gr = - perimetre_gr*omega_z_gr #car la vitesse max est basée sur le périmètre du grand robot
        Vbf_gr = - perimetre_gr*omega_z_gr
        Vcf_gr = - perimetre_gr*omega_z_gr
    #Déterminer la vitesse de rotation des moteurs des trois roues en degré/s
    omega_a_gr = (3*873)*Vaf_gr/r_roue
    omega_b_gr = (3*873)*Vbf_gr/r_roue
    omega_c_gr = (3*873)*Vcf_gr/r_roue
    #Déterminer le déplacement prévu PETIT ROBOT
    d_pr = sqrt((x_obj_pr-xo_pr)**2 + (y_obj_pr-yo_pr)**2) #distance en pixels entre la position actuelle et la position de l'objectif en cours
    dt_pr = d_pr
    t_pr = d_pr/v_const #temps en s qu'on mettrait pour y aller à cette vitesse constante
    if t_pr > pas_de_temps:#si cela prend plus de temps que le pas de temps de l'affichage alors on va moins loin
        t_pr = pas_de_temps #s
        dt_pr = v_const * t_pr #pixels
    #Déterminer les vitesses du centre du robot et la vitesse angulaire en pixel/s et degré/s
    if d_pr>0:
        Vox_pr = abs(x_obj_pr-xo_pr)*(dt_pr/d_pr)/t_pr
        Voy_pr = abs(y_obj_pr-yo_pr)*(dt_pr/d_pr)/t_pr
        omega_z_pr = abs(angle_obj_pr - angle_pr)*(dt_pr/d_pr)/t_pr
        t_alpha_pr = t_pr
        if omega_z_pr > omega_max:
            omega_z_pr = omega_max
            t_alpha_pr = abs(angle_obj_pr - angle_pr)*(dt_pr/d_pr)/omega_z_pr
            if t_alpha_pr > pas_de_temps:
                t_alpha_pr = pas_de_temps
    elif abs(angle_obj_pr - angle_pr) > 0: #si rotation pure
        Vox_pr = 0
        Voy_pr = 0
        alpha_pr = abs(angle_obj_pr - angle_pr)
        t_alpha_pr = alpha_pr/omega_max
        if t_alpha_pr > pas_de_temps:
            t_alpha_pr = pas_de_temps
            alpha_pr = omega_max*t_alpha_pr
        omega_z_pr = alpha_pr/t_alpha_pr
    else:
        Vox_pr = 0
        Voy_pr = 0
        omega_z_pr = 0
        t_alpha_pr = 0
    #Déterminer les vitesses forcées des trois roues en pixels/s
    if d_pr > 0:
        Vaf_pr = 0.5*Vox_pr - sqrt(3)*0.5*Voy_pr - dt_pr*omega_z_pr
        Vbf_pr = 0.5*Vox_pr + sqrt(3)*0.5*Voy_pr - dt_pr*omega_z_pr
        Vcf_pr = -Vox_pr - dt_pr*omega_z_pr
    else:#si rotation pure
        Vaf_pr = - perimetre_pr*omega_z_pr #car la vitesse max est basée sur le périmètre du petit robot
        Vbf_pr = - perimetre_pr*omega_z_pr
        Vcf_pr = - perimetre_pr*omega_z_pr
    #Déterminer la vitesse de rotation des moteurs des trois roues en degré/s
    omega_a_pr = (3*873)*Vaf_pr/r_roue
    omega_b_pr = (3*873)*Vbf_pr/r_roue
    omega_c_pr = (3*873)*Vcf_pr/r_roue

    #Calcul des nouvelles coordonnées GRAND ROBOT
    xo_gr += signe(x_obj_gr - xo_gr) * Vox_gr * t_gr
    yo_gr += signe(y_obj_gr - yo_gr) * Voy_gr * t_gr
    delta_angle_gr = signe(angle_obj_gr - angle_gr) * omega_z_gr * t_alpha_gr # degrés
    angle_gr += delta_angle_gr
    #Calcul des nouvelles coordonnées PETIT ROBOT
    xo_pr += signe(x_obj_pr - xo_pr) * Vox_pr * t_pr
    yo_pr += signe(y_obj_pr - yo_pr) * Voy_pr * t_pr
    delta_angle_pr = signe(angle_obj_pr - angle_pr) * omega_z_pr * t_alpha_pr # degrés
    angle_pr += delta_angle_pr

    #Mettre à jour les coordonnées GRAND ROBOT
    Canevas.coords(robot_gr, r_gr*cos(rad(angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(angle_robot_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120-angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120-angle_robot_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120+angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120+angle_robot_gr+angle_gr)) + yo_gr, r_gr*cos(rad(-(120+angle_robot_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120+angle_robot_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-(120-angle_robot_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120-angle_robot_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-angle_robot_gr+angle_gr)) + xo_gr, r_gr*sin(rad(-angle_robot_gr+angle_gr)) + yo_gr)
    Canevas.coords(roue_avant_gauche_gr, r_inte_gr*cos(rad(angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(angle_inte_gr+angle_gr)) + yo_gr, r_inte_gr*cos(rad(-angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(-angle_inte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(-angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(-angle_exte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(angle_exte_gr+angle_gr)) + yo_gr)
    Canevas.coords(roue_arriere_gr, r_inte_gr*cos(rad(-(120-angle_inte_gr-angle_gr))) + xo_gr, r_inte_gr*sin(rad(-(120-angle_inte_gr-angle_gr))) + yo_gr, r_inte_gr*cos(rad(-(120+angle_inte_gr-angle_gr))) + xo_gr, r_inte_gr*sin(rad(-(120+angle_inte_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-(120+angle_exte_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120+angle_exte_gr-angle_gr))) + yo_gr, r_gr*cos(rad(-(120-angle_exte_gr-angle_gr))) + xo_gr, r_gr*sin(rad(-(120-angle_exte_gr-angle_gr))) + yo_gr)
    Canevas.coords(roue_avant_droite_gr, r_inte_gr*cos(rad(120-angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(120-angle_inte_gr+angle_gr)) + yo_gr, r_inte_gr*cos(rad(120+angle_inte_gr+angle_gr)) + xo_gr, r_inte_gr*sin(rad(120+angle_inte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120+angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120+angle_exte_gr+angle_gr)) + yo_gr, r_gr*cos(rad(120-angle_exte_gr+angle_gr)) + xo_gr, r_gr*sin(rad(120-angle_exte_gr+angle_gr)) + yo_gr)
    # Canevas.coords(texte_angle,xo_gr,yo_gr)
    # Canevas.itemconfigure(texte_angle, text=str(round(angle_gr)))
    #Mettre à jour les coordonnées PETIT ROBOT
    Canevas.coords(robot_pr, r_pr*cos(rad(angle_robot_pr+angle_pr)) + xo_pr, r_pr*sin(rad(angle_robot_pr+angle_pr)) + yo_pr, r_pr*cos(rad(120-angle_robot_pr+angle_pr)) + xo_pr, r_pr*sin(rad(120-angle_robot_pr+angle_pr)) + yo_pr, r_pr*cos(rad(120+angle_robot_pr+angle_pr)) + xo_pr, r_pr*sin(rad(120+angle_robot_pr+angle_pr)) + yo_pr, r_pr*cos(rad(-(120+angle_robot_pr-angle_pr))) + xo_pr, r_pr*sin(rad(-(120+angle_robot_pr-angle_pr))) + yo_pr, r_pr*cos(rad(-(120-angle_robot_pr-angle_pr))) + xo_pr, r_pr*sin(rad(-(120-angle_robot_pr-angle_pr))) + yo_pr, r_pr*cos(rad(-angle_robot_pr+angle_pr)) + xo_pr, r_pr*sin(rad(-angle_robot_pr+angle_pr)) + yo_pr)
    Canevas.coords(roue_avant_gauche_pr, r_inte_pr*cos(rad(angle_inte_pr+angle_pr)) + xo_pr, r_inte_pr*sin(rad(angle_inte_pr+angle_pr)) + yo_pr, r_inte_pr*cos(rad(-angle_inte_pr+angle_pr)) + xo_pr, r_inte_pr*sin(rad(-angle_inte_pr+angle_pr)) + yo_pr, r_pr*cos(rad(-angle_exte_pr+angle_pr)) + xo_pr, r_pr*sin(rad(-angle_exte_pr+angle_pr)) + yo_pr, r_pr*cos(rad(angle_exte_pr+angle_pr)) + xo_pr, r_pr*sin(rad(angle_exte_pr+angle_pr)) + yo_pr)
    Canevas.coords(roue_arriere_pr, r_inte_pr*cos(rad(-(120-angle_inte_pr-angle_pr))) + xo_pr, r_inte_pr*sin(rad(-(120-angle_inte_pr-angle_pr))) + yo_pr, r_inte_pr*cos(rad(-(120+angle_inte_pr-angle_pr))) + xo_pr, r_inte_pr*sin(rad(-(120+angle_inte_pr-angle_pr))) + yo_pr, r_pr*cos(rad(-(120+angle_exte_pr-angle_pr))) + xo_pr, r_pr*sin(rad(-(120+angle_exte_pr-angle_pr))) + yo_pr, r_pr*cos(rad(-(120-angle_exte_pr-angle_pr))) + xo_pr, r_pr*sin(rad(-(120-angle_exte_pr-angle_pr))) + yo_pr)
    Canevas.coords(roue_avant_droite_pr, r_inte_pr*cos(rad(120-angle_inte_pr+angle_pr)) + xo_pr, r_inte_pr*sin(rad(120-angle_inte_pr+angle_pr)) + yo_pr, r_inte_pr*cos(rad(120+angle_inte_pr+angle_pr)) + xo_pr, r_inte_pr*sin(rad(120+angle_inte_pr+angle_pr)) + yo_pr, r_pr*cos(rad(120+angle_exte_pr+angle_pr)) + xo_pr, r_pr*sin(rad(120+angle_exte_pr+angle_pr)) + yo_pr, r_pr*cos(rad(120-angle_exte_pr+angle_pr)) + xo_pr, r_pr*sin(rad(120-angle_exte_pr+angle_pr)) + yo_pr)
    # Canevas.coords(texte_angle,xo_pr,yo_pr)
    # Canevas.itemconfigure(texte_angle, text=str(round(angle_pr)))

    recursif = fenetre.after(int(pas_de_temps*1000),deplacement)
    #Si on a atteint l'objectif GRAND ROBOT
    if not fin_strat_gr and timeout_gr == 0 and (xo_gr == x_obj_gr and yo_gr == y_obj_gr and angle_gr%360 == angle_obj_gr%360):
        if not timeout_gr_fini:
            timeout_gr = objectifs_gr[objectif_en_cours_gr].duree_action
            timeout_gr_fini = True
        else:
            timeout_gr_fini=False
            if objectifs_gr[objectif_en_cours_gr].points >0:
                points_total += objectifs_gr[objectif_en_cours_gr].points
                texte_points.set(str(points_total)+" points\n+"+str(objectifs_gr[objectif_en_cours_gr].points)+" : "+objectifs_gr[objectif_en_cours_gr].description_points)
            objectif_en_cours_gr+=1
            #Si on a terminé tous les objectifs
            if objectif_en_cours_gr == len(objectifs_gr):
                print("Fin de la strat du grand robot")
                fin_strat_gr =True
            else:
                x_obj_gr = objectifs_gr[objectif_en_cours_gr].x
                y_obj_gr = objectifs_gr[objectif_en_cours_gr].y
                angle_obj_gr = objectifs_gr[objectif_en_cours_gr].angle
    #Si on a atteint l'objectif PETIT ROBOT
    if not fin_strat_pr and timeout_pr == 0 and (xo_pr == x_obj_pr and yo_pr == y_obj_pr and angle_pr%360 == angle_obj_pr%360):
        if not timeout_pr_fini:
            timeout_pr = objectifs_pr[objectif_en_cours_pr].duree_action
            timeout_pr_fini = True
        else:
            timeout_pr_fini=False
            if objectifs_pr[objectif_en_cours_pr].points >0:
                points_total += objectifs_pr[objectif_en_cours_pr].points
                texte_points.set(str(points_total)+" points\n+"+str(objectifs_pr[objectif_en_cours_pr].points)+" : "+objectifs_pr[objectif_en_cours_pr].description_points)
            objectif_en_cours_pr+=1
            #Si on a terminé tous les objectifs
            if objectif_en_cours_pr == len(objectifs_pr):
                print("Fin de la strat du petit robot")
                fin_strat_pr =True
            else:
                x_obj_pr = objectifs_pr[objectif_en_cours_pr].x
                y_obj_pr = objectifs_pr[objectif_en_cours_pr].y
                angle_obj_pr = objectifs_pr[objectif_en_cours_pr].angle

    if temps_total >= 100: #si plus de 100 secondes
        fenetre.after_cancel(recursif)
        print("Fin au temps")
        return "Fin du temps"
    elif fin_strat_gr and fin_strat_pr:
        fenetre.after_cancel(recursif)
        print("Fin de la stratégie globale")
        return "Fin de la stratégie"


#Tkinter
hauteur,largeur=769, 1000

fenetre=Tk()
fenetre.title("")

Canevas=Canvas(fenetre,height=hauteur,width=largeur)
Canevas.pack()

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
             Deplacement(270,507,-60), Deplacement(231,195,-150,points=6,desc="échantillon dans la galerie au bon emplacement"), Deplacement(284,560,-60),Deplacement(372,195,-150,points=6,desc="échantillon dans la galerie au bon emplacement"),Deplacement(283,472,-60,0),Deplacement(313,522,-60),Deplacement(300,195,-150,points=6,desc="échantillon dans la galerie au bon emplacement"), #galerie
             Deplacement(350,528,-150,0,points=20+34,desc="les deux robots sont rentrés au campement ou au site de fouille (20) et prédiction correcte du score (ceil(112*0.3) = 34)")] #retour, points si les deux robots sont rentrés
objectifs_pr = [Deplacement(x0_pr+1,y0_pr,0,0,5,"non forfait + vitrine déposée + statuette déposée"), Deplacement(367,685,30,3), Deplacement(367,695,30,0,5,"carré de fouille de notre équipe"), Deplacement(367,685,30,0), Deplacement(428,685,30), Deplacement(428,695,30,0,5,"carré de fouille de notre équipe"), Deplacement(428,685,30,0), Deplacement(312,685,30,0), Deplacement(312,695,30,42,10,"carré de fouille de notre équipe et carré rouge non retourné"), #mesurer et retourner les carrés de fouille
             Deplacement(165,623,-45,points=5,desc="prend la statuette"),Deplacement(165,623,135,points=10,desc="pose la réplique"),Deplacement(131,171,270,points=20,desc="pose la statuette sur la vitrine qui s'allume"), #statuette et vitrine
             Deplacement(116,300,270,0)] #retour

#Initialisation des paramètres des robots
objectif_en_cours_gr, objectif_en_cours_pr = 0, 0 #indice de l'objectif en cours dans la liste
timeout_gr, timeout_pr = 0, 0 #permet de mettre en pause le mouvement des robots durant le temps nécessaire pour accomplir l'action
timeout_gr_fini, timeout_pr_fini = False, False
fin_strat_gr, fin_strat_pr = False, False

x_obj_gr = objectifs_gr[objectif_en_cours_gr].x
y_obj_gr = objectifs_gr[objectif_en_cours_gr].y
angle_obj_gr = objectifs_gr[objectif_en_cours_gr].angle
xo_gr, yo_gr, angle_gr = x0_gr, y0_gr, 0 #coordonnées du centre du robot et angle initial. 0 car la roue avant gauche (verte) est vers la droite. Sens direct=sens trigo mais en degrés
perimetre_gr = 2*pi*((r_inte_gr+r_gr)/2) #pixels, périmètre du cercle formé par les roues du grand robot 

x_obj_pr = objectifs_pr[objectif_en_cours_pr].x
y_obj_pr = objectifs_pr[objectif_en_cours_pr].y
angle_obj_pr = objectifs_pr[objectif_en_cours_pr].angle
xo_pr, yo_pr, angle_pr = x0_pr, y0_pr, 0 #coordonnées du centre du robot et angle initial. 0 car la roue avant gauche (verte) est vers la droite. Sens direct=sens trigo mais en degrés
perimetre_pr = 2*pi*((r_inte_pr+r_pr)/2) #pixels, périmètre du cercle formé par les roues du petit robot 

#Paramètres généraux
v_const = 61 #vitesse linéaire constante du robot : 61 pixels/s trouvés grossièrement avec la vidéo du match depuis les tribunes
v_const = 200 #TEMP pour créer la stratégie
temps_total = 0 #en s, ne doit pas dépasser 100 s
r_roue = 0.058 #m
r_roue *= 873/3 #pixels
perimetre_roue = 2*pi*r_roue
omega_max = (180/pi)*(2*pi*perimetre_pr/perimetre_roue)/10 # degré/s on part sur un 360° en 10s
points_total = 0

temps=StringVar()
Label(fenetre,textvariable=temps).pack()
temps.set("0 s")
texte_points=StringVar()
Label(fenetre,textvariable=texte_points).pack()
texte_points.set(f"{points_total} points")

Canevas.bind('<Button-1>',  Clic_gauche)
Canevas.bind('<Button-3>',  Clic_droit)
save_x, save_y = 0, 0
# texte_angle = Canevas.create_text(x0_pr, y0_pr, text=str(angle_pr), fill="white")

deplacement()

fenetre.mainloop()