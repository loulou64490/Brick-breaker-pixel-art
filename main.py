import sys

from classes import *

pygame.init()

pygame.display.set_caption("Casse Briques")

clock = pygame.time.Clock()


class Jeu:
    def __init__(self):
        self.balle = Balle()
        xb, yb, i = 100, 100, 0
        self.liste_briques = []
        fichier = open("briques.txt")
        for ligne in fichier:
            for c in ligne:
                if c == 'b':
                    br = Brique(xb + 75 * i, yb)
                    self.liste_briques.append(br)
                    i += 1
            i = -0.5
            yb += 50
        self.raquette = Raquette()

        self.brique = Brique(400, 100)

    def gestion_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        x = pygame.mouse.get_pos()[0]
        self.balle.deplacer(self.raquette)
        for brique in self.liste_briques:
            if brique.en_vie():
                brique.collision_balle(self.balle)
        self.raquette.deplacer(x)

    def affichage(self):
        screen.fill(NOIR)
        self.balle.afficher()
        self.raquette.afficher()
        for brique in self.liste_briques:
            if brique.en_vie():
                brique.afficher()


jeu = Jeu()
while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()
    pygame.display.flip()
    clock.tick(60)
