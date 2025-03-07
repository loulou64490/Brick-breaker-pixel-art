import math

import pygame  # Le module Pygame

from constantes import *

screen = pygame.display.set_mode((width, height))


class Balle:
    def __init__(self):
        self.vx, self.vy = None, None
        self.x, self.y = 400, 400
        self.vitesse = 4
        self.vitesse_par_angle(60)
        self.sur_raquette = True

    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def afficher(self):
        pygame.draw.rect(screen, BLANC, (self.x - RAYON_BALLE, self.y - RAYON_BALLE, 2 * RAYON_BALLE, 2 * RAYON_BALLE),
                         0)

    def rebond_raquette(self, raquette):
        diff = raquette.x - self.x  # On calcule l'écart horizontal
        longueur_totale = raquette.longueur / 2 + RAYON_BALLE  # écart tangent
        angle = 90 + 80 * diff / longueur_totale  # formule où l'angle est proportionnel à l'écart au centre de la raquette
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette):
        if self.sur_raquette:  # On met la balle sur la raquette
            self.y = raquette.y - 2 * RAYON_BALLE
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
            if raquette.collision_balle(self) and self.vy > 0:  # Il y a collision et la balle descend
                self.rebond_raquette(raquette)
            if self.x + RAYON_BALLE > XMAX:
                self.vx = -self.vx
            if self.x - RAYON_BALLE < XMIN:
                self.vx = -self.vx
            if self.y + RAYON_BALLE > YMAX:
                self.sur_raquette = True
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy


class Raquette:
    def __init__(self):
        self.x, self.y = XMAX / 2, YMAX - RAYON_BALLE
        self.longueur = 10 * RAYON_BALLE

    def afficher(self):
        pygame.draw.rect(screen, BLANC,
                         (self.x - self.longueur / 2, self.y - RAYON_BALLE, self.longueur, 2 * RAYON_BALLE), 0)

    def deplacer(self, x):
        # On limite la position x pour que la raquette ne dépasse pas de l'écran
        if x + self.longueur / 2 > XMAX:
            self.x = XMAX - self.longueur / 2
        elif x - self.longueur / 2 < XMIN:
            self.x = XMIN + self.longueur / 2
        else:
            self.x = x

    def collision_balle(self, balle):
        horizontal = abs(self.x - balle.x) < RAYON_BALLE + self.longueur / 2
        vertical = abs(self.y - balle.y) < 2 * RAYON_BALLE
        return horizontal and vertical


class Brique:
    def __init__(self, x, y):
        self.x = x  # abscisse du centre de la brique
        self.y = y
        self.vie = 1
        self.longueur = 5 * RAYON_BALLE  # longueur de la brique
        self.largeur = 3 * RAYON_BALLE  # largeur de la brique

    def en_vie(self):
        return self.vie > 0  # renvoie True ou False

    def afficher(self):
        pygame.draw.rect(screen, BLANC,
                         (self.x - self.longueur / 2, self.y - self.largeur / 2, self.longueur, self.largeur), 0)

    def collision_balle(self, balle):
        # on suppose que largeur<longueur
        marge = self.largeur / 2 + RAYON_BALLE  # La balle est tangente aux côtés droit et gauche de la brique
        dy = balle.y - self.y  # Écart avec le bas et le haut de la brique
        touche = False
        if balle.x >= self.x:  # on regarde a droite
            dx = balle.x - (self.x + self.longueur / 2 - self.largeur / 2)
            if abs(dy) <= marge and dx <= marge:  # on touche
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else:  # a droite
                    balle.vx = -balle.vx
        else:  # on regarde a gauche
            dx = balle.x - (self.x - self.longueur / 2 + self.largeur / 2)
            if abs(dy) <= marge and -dx <= marge:  # on touche
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else:  # a gauche
                    balle.vx = -balle.vx
        if touche:
            self.vie -= 1
        return touche
