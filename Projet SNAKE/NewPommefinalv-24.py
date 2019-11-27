import pygame , sys , random, time
from pygame.locals import *
from Level1collision import*
from Level2collision import*
from Level3collision import*

pygame.mixer.pre_init(44100,16,2,4096)

pygame.init() #Initialisation de pygame


#--------------------------------Parametre------------------------------------------------------

       #---------- creation de la fenetre de jeu----------
Xmax= 1280
Ymax= 720               

       #----------------------Couleurs---------------------
blue = (113,177,227)
blanc = (255,255,255)
black = (0,0,0)
rouge = (200,0,0)
vert = (0,200,0)
rouge_fance =(255,0,0)
vert_fance = (0,255,0)
BLEU_NUIT = (5,5,30)
VERT      = (0,255,0)
JAUNE     = (255,255,0)
       #------------------Gestion niveau-------------------
level = 3
newlevel = 3

       #------------------Gestion vie-------------------
vie = 3
newvie = 3
dansPiege = False
dansPiege2 = False
       #---------------------Level 3----------------------
xmob1=1250
depmob = 0 #Droite
pommepos=1010
deppomme=0
depmob = 0 #Droite
deppomme=0
bossvie = 10
newbossvie = 10
i=0
k=25
clockend = 0
attaquer = False
lose = 1
touche = 0
attaqueOk = False
chute = False
monstr1L3vie = 6
colliMonstre = False
attaqueMonstre = False
monstreMort = False

restart = 0


       #-----------------possition de Newton---------------
#position du joueur
x, y = 0, 0
# Vitesse du joueur
vx, vy = 0, 0
vitesseSaut = 20
  # GravitÃ© vers le bas donc positive
GRAVITE = 2
bouge = 0
endrestart = 0

clock = pygame.time.Clock()

# ----------------------Creation de la fenetre de jeu  ----------------------------------------
             
DISPLAYSURF = pygame.display.set_mode((Xmax,Ymax))
pygame.display.set_caption("New Pomme")

#----------------------- importation de 1er image ---------------------------------------------

newton_image = pygame.image.load('newtonsprite1.png')
newton_attaque = pygame.image.load('spriteattaque.png')

newton_attaqueg = pygame.image.load('spriteattaqueg.png')


       #------------------Surafce/rect associe au image du Newton------------------

newton_rect = pygame.Surface((32, 43))  # taille de l'image
newton_rect.set_alpha(0)                # niveau alpha 
newton_rect.fill((255,255,255))           # on remplie le rectangle


       #------------------Image niveau----------------------
level1 = pygame.image.load('Level 1.jpg')
level2 = pygame.image.load('Level 2.jpg')
level3 = pygame.image.load('Level 3.jpg')

level1porte = pygame.image.load('Level1porte.jpg')
rectlevel1porte = level1porte.get_rect(center=(240,650))

level2porte = pygame.image.load('Level2porte.jpg')
rectlevel2porte = level2porte.get_rect(center=(1050,650))


       #-----------------------------Sprites----------------

marcherVersLaDroite = [pygame.image.load('newtonsprite2.png'),pygame.image.load('newtonsprite3.png'),pygame.image.load('newtonsprite4.png')]
marcherVersLaGauche = [pygame.image.load('newtonspriteg2.png'),pygame.image.load('newtonspriteg3.png'),pygame.image.load('newtonspriteg4.png')]

#-----------------------------Gestion de vie---------------------------------------------------

def afficherVie():
    global score,endrestart
    if vie == 3:                             #si la variable vie en entrant en collision avec les obstacles et les monstres alors on affiche les coeurs en fonction de la valeur de la vie
        DISPLAYSURF.blit(coeur3,(0,20))
        DISPLAYSURF.blit(coeur2,(50,20))
        DISPLAYSURF.blit(coeur1,(100,20))
        endrestart = 0
    elif vie == 2:
        DISPLAYSURF.blit(coeur3,(0,20))
        DISPLAYSURF.blit(coeur2,(50,20))
        endrestart=0
    elif vie == 1:
        DISPLAYSURF.blit(coeur1,(0,20))
        endrestart=0
    elif vie <= 0: #Si la vie atteint 0 alors c'est game over, on affiche une image de game over correspondant au niveau du joueur, on affiche le score total
        endrestart = 1
        if level == 3 and lose == 1:
            DISPLAYSURF.blit(endloselvl3,(0,0))
            afficheScoreGO (score)
        elif level == 2 and lose == 1:
            DISPLAYSURF.blit(endloselvl2,(0,0))
            afficheScoreGO (score)
        elif level == 1 and lose == 1:
            DISPLAYSURF.blit(endloselvl1,(0,0))
            afficheScoreGO (score)


#--------------------------Gestions/changement des nivaux-------------------------------------------------
        
def imgLevel():                               #changement du niveau en fonction des collision
    global level

    if level == 1:                            #on appele tous les fonctions liees au differents niveau
        dessiner_niveau(DISPLAYSURF, niveau)
        DISPLAYSURF.blit(level1, (0,0))
        piegeLevel1 ()
        ramasserPomme()
        pommeCollecteL1()
        afficheScore(score)
        monstre_L1()

    elif level == 2:
        dessiner_niveau2(DISPLAYSURF, niveau2)
        DISPLAYSURF.blit(level2, (0,0))
        piegeLevel2 ()
        ramasserPommeL2()
        afficheScore(score)
        pommeCollecteL2()
        monstre_L2()

    elif level == 3:
        dessiner_niveau3(DISPLAYSURF, niveau3)
        DISPLAYSURF.blit(level3, (0,0))
        boss()
        attaque()
        

