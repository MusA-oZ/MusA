from upemtk import *
from time import sleep
from random import randrange
from tkinter import *
import pygame , sys , random, time
from pygame.locals import *


def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')

def affiche_serpent(serpents, longueur):
    for serpent in serpents:
        x, y = case_vers_pixel(serpent)
    
        cercle(x, y, taille_case/2 + 1,
               couleur='darkgreen', remplissage='darkblue')
        
    for i in range(1,longueur):
        x, y = case_vers_pixel((serpents[0][0]-i,serpents[0][1]))
        
        cercle(x, y, taille_case/2 + 1,
                   couleur='darkgreen', remplissage='green')
        

def ajouter_pommes(l,h,pommes):
    pommes.append((randrange(0, l, 2),randrange(0,h,2)))
    return pommes

def change_direction(direction, touche):
    # à compléter !!!
    if touche == 'Up':
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down':
        return (0, 1)
    elif touche == 'Right':
        return (1, 0)
    elif touche == 'Left':
        return (-1, 0)
    else:
        # pas de changement !
        return direction
    
x0, y0 = 100, 100
dx = 0
dy = 0
flag = 0




# dimensions du jeu
taille_case = 15
largeur_plateau = 60  # en nombre de cases
hauteur_plateau = 50  # en nombre de cases




# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 10    # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)  # direction initiale du serpent
    pommes = [(10,10)] # liste des coordonnées des cases contenant des pommes
    serpent = [(0,10)] # liste des coordonnées de cases adjacentes décrivant le serpent
    cree_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
    time_elapsed = 0
    touchedPomme = []
    longueur = 1

# ---------------------------------------------------------boucle principale-------------------------------------------------------------------------
     
    jouer = True
    
    while jouer:
        # affichage des objets
        efface_tout()
        affiche_pommes(pommes) 
        affiche_serpent(serpent, longueur)  # à modifier !
        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            print(touche(ev))
            direction = change_direction(direction, touche(ev))
            
        serpent[0] = (serpent[0][0]+direction[0], serpent[0][1]+direction[1])

        touchedPomme = [x for x in serpent if x in pommes]
        if(len(touchedPomme) > 0):
            longueur = longueur + 1
            #serpent.append((serpent[len(serpent)-1][0]+direction[0], serpent[len(serpent)-1][1]+direction[1]))
            pommes.remove(touchedPomme[0])
            touchedPomme = []
        
        if(serpent[0][0] > largeur_plateau or serpent[0][0] < 0 or serpent[0][1] > hauteur_plateau or serpent[0][1] < 0):
            jouer = False # le joueur a perdu
        
        # modification pour avoir une longueur : au lieu de remplacer serpent[0], il faut append sur la liste serpent avec la derniere arete+direction
        # l'affichage se fera par boucle sur toutes les aretes du serpent
        # et les verifications de bord se feront sur la derniere arete de la liste serpent
        
        time_elapsed = time_elapsed + 1
        
        if(time_elapsed == 10) :
            time_elapsed = 0
            pommes = ajouter_pommes(largeur_plateau,hauteur_plateau,pommes)
        
        # attente avant rafraîchissement
        sleep(1/framerate)
    # fermeture et sortie
    ferme_fenetre()
