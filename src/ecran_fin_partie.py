"""
Module pour gérer les écrans de fin de partie (game over et victoire)
"""
import pygame
from src.constantes import screen, XMAX, YMAX
from src.boutons import Bouton
from src.sons import jouer_musique_game_over, jouer_musique_victoire
from src.ecrans import charger_police, charger_fond, creer_overlay

def afficher_ecran_game_over(background_image=None):
    """
    Affiche l'écran de game over avec un bouton pour revenir à l'écran de démarrage
    
    Args:
        background_image (Surface, optional): Image de fond à utiliser
    
    Returns:
        bool: True si le joueur a choisi de revenir au menu, False s'il a fermé le jeu
    """
    # Jouer la musique de game over
    jouer_musique_game_over()
    
    # Chargement des polices
    polices = charger_police()
    
    # Créer le bouton pour revenir au menu
    bouton = Bouton(XMAX/2, YMAX/2 + 30, 145, 25, "Menu principal", polices['bouton'])
    
    # Titre et sous-titre
    titre_surface = polices['titre'].render("GAME OVER", True, (255, 50, 50))
    titre_rect = titre_surface.get_rect(center=(XMAX/2, YMAX/2 - 50))
    
    sous_titre_surface = polices['sous_titre'].render("Vous avez perdu toutes vos vies !", True, (246, 215, 189))
    sous_titre_rect = sous_titre_surface.get_rect(center=(XMAX/2, YMAX/2))
    
    # Utiliser le fond fourni ou charger une image par défaut
    if background_image is None:
        background_image, bg_x, bg_y = charger_fond('assets/background/1.png')
    else:
        bg_x = (XMAX - background_image.get_width()) // 2
        bg_y = (YMAX - background_image.get_height()) // 2
    
    # Créer un overlay semi-transparent rouge pour le fond
    overlay = creer_overlay((255, 50, 50), 40)
    
    clock = pygame.time.Clock()
    
    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quitter le jeu
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if bouton.est_clique(event.pos):
                        return True  # Revenir au menu principal
        
        # Mettre à jour l'état du bouton
        bouton.verifier_survol(pygame.mouse.get_pos())
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Dessiner l'arrière-plan s'il est disponible
        if background_image:
            screen.blit(background_image, (bg_x, bg_y))
        
        # Appliquer l'overlay rouge
        screen.blit(overlay, (0, 0))
        
        # Dessiner le titre et sous-titre
        screen.blit(titre_surface, titre_rect)
        #screen.blit(sous_titre_surface, sous_titre_rect)
        
        # Dessiner le bouton
        bouton.dessiner()
        
        # Rafraîchir l'écran
        pygame.display.flip()
        
        # Limiter à 60 FPS
        clock.tick(60)

def afficher_ecran_victoire(background_image=None):
    """
    Affiche l'écran de victoire avec un bouton pour revenir à l'écran de démarrage
    
    Args:
        background_image (Surface, optional): Image de fond à utiliser
    
    Returns:
        bool: True si le joueur a choisi de revenir au menu, False s'il a fermé le jeu
    """
    # Jouer la musique de victoire
    jouer_musique_victoire()
    
    # Chargement des polices
    polices = charger_police()
    
    # Créer le bouton pour revenir au menu
    bouton = Bouton(XMAX/2, YMAX/2 + 30, 145, 25, "Menu principal", polices['bouton'])
    
    # Titre et sous-titre
    titre_surface = polices['titre'].render("VICTOIRE !", True, (255, 215, 0))
    titre_rect = titre_surface.get_rect(center=(XMAX/2, YMAX/2 - 50))
    
    sous_titre_surface = polices['sous_titre'].render("Vous avez terminé tous les niveaux !", True, (246, 215, 189))
    sous_titre_rect = sous_titre_surface.get_rect(center=(XMAX/2, YMAX/2))
    
    # Utiliser le fond fourni ou charger une image par défaut
    if background_image is None:
        background_image, bg_x, bg_y = charger_fond('assets/background/2.png')
    else:
        bg_x = (XMAX - background_image.get_width()) // 2
        bg_y = (YMAX - background_image.get_height()) // 2
    
    # Créer un overlay semi-transparent doré pour le fond
    overlay = creer_overlay((255, 215, 0), 40)
    
    clock = pygame.time.Clock()
    
    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quitter le jeu
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if bouton.est_clique(event.pos):
                        return True  # Revenir au menu principal
        
        # Mettre à jour l'état du bouton
        bouton.verifier_survol(pygame.mouse.get_pos())
        
        # Effacer l'écran
        screen.fill((0, 0, 0))
        
        # Dessiner l'arrière-plan s'il est disponible
        if background_image:
            screen.blit(background_image, (bg_x, bg_y))
        
        # Appliquer l'overlay doré
        screen.blit(overlay, (0, 0))
        
        # Dessiner le titre et sous-titre
        screen.blit(titre_surface, titre_rect)
        #screen.blit(sous_titre_surface, sous_titre_rect)
        
        # Dessiner le bouton
        bouton.dessiner()
        
        # Rafraîchir l'écran
        pygame.display.flip()
        
        # Limiter à 60 FPS
        clock.tick(60) 