def niveauSuivant():                         #changement de nivau si collision avec les portes 
    global level, x, y

    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))    #rect associÃ© au newton

    if rectlevel1porte.colliderect(rectNewton) and level == 1:
        level = 2
        x, y = 264, 100 

    if rectlevel2porte.colliderect(rectNewton) and level == 2:
        level = 3
        x, y = 100, 100


        

def redemarer ():
    global level, x, y,pommeCollecte1,pommeCollecte2,pommeCollecte3,pommeCollecte4,pommeCollecte5,pommeCollecte6,pommeCollecte7,pommeCollecte8,pommeCollecte9,pommeCollecte10,endrestart

            #Resart --> on revenins sur les postions de depart. 
    if level == 1 and restart == 1:
        x, y = 1000, 100
        pommeCollecte1 = 0      #Permet de enlever les pommes 
        pommeCollecte2 = 0
        pommeCollecte3 = 0
        pommeCollecte4 = 0
        pommeCollecte5 = 0
        imgLevel()
        endrestart = 0
            
    if level == 2 and restart == 1:
        x, y = 264, 100
        pommeCollecte6 = 0      #Permet de enlever les pommes 
        pommeCollecte7 = 0
        pommeCollecte8 = 0
        pommeCollecte9 = 0
        pommeCollecte10 = 0
        imgLevel()
        endrestart = 0

    if level == 3 and restart ==1:
        x, y = 100, 100
        endrestart = 0
        

#----------------------------------Level 1------------------------------------------------------

xmonstr1=700
xmonstr2=400
xmonstr3=1180
xmonstr4=700
depmonstr = 0
depmonstr1 = 0
depmonstr2 = 0
depmonstr3 = 0 

cmonstre = False 

mob1=pygame.image.load('mob.png')
mob1_rect= mob1.get_rect(center=(xmob1,385))
mob1phase2=pygame.image.load('steveend2.png')
mob1phase2_rect=mob1phase2.get_rect(center=(xmob1,400))
mob1phase3=pygame.image.load('steveend3.png')
mob1phase3_rect=mob1phase3.get_rect(center=(xmob1,400))

monstr1=pygame.image.load('monst2.png')
monstr1_rect= monstr1.get_rect(center=(xmonstr1,345))

monstr2=pygame.image.load('monst1.png')
monstr2_rect= monstr2.get_rect(center=(xmonstr2,510))

monstr3=pygame.image.load('monst1.png')
monstr3_rect= monstr3.get_rect(center=(xmonstr3,510))

monstr4=pygame.image.load('monst2.png')
monstr4_rect= monstr4.get_rect(center=(xmonstr4,675))


pomme=pygame.image.load('pomme.png')
pomme_rect= pomme.get_rect(center=(pommepos,450))
pomme2=pygame.image.load('pomme.png')
pomme2_rect = pomme.get_rect(center=(pommepos,450))


def monstre_L1():
    global depmonstr, depmonstr1, depmonstr2, depmonstr3, xmonstr1, xmonstr2, xmonstr3, xmonstr4, vie,cmonstre
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    if depmonstr==0 and xmonstr1 < 700:
        xmonstr1 = xmonstr1+2
        monstr1_rect.move_ip(2,0)
    elif depmonstr==1 and xmonstr1 > 300:
        xmonstr1 = xmonstr1-2
        monstr1_rect.move_ip(-2,0)
    if xmonstr1==700: 
        depmonstr=1
    elif xmonstr1==300:
        depmonstr=0
    DISPLAYSURF.blit(monstr1, monstr1_rect)
    if depmonstr1==0 and xmonstr2 < 400:
        xmonstr2 = xmonstr2+2
        monstr2_rect.move_ip(2,0)
    elif depmonstr1==1 and xmonstr2 > 300:
        xmonstr2 = xmonstr2-2
        monstr2_rect.move_ip(-2,0)
    if xmonstr2==400: 
        depmonstr1=1
    elif xmonstr2==300:
        depmonstr1=0
    DISPLAYSURF.blit(monstr2, monstr2_rect)
    if depmonstr2==0 and xmonstr3 < 1180:
        xmonstr3 = xmonstr3+2
        monstr3_rect.move_ip(2,0)
    elif depmonstr2==1 and xmonstr3 > 800:
        xmonstr3 = xmonstr3-2
        monstr3_rect.move_ip(-2,0)
    if xmonstr3==1180: 
        depmonstr2=1
    elif xmonstr3==800:
        depmonstr2=0
    DISPLAYSURF.blit(monstr3, monstr3_rect)
    if depmonstr3==0 and xmonstr4 < 700:
        xmonstr4 = xmonstr4+2
        monstr4_rect.move_ip(2,0)
    elif depmonstr3==1 and xmonstr4 > 100:
        xmonstr4 = xmonstr4-2
        monstr4_rect.move_ip(-2,0)
    if xmonstr4==700: 
        depmonstr3=1
    elif xmonstr4==100:
        depmonstr3=0
    DISPLAYSURF.blit(monstr4, monstr4_rect)
    if not monstr1_rect.colliderect(rectNewton) and not  monstr2_rect.colliderect(rectNewton) and not  monstr3_rect.colliderect(rectNewton) and not monstr4_rect.colliderect(rectNewton) :
        cmonstre = False
    if monstr1_rect.colliderect(rectNewton) and cmonstre == False :
        vie = vie - 1
        cmonstre = True
    if monstr2_rect.colliderect(rectNewton) and cmonstre == False:
        vie = vie - 1
        cmonstre = True
    if monstr3_rect.colliderect(rectNewton) and cmonstre == False:
        vie = vie - 1
        cmonstre = True
    if monstr4_rect.colliderect(rectNewton) and cmonstre == False:
        vie = vie - 1
        cmonstre = True
     

