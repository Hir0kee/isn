import pygame
from pygame.locals import *
import random
import pickle
import time
import os

## Définition du chemin d'accès de chaque image
pathDoodle = os.path.join("assets", "perso1.png")
pathWhite = os.path.join("assets", "white.png")
pathBg = os.path.join("assets", "800background.jpg")
pathJump = os.path.join("assets", "jump.png")
pathCoin = os.path.join("assets", "coin.png")
pathOwl = os.path.join("assets", "owl.png")
pathMonkey = os.path.join("assets", "monkey.png")
pathOctopus = os.path.join("assets", "octopus.png")
pathCheck = os.path.join("assets", "check.png")

##Initialisation de pygame
pygame.init()

##Classe permettant de garder en mémoire des variables, pour qu'elle ne soient pas réinitialisées à chaque mort.
class mem:
    coin = 0 #Nombre de pièces
    achete =[0,0,0] #0 si l'item n'a pas été acheté, 1 s'il a été acheté
    perso = pygame.image.load(pathDoodle) #Apparence utilisée

##Création de la classe "Menu"
class Menu:
##Initialisation de toutes les vairables/configurations grâce à __init__
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 800))
        self.white = (255, 255, 255)
        self.font = pygame.font.Font("BradBunR.ttf", 100)
        pygame.display.set_caption('Box Test')
        pygame.display.update()

    def menu(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((self.white))
            clock.tick(30)

            ##Création de evennements qui vont lancer les diférentes classes en fonction de l'endroit où le joueur a cliqué
            for event in pygame.event.get():
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                if (event.type == pygame.MOUSEBUTTONDOWN) & (287 < x < 513) & (300 + 10 < y < 410):
                    Jeu.run()
                if (event.type == pygame.MOUSEBUTTONDOWN) & (287 < x < 513) & (410 < y < 510):
                    Jeu.shop()
                if (event.type == pygame.MOUSEBUTTONDOWN) & (287 < x < 513) & (510 < y < 610):
                    Jeu.save()

            ##Lancement de chaque fonctions associée à un bouton
            self.playButton()
            self.shopButton()
            self.saveButton()

            ##Actualisation de l'affichage
            pygame.display.flip()

    ##Création des fonctions qui créent les boutons
    def playButton(self):
        self.screen.blit(self.font.render('Play !', True, (0, 0, 0)), (307, 300))
        pygame.draw.rect(self.screen, (0, 0, 0), (307 - 20, 300 + 10, 93 * 2 + 40, 100), 2)

    def shopButton(self):
        self.screen.blit(self.font.render('Shop ', True, (0, 0, 0)), (307, 400))
        pygame.draw.rect(self.screen, (0, 0, 0), (307 - 20, 400 + 10, 93 * 2 + 40, 100), 2)

    def saveButton(self):
        self.screen.blit(self.font.render('Save ', True, (0, 0, 0)), (400 - 93, 500))
        pygame.draw.rect(self.screen, (0, 0, 0), (307 - 20, 500 + 10, 93 * 2 + 40, 100), 2)

##Définition de la classe du jeu
class Jeu:
    ##Initialisation de toutes les vairables/configurations grâce à __init__
    def __init__(self):
        self.direction = 0
        self.mort1 = 0
        self.rect = 3
        self.screen = pygame.display.set_mode((800, 800))
        self.check = pygame.image.load(pathCheck).convert_alpha()
        self.plat = pygame.image.load(pathWhite).convert_alpha()
        self.bg = pygame.image.load(pathBg).convert_alpha()
        self.imgJump = pygame.image.load(pathJump).convert_alpha()
        self.imgCoin = pygame.image.load(pathCoin).convert_alpha()
        self.imgOwl = pygame.image.load(pathOwl).convert_alpha()
        self.imgMonkey = pygame.image.load(pathMonkey).convert_alpha()
        self.imgOctopus = pygame.image.load(pathOctopus).convert_alpha()
        self.xDood = 800 / 2 - 86 / 2
        self.yDood = 800 - 200
        self.xMouvement = 0
        self.yMouvement = -20
        self.platMouvement = 0
        self.score = 0
        self.yPlat = []
        self.xPlat = []
        self.white = (255, 255, 255)
        self.spawnDouble = 0
        self.xDouble = random.randint(0, 750)
        self.yDouble = random.randint(0, 750)
        self.time = 0
        self.spawnCoin = 0
        self.money = 0
        self.xCoin = random.randint(0, 750)
        self.yCoin = random.randint(0, 750)
        self.vieSaut = 5
        self.font = pygame.font.Font("BradBunR.ttf", 50)
        pygame.display.set_caption('Jumpy')

    ##Boucle principale du jeu
    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.blit(self.bg, (0, 0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Menu.menu()
            self.plateform()
            self.argent()
            self.doodle()
            self.scor()
            self.doublejump()

            ##Si la position du personnage dépasse le point le plus bas de la fenêtre, la variable self.mort1 passe à 1,
            # l'écran Game Over est affiché, et tant que mort1==1, l'affichage du jeu n'est pas actualisé
            if (self.yDood) > 800:
                self.mort1 = 1
                self.mort()
            if self.mort1 == 0:
                pygame.display.update()

            ##Comme la boucle fontctionne en continu, on fait incrémenter une variable à l'infini afin d'obtenir un
            # système de temps
            self.time += 1

    ##Boutique pour changer l'apparence
    def shop(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((self.white))
            clock.tick(30)
            for event in pygame.event.get():
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    Menu.menu()

                ##Création des evennements qui vont permettre au joueur d'acheter des apparences, tout en vérifiant la
                # position de la souris, si l'item séléctionné n'a pas déjà été acheté et si le joueur à suffisemment
                # d'argent pour l'acheter.
                if (event.type == pygame.MOUSEBUTTONDOWN) and (0<x<86) and (0<y<150) and (mem.coin >= 10 or mem.achete[0] == 1):
                    mem.perso=pygame.image.load(pathOwl).convert_alpha()
                    if mem.achete[0] ==0:
                        mem.coin -= 10
                    mem.achete[0] = 1
                    self.rect=0
                if (event.type == pygame.MOUSEBUTTONDOWN) and (87<x<172) and (0<y<150) and (mem.coin >= 20 or mem.achete[1] == 1):
                    mem.perso=pygame.image.load(pathMonkey).convert_alpha()
                    if mem.achete[1] == 0:
                        mem.coin -= 20
                    mem.achete[1] = 1
                    self.rect=1
                if (event.type == pygame.MOUSEBUTTONDOWN) and (173<x<258) and (0<y<150) and (mem.coin >= 50 or mem.achete[2] == 1):
                    mem.perso=pygame.image.load(pathOctopus).convert_alpha()
                    if mem.achete[2] == 0:
                        mem.coin -= 50
                    mem.achete[2] = 1
                    self.rect=2

            ##Création des evennements qui vont afficher un rectangle autour de l'apparence séléctionnée
            if self.rect == 0:
                pygame.draw.rect(self.screen, (0, 0, 0), (2, 2, 86, 150), 2)
            elif self.rect == 1:
                pygame.draw.rect(self.screen, (0, 0, 0), (86, 2, 86, 150), 2)
            elif self.rect ==2:
                pygame.draw.rect(self.screen, (0, 0, 0), (172, 2, 86, 150), 2)

            ##Prévisualisation des apparences
            self.screen.blit(self.font.render(str(mem.coin), True, (0, 0, 0)), (770, 29))
            self.screen.blit(self.imgCoin, (800 - 2 * 38, 45))
            self.screen.blit(self.imgOwl, (0, 0))
            self.screen.blit(self.imgMonkey, (90, 0))
            self.screen.blit(self.imgOctopus, (180, 0))

            ##Affichage des prix (si l'item n'a pas encore été acheté) ou du "check" vert si l'item à été acheté
            if mem.achete[0] == 0:
                self.screen.blit(self.font.render("10", True, (255, 0, 0)), (20, 180))
            else :
                self.screen.blit(self.check, (56, 0))

            if mem.achete[1] == 0:
                self.screen.blit(self.font.render("20", True, (255, 0, 0)), (85, 180))
            else:
                self.screen.blit(self.check, (142, 0))
            if mem.achete[2] == 0:
                self.screen.blit(self.font.render("50", True, (255, 0, 0)), (185, 180))
            else:
                self.screen.blit(self.check, (228, 0))

            pygame.display.update()

    ##Création de la fonction gérant la physique du personnage sachant que l'ont a initialisé l'accellération yMouvement à -13
    def doodle(self):
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xMouvement < 5:  # On ajoute cette condition pourque l'accellération sur x ne soit pas infinie
                self.xMouvement += 1
        elif key[K_LEFT]:
            if self.xMouvement > -5:
                self.xMouvement -= 1

        # Permet d'arreter le  perso sur x si aucune touche n'est pressée
        else:
            if self.xMouvement > 0:
                self.xMouvement -= 1
            elif self.xMouvement < 0:
                self.xMouvement += 1

        # Avec une accel. initiale de -13, on incrémente cette accel pour faire ralentir l'accélération, puis l'augmenter quand self.yMouvement dépassera 0
        self.yMouvement += 0.5

        # Permet au personnage de passer sur un bord de l'écran, puis de le faire revenir de l'autre coté
        if self.xDood < -43:
            self.xDood = 850
        elif self.xDood > 850:
            self.xDood = -43

        # Si le personnage va en haut de l'écran, il réapparait en bas avec une bonne accélératon
        if self.yDood + 150 < 0:
            self.yDood, self.yMouvement = 800, -20

        # La position x et y du personnage dépend de son accélération
        self.yDood += self.yMouvement
        self.xDood += self.xMouvement

        # Affichage du personnage
        self.screen.blit(mem.perso, (self.xDood, self.yDood))

    ##Génération des plateformes ainsi qu leur déplacement
    def plateform(self):
        for i in range(0, 12): #On crée 13 plateforme qui seront à la position i dans les tableaux xPLat[] et yPlat[] définis au paravant
            self.yPlat.append(random.randint(i * 60, i * 60 + 60))
            self.xPlat.append((random.randint(0, 700)))

            ##Collisions entre le personnage et une plateforme
            if (self.yPlat[i] + 20 >= self.yDood + 150 >= self.yPlat[i]) & (
                (self.xPlat[i] < self.xDood < self.xPlat[i] + 100) or (
                    self.xPlat[i] < self.xDood + 86 < self.xPlat[i] + 100)) & (self.yDood + 150 > 0) & (
                self.yMouvement > 0):
                self.yMouvement = -13.5

            ##Accélération de la descente des plateforme en fonction de la position du joueur
            if self.yDood <= 400 - 150:
                self.platMouvement = 2
            elif self.yDood > 500 - 150:
                self.platMouvement = 0
            if self.yDood <= 150:
                self.platMouvement = 4

            ## Une fois les plateformes passées en dessous, elles réaparaissent en haut, mais avec des positions différentes
            if self.yPlat[i] > 800:
                self.yPlat[i] = random.randint(-90, 0)
                self.xPlat[i] = random.randint(0, 700)
            self.yPlat[i] = self.yPlat[i] + self.platMouvement
            self.screen.blit(self.plat, (self.xPlat[i], self.yPlat[i]))

    ##Calcul et affichage du score
    def scor(self):
        for i in range(0, 12):
            if self.yPlat[i] >= 800: #Le score augemente de 10 à chaque fois qu'une plateforme passe sous l'écran
                self.score += 10
        self.screen.blit(self.font.render(str(self.score), True, (194, 181, 164)), (0, 0))

    ##Apparition aléatoire des doubles-sauts
    def doublejump(self):
        ##A un intervalle de 60 unités de temps, on regarde si un nombre généré entre 0 et 100 est inférieur à 10.
        # Si c'est le cas, alors un double-saut apparait. On a donc une chance de 10% toutes les 60 unités de temps
        # qu'un double saut apparaisse. On empêche aussi que plusieurs doubles-sauts n'apparaissent.
        if (self.time % 60 == 0) & (self.spawnDouble == 0):
            self.xDouble = random.randint(0, 750)
            self.yDouble = random.randint(0, 750)
            self.probd = random.randint(0, 100)
            if self.probd < 10:
                self.spawnDouble = 1
            else:
                self.spawnDouble = 0
        #Le nommbre de double sauts augmente si le joueur rentre en collision avec
        if (self.xDood + 86 > self.xDouble + 15 > self.xDood) & (self.yDood + 150 > self.yDouble + 15 > self.yDood) & (self.spawnDouble == 1):
            self.spawnDouble = 0
            self.vieSaut += 1

        ##Si la condition d'apparition est validée, alors on affiche le double saut à l'écran
        if self.spawnDouble == 1:
            self.screen.blit(self.imgJump, (self.xDouble, self.yDouble))

        ##Affichage du nombre de doubles-sauts restants
        self.screen.blit(self.imgJump, (800 - 2 * 38, 10))
        self.screen.blit(self.font.render(str(self.vieSaut), True, (194, 181, 164)), (770, -6))

        ##Le joueur peut réinitialiser son accéleration à -13,5 en appuyant sur "espace" tant qu'il a des vies
        if (pygame.key.get_pressed()[K_SPACE]) & (self.yMouvement > 0) & (self.vieSaut > 0):
            self.yMouvement = -13.5
            self.vieSaut -= 1

    ##Apparition aléatoire des pièces (similaire à celle des doubles-sauts)
    def argent(self):
        if (self.time % 60 == 0) & (self.spawnCoin == 0):
            self.xCoin = random.randint(0, 750)
            self.yCoin = random.randint(0, 750)
            self.probc = random.randint(0, 100)
            if self.probc < 10:
                self.spawnCoin = 1
            else:
                self.spawnCoin = 0


        if (self.xDood + 86 > self.xCoin + 15 > self.xDood) & (self.yDood + 150 > self.yCoin + 15 > self.yDood) & (
            self.spawnCoin == 1):
            self.spawnCoin = 0
            mem.coin += 10

        if self.spawnCoin == 1:
            self.screen.blit(self.imgCoin, (self.xCoin, self.yCoin))

        self.screen.blit(self.font.render(str(mem.coin), True, (194, 181, 164)), (770, 29))
        self.screen.blit(self.imgCoin, (800 - 2 * 38, 45))

    ##Apparition de l'écran Game Over
    def mort(self):
        while True:

            self.screen.fill((self.white))
            self.screen.blit(self.font.render("GAME OVER", True, (255, 0, 0)), (300, 200))
            self.screen.blit(self.font.render('Back to menu', True, (0, 0, 0)), (273, 300))

            ##Si le joueur clique sur le bouton, on réinitialise toutes les variables/configurations de __init__, et on
            # le renvoie au menu
            for event in pygame.event.get():
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                if (event.type == pygame.MOUSEBUTTONUP):
                    x, y = pygame.mouse.get_pos()
                if (event.type == pygame.MOUSEBUTTONDOWN) & (254 < x < 529) & (324 < y < 350):
                    self.__init__()
                    Menu.menu()

            pygame.display.update()





if __name__ == '__main__':
    Menu = Menu()
    Jeu = Jeu()
    Menu.menu()
