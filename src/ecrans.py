"""
Module contenant des fonctions communes pour les différents écrans du jeu
"""
import pygame
from src.constantes import XMAX, YMAX

def charger_police(noms_polices=None, tailles=None):
    """
    Charge les polices de caractères pour un écran.
    
    Args:
        noms_polices (dict): Dictionnaire des noms de polices pour chaque usage
        tailles (dict): Dictionnaire des tailles de police pour chaque usage
    
    Returns:
        dict: Dictionnaire contenant les polices chargées
    """
    # Valeurs par défaut
    tailles_defaut = {'titre': 24, 'sous_titre': 20, 'bouton': 16}
    if tailles is None:
        tailles = tailles_defaut
    else:
        # S'assurer que toutes les clés par défaut sont présentes
        for key, value in tailles_defaut.items():
            if key not in tailles:
                tailles[key] = value
    
    if noms_polices is None:
        noms_polices = {'titre': 'assets/font.ttf', 'sous_titre': 'assets/font.ttf', 'bouton': 'assets/font.ttf'}
    
    polices = {}
    
    try:
        # Charger les polices personnalisées
        for usage, nom in noms_polices.items():
            if usage in tailles:  # Vérifier que la clé existe dans tailles
                polices[usage] = pygame.font.Font(nom, tailles[usage])
    except FileNotFoundError:
        # Utiliser des polices système en cas d'échec
        polices['titre'] = pygame.font.SysFont('Arial', tailles['titre'])
        polices['sous_titre'] = pygame.font.SysFont('Arial', tailles['sous_titre'])
        polices['bouton'] = pygame.font.SysFont('Arial', tailles['bouton'])
    
    return polices

def charger_fond(image_path='assets/background/1.png'):
    """
    Charge une image de fond et calcule sa position pour être centrée.
    
    Args:
        image_path (str): Chemin vers l'image de fond à charger
    
    Returns:
        tuple: (image, bg_x, bg_y) - Image chargée et coordonnées
    """
    try:
        background_image = pygame.image.load(image_path)
        bg_x = (XMAX - background_image.get_width()) // 2
        bg_y = (YMAX - background_image.get_height()) // 2
    except FileNotFoundError:
        background_image = None
        bg_x = bg_y = 0
    
    return background_image, bg_x, bg_y

def creer_overlay(couleur_base, alpha=40):
    """
    Crée un overlay semi-transparent pour mettre en valeur l'écran.
    
    Args:
        couleur_base (tuple): Couleur RGB de base
        alpha (int): Valeur de transparence (0-255)
    
    Returns:
        Surface: Surface pygame avec transparence
    """
    overlay = pygame.Surface((XMAX, YMAX), pygame.SRCALPHA)
    couleur_rgba = (*couleur_base, alpha)  # Ajouter canal alpha
    overlay.fill(couleur_rgba)
    return overlay 