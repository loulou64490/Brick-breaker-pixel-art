"""
Module pour la classe Raquette
"""
import pygame
from src.constantes import screen, XMAX, XMIN, YMAX, YMIN

from src.sprites import sprite_images

class Raquette:
    """Classe représentant la raquette contrôlée par le joueur."""
    
    def __init__(self):
        """Initialise une nouvelle raquette."""
        # Utilisation des sprites individuels
        self.sprite_gauche = sprite_images['raquette_gauche']
        self.sprite_milieu = sprite_images['raquette_milieu']
        self.sprite_droite = sprite_images['raquette_droite']
        
        # Dimensions des parties constituantes
        self.larg_gauche = self.sprite_gauche.get_width()
        self.larg_milieu = self.sprite_milieu.get_width()
        self.larg_droite = self.sprite_droite.get_width()
        self.height = self.sprite_milieu.get_height()  # La hauteur est la même pour tous
        
        # Par défaut - raquette normale avec 8 sections milieu
        self.nb_sections_milieu = 8
        self.elargie = False
        
        # Calcul de la largeur totale
        self.width = self.larg_gauche + (self.nb_sections_milieu * self.larg_milieu) + self.larg_droite
        
        # Position
        self.x = XMAX / 2
        self.y = YMAX - self.height/2
        
        # Temps d'élargissement
        self.temps_elargie = 0

    def afficher(self):
        """Affiche la raquette composée de plusieurs sprites."""
        # Position de début (partie gauche)
        x_debut = self.x - self.width/2
        y_pos = self.y - self.height/2
        
        # Afficher la partie gauche
        screen.blit(self.sprite_gauche, (x_debut, y_pos))
        x_courant = x_debut + self.larg_gauche
        
        # Afficher les sections du milieu
        for i in range(self.nb_sections_milieu):
            screen.blit(self.sprite_milieu, (x_courant, y_pos))
            x_courant += self.larg_milieu
            
        # Afficher la partie droite
        screen.blit(self.sprite_droite, (x_courant, y_pos))
    
    def elargir(self):
        """Élargit temporairement la raquette en augmentant le nombre de sections milieu."""
        if not self.elargie:
            # Agrandir la raquette en ajoutant des sections au milieu
            self.nb_sections_milieu = 14  # Augmenter le nombre de sections du milieu
            
            # Recalculer la largeur totale
            self.width = self.larg_gauche + (self.nb_sections_milieu * self.larg_milieu) + self.larg_droite
            
            self.elargie = True
            self.temps_elargie = 600  # 10 secondes à 60 FPS
    
    def mise_a_jour(self):
        """Met à jour l'état de la raquette (bonus temporaires)."""
        if self.elargie:
            self.temps_elargie -= 1
            if self.temps_elargie <= 0:
                # Revenir à la taille normale
                self.nb_sections_milieu = 8
                # Recalculer la largeur totale
                self.width = self.larg_gauche + (self.nb_sections_milieu * self.larg_milieu) + self.larg_droite
                self.elargie = False

    def deplacer(self, x):
        """
        Déplace la raquette horizontalement en limitant sa position à l'écran.
        
        Args:
            x (int): Nouvelle position x souhaitée (généralement la position de la souris)
        """
        # On limite la position x pour que la raquette ne dépasse pas de l'écran
        if x + self.width / 2 > XMAX:
            self.x = XMAX - self.width / 2
        elif x - self.width / 2 < XMIN:
            self.x = XMIN + self.width / 2
        else:
            self.x = x

    def collision_balle(self, balle):
        """
        Vérifie s'il y a collision entre la raquette et la balle.
        
        Args:
            balle (Balle): La balle à tester
            
        Returns:
            bool: True s'il y a collision, False sinon
        """
        horizontal = abs(self.x - balle.x) < balle.width/2 + self.width/2
        vertical = abs(self.y - balle.y) < balle.height/2 + self.height/2
        return horizontal and vertical 