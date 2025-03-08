"""
Module pour gérer l'écran de démarrage du jeu
"""
import pygame
from src.constantes import screen, XMAX, YMAX
from src.boutons import Bouton
from src.sons import jouer_musique_demarrage
from src.ecrans import charger_police, charger_fond

def afficher_ecran_demarrage():
    """
    Affiche l'écran de démarrage avec un bouton pour lancer le jeu
    
    Returns:
        bool: True si le joueur a choisi de commencer le jeu, False sinon
    """
    # Jouer la musique de l'écran de démarrage
    jouer_musique_demarrage()
    
    # Chargement des polices
    tailles = {'titre': 24, 'bouton': 16}
    polices = charger_police(tailles=tailles)
    
    # Créer le bouton de démarrage
    bouton = Bouton(XMAX/2, YMAX/2 + 30, 65, 25, "JOUER", polices['bouton'])
    
    # Titre du jeu
    titre_surface = polices['titre'].render("BRICK BREAKER", True, (246,215,189))
    titre_rect = titre_surface.get_rect(center=(XMAX/2, YMAX/2 - 30))
    
    # Charger une image de fond
    background_image, bg_x, bg_y = charger_fond('assets/background/1.png')
    
    clock = pygame.time.Clock()
    
    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quitter le jeu
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if bouton.est_clique(event.pos):
                        return True  # Commencer le jeu
        
        # Mettre à jour l'état du bouton
        bouton.verifier_survol(pygame.mouse.get_pos())
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Dessiner l'arrière-plan s'il est disponible
        if background_image:
            screen.blit(background_image, (bg_x, bg_y))
        
        # Dessiner le titre
        screen.blit(titre_surface, titre_rect)
        
        # Dessiner le bouton
        bouton.dessiner()
        
        # Rafraîchir l'écran
        pygame.display.flip()
        
        # Limiter à 60 FPS
        clock.tick(60) 