#----------------------------------Level 2------------------------------------------------------

#----------------------------------Level 2------------------------------------------------------

xmonstr1L2=420
xmonstr2L2=430
xmonstr3L2=1180
xmonstr4L2=500
xmonstr1L3=1010
depmonstrL3 = 0
depmonstrL2 = 0
depmonstr1L2 = 0
depmonstr2L2 = 0
depmonstr3L2 = 0 

cmonstre = False 

monstr1L2=pygame.image.load('monst2.png')
monstr1_rectL2= monstr1L2.get_rect(center=(xmonstr1L2,345))

monstr2L2=pygame.image.load('monst1.png')
monstr2_rectL2= monstr2L2.get_rect(center=(xmonstr2L2,510))

monstr3L2=pygame.image.load('monst1.png')
monstr3_rectL2= monstr3L2.get_rect(center=(xmonstr3L2,510))

monstr4L2=pygame.image.load('monst2.png')
monstr4_rectL2= monstr4L2.get_rect(center=(xmonstr4L2,670))

monstr1L3=pygame.image.load('monst1.png')
monstr1_rectL3= monstr1L3.get_rect(center=(xmonstr1L3,460))


def monstre_L2():
    global depmonstrL2, depmonstr1L2, depmonstr2L2, depmonstr3L2, xmonstr1L2, xmonstr2L2, xmonstr3L2, xmonstr4L2, vie,cmonstre
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    if depmonstrL2==0 and xmonstr1L2 < 420:
        xmonstr1L2 = xmonstr1L2+2
        monstr1_rectL2.move_ip(2,0)
    elif depmonstrL2==1 and xmonstr1L2 > 100:
        xmonstr1L2 = xmonstr1L2-2
        monstr1_rectL2.move_ip(-2,0)
    if xmonstr1L2==420: 
        depmonstrL2=1
    elif xmonstr1L2==100:
        depmonstrL2=0
    DISPLAYSURF.blit(monstr1L2, monstr1_rectL2)
    if depmonstr1L2==0 and xmonstr2L2 < 430:
        xmonstr2L2 = xmonstr2L2+2
        monstr2_rectL2.move_ip(2,0)
    elif depmonstr1L2==1 and xmonstr2L2 > 100:
        xmonstr2L2 = xmonstr2L2-2
        monstr2_rectL2.move_ip(-2,0)
    if xmonstr2L2==430: 
        depmonstr1L2=1
    elif xmonstr2L2==100:
        depmonstr1L2=0
    DISPLAYSURF.blit(monstr2L2, monstr2_rectL2)
    if depmonstr2L2==0 and xmonstr3L2 < 1180:
        xmonstr3L2 = xmonstr3L2+2
        monstr3_rectL2.move_ip(2,0)
    elif depmonstr2L2==1 and xmonstr3L2 > 900:
        xmonstr3L2 = xmonstr3L2-2
        monstr3_rectL2.move_ip(-2,0)
    if xmonstr3L2==1180: 
        depmonstr2L2=1
    elif xmonstr3L2==900:
        depmonstr2L2=0
    DISPLAYSURF.blit(monstr3L2, monstr3_rectL2)
    if depmonstr3L2==0 and xmonstr4L2 < 500:
        xmonstr4L2 = xmonstr4L2+2
        monstr4_rectL2.move_ip(2,0)
    elif depmonstr3L2==1 and xmonstr4L2 > 100:
        xmonstr4L2 = xmonstr4L2-2
        monstr4_rectL2.move_ip(-2,0)
    if xmonstr4L2==500: 
        depmonstr3L2=1
    elif xmonstr4L2==100:
        depmonstr3L2=0
    DISPLAYSURF.blit(monstr4L2, monstr4_rectL2)
    if not monstr1_rectL2.colliderect(rectNewton) and not  monstr2_rectL2.colliderect(rectNewton) and not  monstr3_rectL2.colliderect(rectNewton) and not monstr4_rectL2.colliderect(rectNewton) :
        cmonstre = False
    if monstr1_rectL2.colliderect(rectNewton) and cmonstre == False :
        vie = vie - 1
        cmonstre = True
    if monstr2_rectL2.colliderect(rectNewton) and cmonstre == False:
        vie = vie - 1
        cmonstre = True
    if monstr3_rectL2.colliderect(rectNewton) and cmonstre == False:
        vie = vie - 1
        cmonstre = True
    if monstr4_rectL2.colliderect(rectNewton) and cmonstre == False:
        vie = vie - 1
        cmonstre = True

