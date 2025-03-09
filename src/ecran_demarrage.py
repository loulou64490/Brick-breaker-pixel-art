"""
Module pour gérer l'écran de démarrage du jeu
"""
import pygame
import sys
from src.constantes import screen, XMAX, YMAX
from src.boutons import Bouton
from src.sons import jouer_musique_demarrage
from src.ecrans import charger_police, charger_fond, render_pixel_text

def afficher_ecran_demarrage():
    """
    Affiche l'écran de démarrage avec un bouton pour lancer le jeu
    
    Returns:
        bool: True si le joueur a choisi de commencer le jeu, False sinon
    """
    # Jouer la musique de l'écran de démarrage
    jouer_musique_demarrage()
    
    # Chargement des polices
    tailles = {'titre': 24}
    polices, render_options = charger_police(tailles=tailles)
    
    # Créer le bouton de démarrage
    bouton_jouer = Bouton(XMAX/2, YMAX/2 + 30, 45, 18, "Jouer", polices['bouton'])
    
    # Créer le bouton Quitter
    bouton_quitter = Bouton(XMAX/2, YMAX/2 + 60, 55, 18, "Quitter", polices['bouton'])
    
    # Titre du jeu - utiliser render_pixel_text pour un rendu pixel perfect
    titre_surface_1 = render_pixel_text(
        polices['titre'], 
        "BRICK", 
        (246,215,189), 
        render_options['titre']
    )
    titre_surface_2 = render_pixel_text(
        polices['titre'], 
        "BREAKER", 
        (246,215,189), 
        render_options['titre']
    )
    titre_rect_1 = titre_surface_1.get_rect(center=(XMAX/2, YMAX/2 - 45))
    titre_rect_2 = titre_surface_2.get_rect(center=(XMAX/2, YMAX/2 - 15))
    
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
                    if bouton_jouer.est_clique(event.pos):
                        return True  # Commencer le jeu
                    elif bouton_quitter.est_clique(event.pos):
                        pygame.quit()
                        sys.exit()
        
        # Mettre à jour l'état des boutons
        pos_souris = pygame.mouse.get_pos()
        bouton_jouer.verifier_survol(pos_souris)
        bouton_quitter.verifier_survol(pos_souris)
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Dessiner l'arrière-plan s'il est disponible
        if background_image:
            screen.blit(background_image, (bg_x, bg_y))
        
        # Dessiner le titre
        screen.blit(titre_surface_1, titre_rect_1)
        screen.blit(titre_surface_2, titre_rect_2)
        
        # Dessiner les boutons
        bouton_jouer.dessiner()
        bouton_quitter.dessiner()
        
        # Rafraîchir l'écran
        pygame.display.flip()
        
        # Limiter à 60 FPS
        clock.tick(60) 