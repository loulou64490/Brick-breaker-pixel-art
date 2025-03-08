"""
Module pour la gestion des sons du jeu
"""
import pygame

# Initialisation du module son si nécessaire
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Chargement des effets sonores
son_bonus = pygame.mixer.Sound('assets/sound/bonus2.wav')
son_rebond = pygame.mixer.Sound('assets/sound/bounce.wav')
son_explosion = pygame.mixer.Sound('assets/sound/explosion.wav')

# Réglage du volume des effets sonores (valeurs entre 0.0 et 1.0)
son_bonus.set_volume(0.7)
son_rebond.set_volume(0.5)
son_explosion.set_volume(0.6)

def jouer_son_bonus():
    """Joue le son lorsqu'un bonus est récupéré"""
    son_bonus.play()

def jouer_son_rebond():
    """Joue le son lorsque la balle rebondit"""
    #son_rebond.play() # Commenté pour éviter le bruit constant

def jouer_son_explosion():
    """Joue le son lorsqu'une brique se casse"""
    son_explosion.play() 