#----------------------------------Level 3------------------------------------------------------
coeur3=pygame.image.load('coeur3.png')
coeur2=pygame.image.load('coeur2.png')
coeur1=pygame.image.load('coeur1.png')

jaugeboss10=pygame.image.load('jaugeboss10.png')
jaugeboss5=pygame.image.load('jaugeboss5.png')
jaugeboss0=pygame.image.load('jaugeboss0.png')
jaugemonstre4=pygame.image.load('jaugemonstre4.png')
jaugemonstre2=pygame.image.load('jaugemonstre2.png')

endwin=pygame.image.load('endwin.png')
endloselvl3=pygame.image.load('endloselvl3.jpg')
endloselvl2=pygame.image.load('endloselvl2.jpg')
endloselvl1=pygame.image.load('endloselvl1.jpg')

tombe = pygame.image.load('tombe.png')

win=pygame.image.load('index.jpg')

mob1=pygame.image.load('mob.png')
mob1_rect= mob1.get_rect(center=(xmob1,385))


pomme=pygame.image.load('pomme.png')
pomme_rect= pomme.get_rect(center=(pommepos,450))


def boss():
    global depmob, xmob1, bossvie, newbossvie, gameend, clockend, i, lose, touche, x, y, attaqueOk
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    
    if depmob==0 and xmob1 < 1250: #Depmob indique si le personnage va à gauche ou à droite, ceci pour le faire se déplacer à gauche ou à droite en fonction de sa position extrème
        xmob1 = xmob1+1 #Incrémentation de 1 à la position pour déplacer le personnage
        mob1_rect.move_ip(1,0)
        mob1phase2_rect.move_ip(1,0) #Déplacement des rectangles correspondant aux différentes phases de vie du boss
        mob1phase3_rect.move_ip(1,0)
    elif depmob==1 and xmob1 > 1220:
        xmob1 = xmob1-1
        mob1_rect.move_ip(-1,0)
        mob1phase2_rect.move_ip(-1,0)
        mob1phase3_rect.move_ip(-1,0)
    
    if xmob1==1250: #Condition pour savoir si on va à gauche ou à droite
        depmob=1
    elif xmob1<=1220: 
        depmob=0
   
    if bossvie>5: #Affiche un sprite différent selon le niveau de vie du boss correspondant à ses "phases"
        DISPLAYSURF.blit(mob1,mob1_rect)
    elif bossvie<=5 and bossvie>1:
        DISPLAYSURF.blit(mob1phase2, mob1phase2_rect)
    else:
        DISPLAYSURF.blit(mob1phase3, mob1phase3_rect)
        

    if rectNewton.colliderect(mob1_rect) and touche == 1: #Gestion de la vie du boss, 10 coups sont nécessaires pour le tuer
        chute = False
        bossvie = newbossvie - 1
        attaqueOk = True
    else:
        newbossvie = bossvie

    if bossvie>5: #Gestion de la jauge de vie du boss en fonction de sa variable vie
        DISPLAYSURF.blit(jaugeboss10,(1060, 20))
    elif bossvie > 0:
        DISPLAYSURF.blit(jaugeboss5,(1060,20))
    elif bossvie <= 0:
        lose = 0 #Permet d'afficher l'écran de fin de jeu "gagnant"
        clockend = 1 #Permet d'enclencher une horloge qui fermera le programme à i=200 après avoir gagné
        DISPLAYSURF.blit(jaugeboss0,(1060,20))
        DISPLAYSURF.blit(endwin,(0,0))
        
    if clockend == 1: #Horloge en question
        i = i + 1
    
    if i == 200: #Fermeture du programme
        pygame.quit()
        quit()
    
