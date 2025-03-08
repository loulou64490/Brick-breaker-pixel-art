"""
Module contenant les fonctions d'affichage du jeu
"""
import pygame
from src.constantes import screen, XMAX, YMAX
from src.sprites import sprite_images

def afficher_vies(vies, XMAX):
    """
    Affiche les icônes de vie en haut à droite de l'écran.
    
    Args:
        vies (int): Nombre de vies actuelles du joueur
        XMAX (int): Largeur maximale de l'écran
    """
    if vies <= 0:
        return  # Pas de vies à afficher
        
    # Déterminer le sprite principal selon le nombre de vies (1, 2 ou 3+)
    if vies >= 3:
        sprite_principal = sprite_images['vie3']
        vies_principales = 3
    elif vies == 2:
        sprite_principal = sprite_images['vie2']
        vies_principales = 2
    else:  # vies == 1
        sprite_principal = sprite_images['vie1']
        vies_principales = 1
    
    # Calculer combien de vies supplémentaires il faut afficher
    vies_restantes = vies - vies_principales
    
    largeur_vie = sprite_principal.get_width()
    hauteur_vie = sprite_principal.get_height()
    marge = 5  # Espacement entre les icônes
    
    # Position pour le sprite principal (en haut à droite de l'écran)
    x = XMAX - largeur_vie - 10  # 10 pixels de marge par rapport au bord droit
    y = 10
    
    # Afficher le sprite principal
    screen.blit(sprite_principal, (x, y))
    
    # Afficher les vies supplémentaires de façon optimisée
    while vies_restantes > 0:
        x -= (largeur_vie + marge)
        
        if vies_restantes >= 3:
            # Utiliser un coeur de 3 vies
            screen.blit(sprite_images['vie3'], (x, y))
            vies_restantes -= 3
        elif vies_restantes == 2:
            # Utiliser un coeur de 2 vies
            screen.blit(sprite_images['vie2'], (x, y))
            vies_restantes -= 2
        else:  # vies_restantes == 1
            # Utiliser un coeur de 1 vie
            screen.blit(sprite_images['vie1'], (x, y))
            vies_restantes -= 1

def afficher_fin_partie(partie_terminee, vies, victoire_totale):
    """
    Affiche un indicateur visuel de fin de partie sans texte.
    
    Args:
        partie_terminee (bool): Si la partie est terminée
        vies (int): Nombre de vies restantes
        victoire_totale (bool): Si tous les niveaux sont terminés
    """
    if not partie_terminee:
        return
        
    # Créer une surface semi-transparente
    overlay = pygame.Surface((XMAX, YMAX), pygame.SRCALPHA)
    
    # Choisir la couleur en fonction de la situation
    if vies <= 0:
        # Rouge pour défaite
        overlay.fill((255, 50, 50, 128))
    elif victoire_totale:
        # Or pour victoire totale
        overlay.fill((255, 215, 0, 128))
    else:
        # Vert pour niveau terminé
        overlay.fill((50, 255, 50, 128))
    
    # Afficher l'overlay
    screen.blit(overlay, (0, 0)) 