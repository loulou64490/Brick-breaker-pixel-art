"""
Module contenant des fonctions communes pour les différents écrans du jeu
"""
import pygame
from src.constantes import XMAX, YMAX, BOUTON_POLICE_NOM, BOUTON_POLICE_TAILLE, BOUTON_PIXEL_PERFECT

def charger_police(noms_polices=None, tailles=None, pixel_perfect=True):
    """
    Charge les polices de caractères pour un écran.
    
    Args:
        noms_polices (dict): Dictionnaire des noms de polices pour chaque usage
        tailles (dict): Dictionnaire des tailles de police pour chaque usage
        pixel_perfect (bool): Si True, configure les polices pour un rendu pixel perfect
    
    Returns:
        dict: Dictionnaire contenant les polices chargées et un dictionnaire d'options de rendu
    """
    # Valeurs par défaut
    tailles_defaut = {'titre': 24, 'bouton': BOUTON_POLICE_TAILLE}
    if tailles is None:
        tailles = tailles_defaut
    else:
        # S'assurer que toutes les clés par défaut sont présentes
        for key, value in tailles_defaut.items():
            if key not in tailles:
                tailles[key] = value
    
    # Forcer la taille du bouton à utiliser la constante globale
    tailles['bouton'] = BOUTON_POLICE_TAILLE
    
    if noms_polices is None:
        noms_polices = {'titre': 'assets/font/title.otf', 'bouton': BOUTON_POLICE_NOM}
    else:
        # Forcer le nom de police du bouton à utiliser la constante globale
        noms_polices['bouton'] = BOUTON_POLICE_NOM
    
    polices = {}
    # Options de rendu pour les textes pixel perfect
    render_options = {}
    
    try:
        # Charger les polices personnalisées
        for usage, nom in noms_polices.items():
            if usage in tailles:  # Vérifier que la clé existe dans tailles
                # S'assurer que les tailles sont des nombres entiers pour un rendu pixel perfect
                if pixel_perfect and tailles[usage] % 2 != 0:
                    tailles[usage] = int(tailles[usage] / 2) * 2  # Arrondir à un multiple de 2
                
                polices[usage] = pygame.font.Font(nom, tailles[usage])
                
                # Configurer les options de rendu pour chaque police
                if usage == 'bouton':
                    # Utiliser la configuration globale pour les boutons
                    render_options[usage] = {'antialias': not BOUTON_PIXEL_PERFECT, 'background': None}
                elif pixel_perfect:
                    # Pour un rendu pixel perfect: pas d'anti-aliasing (False) et pas de couleur de fond (None)
                    render_options[usage] = {'antialias': False, 'background': None}
                else:
                    # Rendu standard avec anti-aliasing
                    render_options[usage] = {'antialias': True, 'background': None}
    except FileNotFoundError:
        # Utiliser des polices système en cas d'échec
        polices['titre'] = pygame.font.SysFont('Arial', tailles['titre'])
        polices['bouton'] = pygame.font.SysFont('Arial', tailles['bouton'])
        
        # Options par défaut pour les polices système
        for usage in ['titre', 'bouton']:
            if usage == 'bouton':
                render_options[usage] = {'antialias': not BOUTON_PIXEL_PERFECT, 'background': None}
            else:
                render_options[usage] = {'antialias': not pixel_perfect, 'background': None}
    
    # Retourner à la fois les polices et les options de rendu
    return polices, render_options

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

def render_pixel_text(police, texte, couleur, render_options=None):
    """
    Rendu d'un texte en mode pixel perfect.
    
    Args:
        police (Font): Police à utiliser pour le rendu
        texte (str): Texte à rendre
        couleur (tuple): Couleur RGB du texte
        render_options (dict): Options de rendu (antialias, background)
    
    Returns:
        Surface: Surface pygame contenant le texte rendu
    """
    if render_options is None:
        render_options = {'antialias': False, 'background': None}
    
    # Rendu du texte
    return police.render(texte, render_options['antialias'], couleur, render_options['background']) 