def attaque():
    global deppomme, pommepos, vie, newvie, xmonstr1L3, depmonstrL3, monstr1L3vie, monstreMort, colliMonstre, attaqueMonstre, k
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    
    if deppomme==0 and pommepos < 1250 : #Déplacement de la pomme à gauche ou à droite en fonction de ses position extrèmes
        pommepos = pommepos + 7 #modification des coordonnées de la pomme et déplacement de son rectangle
        pomme_rect.move_ip(7,0)
    elif deppomme==1 and pommepos > 50:
        pommepos = pommepos-15
        pomme_rect.move_ip(-15,0)

    if pommepos>=1250: #Permet de définir si la pomme va à gauche ou à droit en fonction des coordonnées atteintes
        deppomme=1
    elif pommepos<=50:
        deppomme=0

    if pomme_rect.colliderect(rectNewton): #Gestion de la collision avec Newton, une collision correspond à un coeur en moins
        vie = newvie - 1
    else:
        newvie = vie    
    DISPLAYSURF.blit(pomme, pomme_rect)
    
    if bossvie <= 5: #Si la vie du boss arrive à 5, alors il fait apparaitre un monstre supplémentaire.
        k = k + 1 #Horloge qui permet de définir un couldown
        if depmonstrL3==0 and xmonstr1L3 < 900 : #Déplacement du monstre à gauche ou à droite
            xmonstr1L3 = xmonstr1L3 + 6 #Modification des coordonnées et déplacement du rectangle associé à l'image
            monstr1_rectL3.move_ip(6,0)
        elif depmonstrL3==1 and xmonstr1L3 > 300:
            xmonstr1L3 = xmonstr1L3-6
            monstr1_rectL3.move_ip(-6,0)

        if xmonstr1L3>=900: #Condition pour savoir si on va à gauche ou à droite
            depmonstrL3=1
        elif xmonstr1L3<=300:
            depmonstrL3=0
 
        if monstreMort == False: #Condition si le monstre est encore en vie c-à-d que la vie du boss>5 et que le joueur n'a pas mis la vie du monstre à 0
            if monstr1_rectL3.colliderect(rectNewton): #Gestion des collisions et des dégats fait soit à Newton soit au monstre
                if colliMonstre == False and touche != 1 and attaqueMonstre == False:
                    vie = vie - 1
                    colliMonstre = True
                elif colliMonstre == False and touche == 1 and k >= 15:
                    k = 0
                    monstr1L3vie = monstr1L3vie - 1
                    attaqueMonstre = True
                    print (monstr1L3vie)
            else:
                colliMonstre = False #réinitialisation des paramètres
                attaqueMonstre = False         
                  
            if monstr1L3vie  >=3: #Gestion de la jauge de vie en fonction de la variable vie du monstre
                DISPLAYSURF.blit(jaugemonstre4,(xmonstr1L3 - 45, 420))
            elif monstr1L3vie <=3 and monstr1L3vie > 0:
                DISPLAYSURF.blit(jaugemonstre2,(xmonstr1L3 - 45, 420))
            elif monstr1L3vie <=0:
                monstreMort = True #Le monstre est mort
            DISPLAYSURF.blit(monstr1L3, monstr1_rectL3)
        if monstreMort == True:
            depmonstrL3 = 5 #On bloque le déplacement du monstre et on affiche à la place une pierre tombale à la position de la mort du mob
            DISPLAYSURF.blit(tombe,(xmonstr1L3, 405))

# movement deNewton lorsqu'il attaque SteveJobs
def ejection():
    global x,y,attaqueOk, chute
    if attaqueOk == True and x >= 100:    #Si on attaque et qu'il y a contact avec le boss alors Newton est renvoyé en l'air jusqu'à une position donnée
        x = x-13
        if y > 125 and chute == False:
            y = y-22
        else:
            chute = True
        if x <= 200:
            attaqueOk = False
    
#----------------------------------Pieges par les niveaux------------------------------------------------------

       #------------------CrÃ©ation des piÃ©ges---------------------------------

sang = pygame.image.load('sang.png')

               #Les trois piege du niveau 1
        
piege_1L1 = pygame.Surface((25, 20)) 
piege_1L1.set_alpha(0)              
piege_1L1.fill((255,255,255))

piege_2L1 = pygame.Surface((25, 15)) 
piege_2L1.set_alpha(0)              
piege_2L1.fill((255,255,255))

piege_3L1 = pygame.Surface((25, 20)) 
piege_3L1.set_alpha(0)              
piege_3L1.fill((255,255,255))

              #Affichage et collision des pieges du niveau 1
def piegeLevel1 ():
    global x, y, vie, viePiege, dansPiege
    
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    
    piege_Rect1L1 =  DISPLAYSURF.blit(piege_1L1, (755,363))          #placement des piege deja definit

    piege_Rect2L1 = DISPLAYSURF.blit(piege_2L1, (460,535))

    piege_Rect3L1 = DISPLAYSURF.blit(piege_3L1, (725,700))

    if not  piege_Rect1L1.colliderect(rectNewton) and not piege_Rect2L1.colliderect(rectNewton) and not  piege_Rect3L1.colliderect(rectNewton):
        dansPiege = False
    if piege_Rect1L1.colliderect(rectNewton) and dansPiege == False:
            vie = vie - 1
            DISPLAYSURF.blit(sang, (755 , 363))
            dansPiege = True
            
    if piege_Rect2L1.colliderect(rectNewton)and dansPiege == False:
            vie = vie - 1
            DISPLAYSURF.blit(sang, (450 , 530))
            dansPiege = True

    if piege_Rect3L1.colliderect(rectNewton)and dansPiege == False:
            vie = vie - 1
            DISPLAYSURF.blit(sang, (716 , 695))
            dansPiege = True 

               #Les trois piege du niveau 2
            
piege_1L2 = pygame.Surface((25, 20)) 
piege_1L2.set_alpha(0)              
piege_1L2.fill((255,255,255))

piege_2L2 = pygame.Surface((25, 20)) 
piege_2L2.set_alpha(0)              
piege_2L2.fill((255,255,255))

piege_3L2 = pygame.Surface((25, 20)) 
piege_3L2.set_alpha(0)              
piege_3L2.fill((255,255,255))

              #Affichage et collision des pieges du niveau 2

