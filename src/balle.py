"""
Module pour la classe Balle
"""
import math
import pygame
from src.constantes import screen, XMAX, XMIN, YMAX, YMIN
from src.sprites import sprite_images

class Balle:
    """Classe représentant la balle du jeu."""
    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        """
        Initialise une nouvelle balle.
        
        Args:
            x (int, optional): Position x initiale. Si None, position par défaut.
            y (int, optional): Position y initiale. Si None, position par défaut.
            vx (float, optional): Vitesse x initiale. Si None, la balle est sur la raquette.
            vy (float, optional): Vitesse y initiale. Si None, la balle est sur la raquette.
        """
        self.x = x if x is not None else 400
        self.y = y if y is not None else 400
        self.vx = vx
        self.vy = vy
        self.vitesse = 3
        self.sur_raquette = vx is None or vy is None  # Si pas de vitesse spécifiée, la balle est sur la raquette
        self.sprite = sprite_images['balle']
        
        # Définir la taille exacte en fonction du sprite
        self.width, self.height = self.sprite.get_size()
        self.rayon = self.width / 2  # Pour les calculs de collision circulaire
        
        # Initialiser la vitesse avec un angle par défaut si la balle n'est pas sur la raquette
        if not self.sur_raquette:
            self.vitesse = math.sqrt(vx**2 + vy**2)  # Garder la même norme de vitesse
        else:
            self.vitesse_par_angle(60)

    def vitesse_par_angle(self, angle):
        """
        Définit la vitesse de la balle en fonction d'un angle.
        
        Args:
            angle (float): Angle en degrés (0° = droite, 90° = haut)
        """
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def afficher(self):
        """Affiche la balle à sa position actuelle."""
        screen.blit(self.sprite, (self.x - self.width/2, self.y - self.height/2))

    def rebond_raquette(self, raquette):
        """
        Calcule le rebond de la balle sur la raquette.
        L'angle dépend de la position de la balle par rapport au centre de la raquette.
        
        Args:
            raquette (Raquette): La raquette avec laquelle la balle entre en collision
        """
        # Écart horizontal entre le centre de la raquette et la balle
        diff = raquette.x - self.x
        
        # Écart tangent (basé sur les sprites)
        longueur_totale = raquette.width / 2 + self.width / 2
        
        # Formule où l'angle est proportionnel à l'écart au centre de la raquette
        angle = 90 + 80 * diff / longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette):
        """
        Déplace la balle et gère les rebonds sur les murs et la raquette.
        
        Args:
            raquette (Raquette): La raquette du joueur
        Returns:
            bool: True si la balle est perdue, False sinon
        """
        perdue = False
        
        if self.sur_raquette:
            # On met la balle sur la raquette
            self.y = raquette.y - self.height/2 - raquette.height/2
            self.x = raquette.x
        else:
            # Déplacement de la balle
            self.x += self.vx
            self.y += self.vy
            
            # Gestion des collisions
            # Avec la raquette
            if raquette.collision_balle(self) and self.vy > 0:  # Collision et balle descendante
                self.rebond_raquette(raquette)
                
            # Avec les bords de l'écran
            if self.x + self.width/2 > XMAX:
                self.vx = -self.vx
                self.x = XMAX - self.width/2  # Éviter que la balle sorte de l'écran
            
            if self.x - self.width/2 < XMIN:
                self.vx = -self.vx
                self.x = XMIN + self.width/2  # Éviter que la balle sorte de l'écran
            
            if self.y + self.height/2 > YMAX:
                self.sur_raquette = True
                perdue = True  # Indique que la balle est perdue
            
            if self.y - self.height/2 < YMIN:
                self.vy = -self.vy
                self.y = YMIN + self.height/2  # Éviter que la balle sorte de l'écran
                
        return perdue 