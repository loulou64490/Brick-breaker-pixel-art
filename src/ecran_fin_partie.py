"""
Module pour gérer les écrans de fin de partie (game over et victoire)
"""
import pygame
from src.constantes import screen, XMAX, YMAX
from src.boutons import Bouton
from src.sons import jouer_musique_game_over, jouer_musique_victoire
from src.ecrans import charger_police, charger_fond, creer_overlay

# Dictionnaire décrivant les différents types d'écrans de fin de partie
CONFIGS_ECRANS = {
    "game_over": {
        "titre": "GAME OVER",
        "couleur_titre": (255, 50, 50),  # Rouge
        "sous_titre": "",
        "couleur_sous_titre": (246, 215, 189),
        "couleur_overlay": (255, 50, 50),  # Rouge
        "image_fond": 'assets/background/1.png',
        "musique": jouer_musique_game_over
    },
    "victoire": {
        "titre": "VICTOIRE !",
        "couleur_titre": (255, 215, 0),  # Doré
        "sous_titre": "",
        "couleur_sous_titre": (246, 215, 189),
        "couleur_overlay": (255, 215, 0),  # Doré
        "image_fond": 'assets/background/2.png',
        "musique": jouer_musique_victoire
    }
    # Possibilité d'ajouter d'autres types d'écrans ici facilement
}

def afficher_ecran_fin_partie(type_ecran="game_over", background_image=None):
    """
    Affiche un écran de fin de partie générique avec un bouton pour revenir à l'écran de démarrage
    
    Args:
        type_ecran (str): Type d'écran à afficher ("game_over", "victoire", etc.)
        background_image (Surface, optional): Image de fond à utiliser
    
    Returns:
        bool: True si le joueur a choisi de revenir au menu, False s'il a fermé le jeu
    """
    # Récupérer la configuration pour ce type d'écran
    if type_ecran not in CONFIGS_ECRANS:
        type_ecran = "game_over"  # Type par défaut
    
    config = CONFIGS_ECRANS[type_ecran]
    
    # Jouer la musique appropriée
    if "musique" in config and callable(config["musique"]):
        config["musique"]()
    
    # Chargement des polices
    polices = charger_police()
    
    # Créer le bouton pour revenir au menu
    bouton = Bouton(XMAX/2, YMAX/2 + 30, 145, 25, "Menu principal", polices['bouton'])
    
    # Titre et sous-titre
    titre_surface = polices['titre'].render(config["titre"], True, config["couleur_titre"])
    titre_rect = titre_surface.get_rect(center=(XMAX/2, YMAX/2 - 50))
    
    # Préparer le sous-titre si présent
    sous_titre_surface = None
    sous_titre_rect = None
    if "sous_titre" in config:
        sous_titre_surface = polices['sous_titre'].render(
            config["sous_titre"], 
            True, 
            config.get("couleur_sous_titre", (246, 215, 189))
        )
        sous_titre_rect = sous_titre_surface.get_rect(center=(XMAX/2, YMAX/2))
    
    # Utiliser le fond fourni ou charger une image par défaut
    if background_image is None and "image_fond" in config:
        background_image, bg_x, bg_y = charger_fond(config["image_fond"])
    elif background_image is None:
        background_image, bg_x, bg_y = charger_fond()
    else:
        bg_x = (XMAX - background_image.get_width()) // 2
        bg_y = (YMAX - background_image.get_height()) // 2
    
    # Créer un overlay semi-transparent pour le fond
    overlay = creer_overlay(config.get("couleur_overlay", (255, 255, 255)), 40)
    
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
        
        # Appliquer l'overlay
        screen.blit(overlay, (0, 0))
        
        # Dessiner le titre
        screen.blit(titre_surface, titre_rect)
        
        # Dessiner le sous-titre si présent
        if sous_titre_surface and sous_titre_rect:
            screen.blit(sous_titre_surface, sous_titre_rect)
        
        # Dessiner le bouton
        bouton.dessiner()
        
        # Rafraîchir l'écran
        pygame.display.flip()
        
        # Limiter à 60 FPS
        clock.tick(60)

# Fonctions de compatibilité pour éviter de casser le code existant
def afficher_ecran_game_over(background_image=None):
    """
    Fonction de compatibilité qui appelle la version générique avec le type game_over
    """
    return afficher_ecran_fin_partie("game_over", background_image)

def afficher_ecran_victoire(background_image=None):
    """
    Fonction de compatibilité qui appelle la version générique avec le type victoire
    """
    return afficher_ecran_fin_partie("victoire", background_image) 