def piegeLevel2 ():
    global x, y, vie, viePiege,dansPiege2
    
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    
    piege_Rect1L2 =  DISPLAYSURF.blit(piege_1L2, (493,375))

    piege_Rect2L2 = DISPLAYSURF.blit(piege_2L2, (790,540))

    piege_Rect3L2 = DISPLAYSURF.blit(piege_3L2, (525,700))
    if not  piege_Rect1L2.colliderect(rectNewton) and not piege_Rect2L2.colliderect(rectNewton) and not  piege_Rect3L2.colliderect(rectNewton):
        dansPiege2 = False

    if piege_Rect1L2.colliderect(rectNewton) and dansPiege2 == False:
            vie = vie - 1
            DISPLAYSURF.blit(sang, (488 , 375))
            dansPiege2 = True
    if piege_Rect2L2.colliderect(rectNewton)and dansPiege2 == False:
            vie = vie - 1
            DISPLAYSURF.blit(sang, (790 , 540))
            dansPiege2 = True
    if piege_Rect3L2.colliderect(rectNewton)and dansPiege2 == False:
            vie = vie - 1
            DISPLAYSURF.blit(sang, (520 , 695))
            dansPiege2 = True

#----------------------------------Pomme/score par niveaux------------------------------------------------------
                #niveau 1

cPomme = False
tscore1 = 0              #Garder le score a 5 meme s'il y'a plusieurs fois collision
tscore2 = 0
tscore3 = 0
tscore4 = 0
tscore5 = 0

score = 0


pommeCollecte1 = 0      #Permet de enlever les pommes 
pommeCollecte2 = 0
pommeCollecte3 = 0
pommeCollecte4 = 0
pommeCollecte5 = 0
                        #image et positions des pommes

pomme1L1 = pygame.image.load('pomme1.png')
pomme1L1_rect = pomme1L1.get_rect(center=(100,340))

pomme2L1 = pygame.image.load('pomme1.png')
pomme2L1_rect = pomme2L1.get_rect(center=(500,340))

pomme3L1 = pygame.image.load('pomme1.png')
pomme3L1_rect = pomme3L1.get_rect(center=(515,505))

pomme4L1 = pygame.image.load('pomme1.png')
pomme4L1_rect = pomme4L1.get_rect(center=(1200,505))

pomme5L1 = pygame.image.load('pomme1.png')
pomme5L1_rect = pomme5L1.get_rect(center=(700,675))


def ramasserPomme():
    global pommeCollecte1,pommeCollecte2,pommeCollecte3,pommeCollecte4,pommeCollecte5, score, newscore, cPomme, tscore1, tscore2, tscore3, tscore4, tscore5
    
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    DISPLAYSURF.blit(pomme1L1, pomme1L1_rect)
    DISPLAYSURF.blit(pomme2L1, pomme2L1_rect)
    DISPLAYSURF.blit(pomme2L1, pomme3L1_rect)
    DISPLAYSURF.blit(pomme2L1, pomme4L1_rect)
    DISPLAYSURF.blit(pomme2L1, pomme5L1_rect)
        
    if pomme1L1_rect.colliderect(rectNewton) :
        score = score + 5
        score = score
        tscore2 = tscore2 + 1
        if tscore2 > 1:
            score = score - 5
        pommeCollecte1 = 1
     
    
    if pomme2L1_rect.colliderect(rectNewton) :
        score = score + 5
        pommeCollecte2 = 1
        tscore1 = tscore1 + 1
        if tscore1 > 1:
            score = score - 5
  

    if pomme3L1_rect.colliderect(rectNewton) :
        score = score + 5
        pommeCollecte3 = 1
        tscore3 = tscore3 + 1
        if tscore3 > 1:
            score = score - 5
       
    if pomme4L1_rect.colliderect(rectNewton):
        score = score + 5
        pommeCollecte4 = 1
        tscore4 = tscore4 + 1
        if tscore4 > 1:
            score = score - 5
        
    if pomme5L1_rect.colliderect(rectNewton) :
        score = score + 5
        pommeCollecte5 = 1
        tscore5 = tscore5 + 1
        if tscore5 > 1:
            score = score - 5
         

hidepomme = pygame.image.load('hidepomme.png')  
     
def pommeCollecteL1():
    global  pommeCollecte1,pommeCollecte2,pommeCollecte3,pommeCollecte4,pommeCollecte5
    if pommeCollecte1 == 1:
        DISPLAYSURF.blit(hidepomme,(80,295))
    if pommeCollecte2 == 1:
        DISPLAYSURF.blit(hidepomme,(480,295))
    if pommeCollecte3 == 1:
        DISPLAYSURF.blit(hidepomme,(500,460))
    if pommeCollecte4 == 1:
        DISPLAYSURF.blit(hidepomme,(1150,460))
    if pommeCollecte5 == 1:
        DISPLAYSURF.blit(hidepomme,(650,627))

               #niveau 2
hidepomme1 = pygame.image.load('hidepomme1.jpg')
hidepomme2 = pygame.image.load('hidepomme2.jpg')
hidepomme3 = pygame.image.load('hidepomme3.jpg')
hidepomme4 = pygame.image.load('hidepomme4.jpg')

tscore6 = 0              #Garder le score a 5 meme s'il y'a plusieurs fois collision
tscore7 = 0
tscore8 = 0
tscore9 = 0
tscore10 = 0

pommeCollecte6 = 0      #Permet de enlever les pommes 
pommeCollecte7 = 0
pommeCollecte8 = 0
pommeCollecte9 = 0
pommeCollecte10 = 0
pommrCollecte11 = 0
                      

pomme1L2 = pygame.image.load('pomme1.png')
pomme1L2_rect = pomme1L2.get_rect(center=(100,340))

