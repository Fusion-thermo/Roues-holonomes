# Roues-holonomes

Ce script montre la stratégie de Robotech Nancy pour la coupe de France de robotique 2022.
Il simule un match parfait en temps réel avec le comptage de points.

Les commandes de vitesse des moteurs sont également calculées, en supposant une accélération et décélération instantanées puis une vitesse linéaire constante.
La vitesse de rotation du robot varie en fonction de la distance linéaire à parcourir mais est limitée par un maximum : permet une rotation pure sans qu'elle soit instantanée.


Oui, j'aurais dû utiliser une classe au lieu d'ajouter _pr et _gr partout (sachant que j'ai commencé par un code fonctionnel pour un seul robot).



Source pour les formules des vitesses forcées des trois roues : 
https://www.poivron-robotique.fr/-Nos-etudes-.html :

Robot holonome - localisation (partie 1 - faisabilité)
Robot holonome - localisation (partie 2)
Robot holonome - lois de commande

Règlement : 

https://www.coupederobotique.fr/edition-2022/le-concours/

Robotech Nancy : 

https://robotech.polytech-nancy.univ-lorraine.fr/
https://robotechnancy.github.io/
https://fr.linkedin.com/company/robotech-nancy
https://www.instagram.com/robotechnancy/
