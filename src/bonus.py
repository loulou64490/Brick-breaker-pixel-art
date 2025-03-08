"""
Module pour la gestion des bonus du jeu
"""
import random
import pygame
from src.constantes import screen, YMAX
from src.sprites import TYPES_BONUS, sprite_images
from src.balle import Balle

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

    def appliquer(self, vies, balles, raquette):
        """
        Applique l'effet d'un bonus ramassé par le joueur.
        
        Args:
            vies (int): Nombre de vies actuelles du joueur
            balles (list): Liste des balles actuellement en jeu
            raquette (Raquette): Raquette du joueur
        
        Returns:
            tuple: (vies, balles) - Nombre de vies mis à jour et liste des balles mise à jour
        """
        if self.type == 'balle_plus':
            # Si le joueur n'a pas de balles actives, la nouvelle balle doit être sur la raquette
            if not balles or all(balle.sur_raquette for balle in balles):
                nouvelle_balle = Balle(raquette.x, raquette.y - raquette.height)
                nouvelle_balle.sur_raquette = True
            else:
                # Sinon, ajouter une nouvelle balle déjà en mouvement
                nouvelle_balle = Balle(raquette.x, raquette.y - raquette.height, 
                                    random.uniform(-1, 1) * 2, -2)
                nouvelle_balle.sur_raquette = False
            balles.append(nouvelle_balle)
            
        elif self.type == 'multi_balles':
            # Dupliquer toutes les balles existantes
            nouvelles_balles = []
            for balle in balles:
                if not balle.sur_raquette:
                    # Créer une balle similaire mais avec un angle légèrement différent
                    vx = balle.vx * 0.9 + random.uniform(-0.5, 0.5)
                    vy = balle.vy * 0.9 + random.uniform(-0.5, 0.5)
                    nouvelle_balle = Balle(balle.x, balle.y, vx, vy)
                    nouvelle_balle.sur_raquette = False
                    nouvelles_balles.append(nouvelle_balle)
            
            # Ajouter les nouvelles balles à la liste
            balles.extend(nouvelles_balles)
            
        elif self.type == 'raquette_large':
            # Élargir temporairement la raquette
            raquette.elargir()
        
        return vies, balles 