pomme2L2 = pygame.image.load('pomme1.png')
pomme2L2_rect = pomme2L2.get_rect(center=(1190,340))

pomme3L2 = pygame.image.load('pomme1.png')
pomme3L2_rect = pomme3L2.get_rect(center=(150,505))

pomme4L2 = pygame.image.load('pomme1.png')
pomme4L2_rect = pomme4L2.get_rect(center=(750,505))

pomme5L2 = pygame.image.load('pomme1.png')
pomme5L2_rect = pomme5L2.get_rect(center=(200,675))

goldpomme = pygame.image.load('pomme2.png')
goldpomme_rect = pomme5L2.get_rect(center=(1200,125))



def ramasserPommeL2():
    global pommeCollecte6,pommeCollecte7,pommeCollecte8,pommeCollecte9,pommeCollecte10,pommrCollecte11, score, newscore,tscore6,tscore7,tscore8,tscore9,tscore10, vie
    
    rectNewton = DISPLAYSURF.blit(newton_rect, (x,y))
    DISPLAYSURF.blit(pomme1L2, pomme1L2_rect)
    DISPLAYSURF.blit(pomme2L2, pomme2L2_rect)
    DISPLAYSURF.blit(pomme2L2, pomme3L2_rect)
    DISPLAYSURF.blit(pomme2L2, pomme4L2_rect)
    DISPLAYSURF.blit(pomme2L2,pomme5L2_rect)
    DISPLAYSURF.blit(goldpomme,goldpomme_rect)

    if pomme1L2_rect.colliderect(rectNewton):
       score = score + 5
       pommeCollecte6 = 1
       tscore6 = tscore6 + 1
       if tscore6 > 1:
           score = score - 5
    
    if pomme2L2_rect.colliderect(rectNewton):
       score = score + 5
       pommeCollecte7 = 1
       tscore7 = tscore7 + 1
       if tscore7 > 1:
           score = score - 5

    if pomme3L2_rect.colliderect(rectNewton):
       score = score + 5
       pommeCollecte8 = 1
       tscore8 = tscore8 + 1
       if tscore8 > 1:
           score = score - 5
           
    if pomme4L2_rect.colliderect(rectNewton):
       score = score + 5
       pommeCollecte9 = 1
       tscore9 = tscore9 + 1
       if tscore9 > 1:
           score = score - 5

    if pomme5L2_rect.colliderect(rectNewton):
       score = score + 5
       pommeCollecte10 = 1
       tscore10 = tscore10 + 1
       if tscore10 > 1:
           score = score - 5

    if goldpomme_rect.colliderect(rectNewton):
        vie = 3
        pommrCollecte11 = 1
        
def pommeCollecteL2():
    global  pommeCollecte6,pommeCollecte7,pommeCollecte8,pommeCollecte9,pommeCollecte10,pommrCollecte11
    if pommeCollecte6 == 1:
        DISPLAYSURF.blit(hidepomme1,(80,295))
    if pommeCollecte7 == 1:
        DISPLAYSURF.blit(hidepomme1,(1130,295))
    if pommeCollecte8 == 1:
        DISPLAYSURF.blit(hidepomme3,(130,460))
    if pommeCollecte9 == 1:
        DISPLAYSURF.blit(hidepomme2,(730,480))
    if pommeCollecte10 == 1:
        DISPLAYSURF.blit(hidepomme4,(180,635))
    if pommrCollecte11 == 1:
        DISPLAYSURF.blit(hidepomme1,(1200,100))

                #score
smallfont = pygame.font.SysFont('comicsansms', 20)    #Font score
smallfont2 = pygame.font.SysFont('comicsansms', 40) 

def afficheScore (s):
    text = smallfont.render('Score: ' + str(s), True, rouge_fance) 
    DISPLAYSURF.blit(text, (1170, 0))
    
        
def afficheScoreGO (s):
    global vie
    text2 = smallfont2.render('Votre Score: ' + str(s), True, rouge_fance)
    if vie == 0:
        DISPLAYSURF.blit(text2, (480, 550))


#--------------------------------Histoire-------------------------------------------------------

entrer = 0
histoire1 = pygame.image.load('Histoire Part 1.png')
histoire2 = pygame.image.load('Histoire Part 2.png')

def histoire():
    global entrer
    if entrer == 0:
        DISPLAYSURF.blit(histoire1, (0, 0))

    if entrer == 1:
        DISPLAYSURF.blit(histoire2, (0, 0))

    if entrer == 3:
        newPomme()
    if entrer > 3:
        newPomme()
        
    

#--------------------------------Creation menu--------------------------------------------------

fondMenu = pygame.image.load('fondMenu.jpg')

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def quitgame():
    pygame.quit()
    quit()

def button_demarage(msg,x,y,l,h,c,cf,action = None):      # ou x et y sont les positions associÃ© au rectangle de button et l et h sont largeur et hauteur / c et cf = couleur et couleur fance
    
         #-------------detection de click du souris et on appele la fonction newPomme------------
    
    mouse = pygame.mouse.get_pos()                
    click = pygame.mouse.get_pressed()
    
    if x + l > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, cf,(x,y,l,h))
    else:
        pygame.draw.rect(DISPLAYSURF, c,(x,y,l,h))
        if click[0] == 1 and action != None:
            action()                            #On donne comme paramettre soit le fonction newPomme ou quite on fonction du click
                
        #-----------affichage du texte sur les buttons----------------------- 
    textButton = pygame.font.Font('freesansbold.ttf',20)
    textSurf, textRect = text_objects(msg,textButton)
    textRect.center = ((x +(l/2)), y+(h/2))
    DISPLAYSURF.blit(textSurf, textRect)
        
        
    #----Creation du menu + on appele la fonction button avec differents parametres des rectangles----
    
