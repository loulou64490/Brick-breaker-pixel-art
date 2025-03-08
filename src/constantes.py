"""
Constantes pour le jeu Brick Breaker
"""
import pygame

# Dimensions de l'écran
XMIN = 0
YMIN = 0
XMAX = 240
YMAX = 160

# Initialisation de l'écran
pygame.init()
screen = pygame.display.set_mode((XMAX, YMAX), pygame.SCALED) 