"""
Module de gestion des sprites pour le jeu Brick Breaker
"""
import pygame
from src.constantes import screen

# Liste des couleurs disponibles pour les briques
COULEURS_DISPONIBLES = ['bleue', 'verte', 'jaune', 'orange', 'rouge', 'violette']

# Structure pour les types de briques:
# 'type': (largeur, hauteur, nombre_de_vies, {couleur: (x_base, y_base)})
# où x_base et y_base sont les coordonnées de la première brique (niveau de vie max)
TYPES_BRIQUES = {
    'standard': (32, 9, 3, {
        'bleue': (0, 7),
        'verte': (0, 23),
        'jaune': (0, 39),
        'orange': (0, 55),
        'rouge': (0, 71),
        'violette': (0, 87)
    }),
    'moyenne': (32, 16, 3, {
        'bleue': (112, 0),
        'verte': (112, 16),
        'jaune': (112, 32),
        'orange': (112, 48),
        'rouge': (112, 64),
        'violette': (112, 80)
    }),
    'petite': (16, 16, 2, {
        'bleue': (224, 0),
        'verte': (224, 16),
        'jaune': (224, 32),
        'orange': (224, 48),
        'rouge': (224, 64),
        'violette': (224, 80)
    })
}

# Types de bonus disponibles avec leurs positions dans le sprite sheet
TYPES_BONUS = {
    'balle_plus': ('sprites', 112, 27, 8, 8),   # Bonus de nouvelle balle
    'multi_balles': ('sprites', 112, 43, 8, 8), # Bonus multiplication des balles
    'raquette_large': ('sprites', 112, 91, 8, 8) # Bonus raquette élargie
}

# Dictionnaire contenant les positions et tailles des sprites dans les sprite sheets
sprites = {
    'balle': ('sprites', 144, 8, 8, 8),
    'raquette': ('sprites', 64, 7, 32, 9),
    'raquette_gauche': ('raquette', 96, 7, 4, 9),
    'raquette_milieu': ('raquette', 112, 7, 3, 9),
    'raquette_droite': ('raquette', 128, 7, 4, 9),
    'vie3': ('hearts', 115, 3, 11, 10),  # Ajout du sprite pour les vies
    'vie2': ('hearts', 82, 3, 11, 10),  # Ajout du sprite pour les vies
    'vie1': ('hearts', 34, 3, 11, 10),  # Ajout du sprite pour les vies
}

# Ajouter les bonus au dictionnaire de sprites
for nom_bonus, (sheet_name, x, y, width, height) in TYPES_BONUS.items():
    sprites[nom_bonus] = (sheet_name, x, y, width, height)

# Génération automatique des sprites pour tous les types de briques
for type_brique, (largeur, hauteur, nb_vies, positions) in TYPES_BRIQUES.items():
    for couleur, (x_base, y_base) in positions.items():
        for niveau in range(nb_vies, 0, -1):
            # Calculer la position X en fonction du niveau de vie et de la position de base
            x = x_base + (nb_vies - niveau) * largeur
            
            # Ajouter au dictionnaire
            nom_sprite = f'brique{type_brique}_{niveau}_{couleur}'
            sprites[nom_sprite] = ('bricks', x, y_base, largeur, hauteur)

# Dictionnaire pour stocker les différentes sprite sheets
sprite_sheets = {
    'sprites': pygame.image.load('assets/paddles_and_balls.png').convert_alpha(),
    'hearts': pygame.image.load('assets/hearts.png').convert_alpha(),
    'bricks': pygame.image.load('assets/bricks.png').convert_alpha(),
    'raquette': pygame.image.load('assets/paddle_part.png').convert_alpha(),
}

# Fonction pour extraire un sprite de la sprite sheet
def get_sprite(name):
    """
    Extrait un sprite spécifique d'une sprite sheet.
    
    Args:
        name (str): Nom du sprite à extraire
        
    Returns:
        Surface: L'image du sprite extraite
    """
    sheet_name, x, y, width, height = sprites[name]
    sprite_sheet = sprite_sheets[sheet_name]
    rect = pygame.Rect(x, y, width, height)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sprite_sheet, (0, 0), rect)
    return image

# Précharger les images des sprites
sprite_images = {name: get_sprite(name) for name in sprites} 