def menu_demarage():
    

    demarage = True

    while demarage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
             #------------------Affichage de menu----------------------
        
        DISPLAYSURF.blit(fondMenu, (0,0))

            #----------------Creation des rectangles------------------
        
        button_demarage('Play',253,550,100,50,vert,vert_fance,quit)
        button_demarage('Quit',920,550,100,50,rouge,rouge_fance,newPomme)
       
        
        pygame.display.update()
        clock.tick(15)

#----------------------------------------Fonction et boucle principale------------------------------------------


def newPomme():
    global x, y, vx, vy, level, newlevel, vie, newvie, vitesseSaut, GRAVITE, touche, restart, entrer, bossvie
    
    #-----------------------------------------Parametre liee au boucle principale----------------
    game_over = False
    
    
    level = 1
    x, y = 1000, 100


    limiteChute = 720    
    nbSaut = 0         #limiter nb du saut
    
            #---------------------Sprites----------------------
    droite = False
    gauche = False
    pas = 0
    nbImPas = 10        # vitesse de deffilement des sprites


    #-------------------------------- Boucle principale ---------------------------------------------------------

    while not game_over :
        global bouge
        imgLevel()
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    nbSaut +=1
                    if nbSaut < 8:
                        vy = -20
                    
                if event.key == K_RIGHT:                                  # on verifie l'atruibut Key de notre Ã©venement (flÃ©che vers le haut,en bas...)
                    vx = 5
                    droite = True
                    bouge = 1
                elif event.key == K_LEFT:
                    vx = -5
                    gauche = True
                    bouge = 1
            
                if event.key == K_a:                                      # Attaque
                    touche = 1
                if event.key == K_r and endrestart == 1:
                    restart = 1

                if event.key == K_RETURN:
                    entrer = entrer + 1
                    print (entrer)
                    
            elif event.type == KEYUP:                                     # si l'utlisateur relache le tpuche il faut que le personnage s'arrete
                if event.key == K_RIGHT:
                    vx = 0                                                #on dÃ©crimente notre acceleration, donc notre vitesse reviens Ã  0.
                    droite = False
                    bouge = 0
                
                elif event.key == K_LEFT:
                    vx = 0
                    gauche = False
                    bouge = 0


                if event.key == K_a:                                      # Attaque
                    touche = 0
                if event.key == K_r:
                    restart = 0
        
            # Sauvegarde de l'ancienne position ( donc s'il y collision on replace notre personnage Ã  l'ancienne position)
        old_x, old_y = x, y
        vy += GRAVITE
        vy = min(vitesseSaut, vy) # vy ne peut pas dÃ©passer 25 sinon effet tunnel...
        if vy == vitesseSaut:
            nbSaut = 0
            
        x += vx
        y += vy
             # Limite jusqu'oÃ¹ le personnage peut tomber
        y = min(limiteChute, y)
       
    #--------------------redemarer/restart------------------------------    
        if restart == 1:
            vie = 3
            bossvie = 10
    #---------------------Plateformes-----------------------------------     

                     #Collision des plateformes en fonction du niveau
        if level == 1:
            x, y, vx, vy = bloque_sur_collision(niveau, (old_x, old_y), (x, y), vx, vy)

        elif level == 2:
            x, y, vx, vy = bloque_sur_collision2(niveau2, (old_x, old_y), (x, y), vx, vy)

        elif level == 3:
            x, y, vx, vy = bloque_sur_collision3(niveau3, (old_x, old_y), (x, y), vx, vy)

       
    #---------------------Sprites-----------------------------------     
        if (droite == False and gauche == False): #Gestion des sprites, à gauche ou à droite
            DISPLAYSURF.blit(newton_image, (x , y))
            
        if pas + 1 >= 3*nbImPas:
            pas = 0

        if (droite and gauche):
            DISPLAYSURF.blit(newton_image, (x , y))
                
        else:
            if bouge == 0 and touche == 1 and not gauche and not droite:
                DISPLAYSURF.blit(newton_attaque,(x,y))
            if droite:
                if touche == 1:
                    DISPLAYSURF.blit(newton_attaque,(x, y))
                else:
                    DISPLAYSURF.blit(marcherVersLaDroite[int(pas//(nbImPas))], (x , y))       #on fait deffiller toutes les images de la liste quant on apuie sur la fleche droite
                pas += 1
                
            if gauche:
                if touche == 1:
                    DISPLAYSURF.blit(newton_attaqueg,(x-15,y))
                else:
                    DISPLAYSURF.blit(marcherVersLaGauche[int(pas//(nbImPas))], (x , y))
                pas += 1
                
         
        #--------------------------------Fonctions---------------
        histoire()
        afficherVie()
        niveauSuivant()
        redemarer ()
        pygame.display.update()
        clock.tick(60)#FPS
        ejection()
        

menu_demarage()

pygame.quit()
sys.exit()
