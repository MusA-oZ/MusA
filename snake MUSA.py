from upemtk import *
from time import sleep
from random import randrange
from tkinter import *



def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case 
    return (i + .15) * taille_case, (j + .15) * taille_case


def affiche_pommes(pommes):
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='yellow')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')

def affiche_obstacles(obstacles):
    for obstacle in obstacles:
        x, y = case_vers_pixel(obstacle)
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='black', remplissage='gray')


def affiche_serpent(serpents):
    for i in range(0,len(serpents)):
        x, y = case_vers_pixel(serpent[i])
        
        if(i <= 1):
            cercle(x, y, taille_case/2 + 0,
               couleur='black', remplissage='darkblue')
        else:
            cercle(x, y, taille_case/2 + 0,
                couleur='darkgreen', remplissage='darkgreen')

def ajouter_pommes(l,h,pommes,obstacles,serpents):
    pomme = (randrange(0, l, 2),randrange(0,h,2))
    
    # eviter de creer une pomme sur un obstacle
    while(pomme in obstacles or pommes in serpents):
        print("pomme sur obstacle/serpent")
        pomme = (randrange(0, l, 2),randrange(0,h,2))
        
    pommes.append(pomme)
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

def deplacer_serpent(serpent,direction):
    #serpent[numeroArete][direction (x ou y)]
    #ici on inverse la tete
    serpent[0] = (serpent[0][0] + direction[0],serpent[0][1] + direction[1])
    del(serpent[len(serpent)-1])
    serpent.insert(0,serpent[0])
    
def create_random_obstacles(l,h,nbObstacles):
    obstacles = []
    for i in range (0,nbObstacles):
        obstacle = (randrange(0, l, 2),randrange(0,h,2))
        obstacles.append(obstacle)
    return obstacles





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
    score = 0

# ---------------------------------------------------------boucle principale-------------------------------------------------------------------------
     
    jouer = True
    serpent.append(serpent[0])
    
    obstacles = create_random_obstacles(largeur_plateau,hauteur_plateau,7)
    
    while jouer:
        # affichage des objets       
        efface_tout()
        affiche_pommes(pommes) 
        affiche_obstacles(obstacles)
        affiche_serpent(serpent)  # à modifier !
        mise_a_jour()
        
        efface('score')
        texte(10, 10, "Score " + str(score), couleur="black", ancrage='nw', taille=10, tag='score')
        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            print(touche(ev))
            direction = change_direction(direction, touche(ev))  
        
        deplacer_serpent(serpent,direction)

        # verifier si la tete du serpent touche une pomme
        if serpent[0] in pommes:
            serpent.append((serpent[0][0], serpent[0][1]))
            pommes.remove(serpent[0])
            score = score + 1
        
        # verifier si la tete du serpent touche un obstacle
        if serpent[0] in obstacles:
            print("PERDU ! (obstacle)")
            efface("etat")
            texte(10, 25, "PERDU ! (obstacle)", couleur="red", ancrage='nw', taille=14, tag='etat')                  
            mise_a_jour()
            jouer = False # le joueur a perdu
        
        if(serpent[0][0] > largeur_plateau or serpent[0][0] < 0 or serpent[0][1] > hauteur_plateau or serpent[0][1] < 0):
            print("PERDU ! (bord de carte)")
            efface("etat")
            texte(10, 25, "PERDU ! (bord de carte)", couleur="red", ancrage='nw', taille=14, tag='etat') 
            mise_a_jour()
            jouer = False # le joueur a perdu
        
        time_elapsed = time_elapsed + 1
        
        if(time_elapsed == 40) :
            time_elapsed = 0
            pommes = ajouter_pommes(largeur_plateau,hauteur_plateau,pommes,obstacles,serpent)
        
        # attente avant rafraîchissement
        sleep(1/framerate)
        
    # fermeture et sortie
    sleep(3)
    ferme_fenetre()
