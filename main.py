"""
Fichier principal du jeu Brick Breaker
"""
import sys
import pygame

from src.constantes import screen
from src.jeu import Jeu

# Initialisation de Pygame
pygame.init()
# Initialisation du module audio
pygame.mixer.init()
pygame.display.set_caption("Brick Breaker pixel art")

# Chargement et démarrage de la musique
pygame.mixer.music.load('assets/sound/music.mp3')
pygame.mixer.music.set_volume(0.5)  # Volume à 50%
pygame.mixer.music.play(-1)  # -1 pour jouer en boucle infinie

# Initialisation de l'horloge pour limiter les FPS
clock = pygame.time.Clock()
FPS = 60  # Images par seconde

def main():
    """Fonction principale du jeu"""
    # Initialisation du jeu
    jeu = Jeu()
    
    # Boucle principale
    while True:
        # Gestion des événements
        quitter = jeu.gestion_evenements()
        if quitter:
            pygame.quit()
            sys.exit()
        
        # Mise à jour de l'état du jeu
        jeu.mise_a_jour()
        
        # Affichage
        jeu.affichage()
        
        # Rafraîchissement de l'écran
        pygame.display.flip()
        
        # Limitation de la fréquence d'images
        clock.tick(FPS)

if __name__ == "__main__":
    main()
