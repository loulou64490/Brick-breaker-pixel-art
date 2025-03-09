"""
Module pour gérer les boutons d'interface utilisateur
"""
import pygame
from src.constantes import screen, BOUTON_PIXEL_PERFECT
from src.ecrans import render_pixel_text

class Bouton:
    """Classe générique représentant un bouton dans l'interface utilisateur"""
    
    def __init__(self, x, y, largeur, hauteur, texte, police, 
                 couleur=(14, 41, 62), couleur_survol=(31, 57, 79), couleur_bordure=(31, 57, 79)):
        """Initialise un nouveau bouton
        
        Args:
            x (int): Position x du centre du bouton
            y (int): Position y du centre du bouton
            largeur (int): Largeur du bouton
            hauteur (int): Hauteur du bouton
            texte (str): Texte à afficher sur le bouton
            police (Font): Police utilisée pour le texte
            couleur (tuple): Couleur RGB du bouton à l'état normal
            couleur_survol (tuple): Couleur RGB du bouton lorsqu'il est survolé
            couleur_bordure (tuple): Couleur RGB de la bordure du bouton
        """
        self.rect = pygame.Rect(x - largeur/2, y - hauteur/2, largeur, hauteur)
        self.couleur = couleur
        self.couleur_survol = couleur_survol
        self.couleur_bordure = couleur_bordure
        self.texte = texte
        self.police = police
        self.est_survole = False
    
    def dessiner(self):
        """Dessine le bouton sur l'écran"""
        couleur = self.couleur_survol if self.est_survole else self.couleur
        
        # Dessiner le fond du bouton
        pygame.draw.rect(screen, couleur, self.rect, border_radius=8)
        
        # Dessiner la bordure
        pygame.draw.rect(screen, self.couleur_bordure, self.rect, width=2, border_radius=8)
        
        # Dessiner le texte avec le mode pixel perfect si activé
        if BOUTON_PIXEL_PERFECT:
            texte_surface = render_pixel_text(self.police, self.texte, (255, 255, 255))
        else:
            texte_surface = self.police.render(self.texte, True, (255, 255, 255))
            
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        screen.blit(texte_surface, texte_rect)
    
    def verifier_survol(self, pos_souris):
        """Vérifie si la souris survole le bouton
        
        Args:
            pos_souris (tuple): Position (x, y) de la souris
            
        Returns:
            bool: True si la souris est sur le bouton, False sinon
        """
        self.est_survole = self.rect.collidepoint(pos_souris)
        return self.est_survole
    
    def est_clique(self, pos_clic):
        """Vérifie si le bouton est cliqué
        
        Args:
            pos_clic (tuple): Position (x, y) du clic
            
        Returns:
            bool: True si le bouton est cliqué, False sinon
        """
        return self.rect.collidepoint(pos_clic) 