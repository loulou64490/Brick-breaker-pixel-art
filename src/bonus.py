"""
Module pour la classe Bonus
"""
import random
import pygame
from src.constantes import screen, YMAX
from src.sprites import TYPES_BONUS, sprite_images

class Bonus:
    """Classe représentant un bonus qui tombe d'une brique détruite."""
    
    def __init__(self, x, y):
        """
        Initialise un nouveau bonus à la position spécifiée.
        
        Args:
            x (int): Position x initiale
            y (int): Position y initiale
        """
        # Choisir un type de bonus au hasard
        self.type = random.choice(list(TYPES_BONUS.keys()))
        self.sprite = sprite_images[self.type]
        self.width, self.height = self.sprite.get_size()
        self.x = x
        self.y = y
        self.vitesse = 1  # Vitesse de chute
        self.actif = True  # Le bonus est actif tant qu'il n'est pas ramassé ou perdu
        
    def deplacer(self):
        """Fait tomber le bonus vers le bas de l'écran."""
        self.y += self.vitesse
        # Désactiver le bonus s'il sort de l'écran
        if self.y > YMAX + self.height:
            self.actif = False
            
    def collision_raquette(self, raquette):
        """
        Vérifie si le bonus entre en collision avec la raquette.
        
        Args:
            raquette (Raquette): La raquette à tester
            
        Returns:
            bool: True s'il y a collision, False sinon
        """
        horizontal = abs(self.x - raquette.x) < (self.width/2 + raquette.width/2)
        vertical = abs(self.y - raquette.y) < (self.height/2 + raquette.height/2)
        return horizontal and vertical
            
    def afficher(self):
        """Affiche le bonus à sa position actuelle."""
        if self.actif:
            screen.blit(self.sprite, (self.x - self.width/2, self.y - self.height/2)) 