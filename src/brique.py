"""
Module pour la classe Brique
"""
import random
import pygame
from src.constantes import screen
from src.sprites import TYPES_BRIQUES, sprite_images

class Brique:
    """Classe représentant une brique destructible."""
    
    def __init__(self, x, y, type_brique='standard', couleur=None):
        """
        Initialise une nouvelle brique.
        
        Args:
            x (int): Position x du centre de la brique
            y (int): Position y du centre de la brique
            type_brique (str): Type de brique ('standard', 'moyenne', 'petite')
            couleur (str, optional): Couleur de la brique. Si None, une couleur aléatoire est choisie.
        """
        self.x = x  # abscisse du centre de la brique
        self.y = y  # ordonnée du centre de la brique
        self.type_brique = type_brique
        
        # Récupérer les propriétés du type de brique
        self.largeur, self.hauteur, self.vie_max, _ = TYPES_BRIQUES[type_brique]
        self.vie = self.vie_max  # Chaque brique commence avec son nombre maximal de vies
        
        # Si aucune couleur n'est spécifiée, en choisir une aléatoirement
        self.couleur = couleur #si couleur else random.choice(COULEURS_DISPONIBLES)
        
        # Dimensions de la brique
        self.width = self.largeur
        self.height = self.hauteur

        # Probabilité de générer un bonus quand la brique est détruite (en pourcentage)
        self.chance_bonus = 30  # 30% de chance

    def en_vie(self):
        """
        Vérifie si la brique est encore en vie.
        
        Returns:
            bool: True si la brique a encore de la vie, False sinon
        """
        return self.vie > 0

    def afficher(self):
        """Affiche la brique avec le sprite correspondant au niveau de vie actuel."""
        if self.en_vie():
            # Sélectionne le sprite selon le type, le niveau de vie et la couleur
            sprite_name = f'brique{self.type_brique}_{self.vie}_{self.couleur}'
            if sprite_name in sprite_images:
                sprite = sprite_images[sprite_name]
                screen.blit(sprite, (self.x - self.width/2, self.y - self.height/2))

    def collision_balle(self, balle):
        """
        Vérifie et gère la collision avec une balle.
        Si collision, fait rebondir la balle et réduit la vie de la brique.
        
        Args:
            balle (Balle): La balle à tester
            
        Returns:
            tuple: (bool, bool, int, int) - collision, bonus généré, position x du bonus, position y du bonus
        """
        # Pas de collision si la brique est déjà détruite
        if not self.en_vie():
            return False, False, 0, 0
        
        # Vérifier la collision avec la balle en utilisant les dimensions exactes des sprites
        horizontal = abs(self.x - balle.x) < (self.width / 2 + balle.width / 2)
        vertical = abs(self.y - balle.y) < (self.height / 2 + balle.height / 2)
        
        if horizontal and vertical:
            # Déterminer de quel côté vient la balle pour le rebond correct
            dx = balle.x - self.x
            dy = balle.y - self.y
            
            # Calculer les distances de pénétration
            penetration_x = self.width / 2 + balle.width / 2 - abs(dx)
            penetration_y = self.height / 2 + balle.height / 2 - abs(dy)
            
            # Rebond sur l'axe de moindre pénétration
            if penetration_x < penetration_y:
                # Rebond horizontal
                balle.vx = -balle.vx
            else:
                # Rebond vertical
                balle.vy = -balle.vy
            
            # Réduire la vie de la brique
            self.vie -= 1
            
            # Vérifier si la brique est détruite et déterminer si un bonus est généré
            bonus_genere = False
            if not self.en_vie() and random.randint(1, 100) <= self.chance_bonus:
                bonus_genere = True
            
            return True, bonus_genere, self.x, self.y
        
        return False, False, 0, 0 