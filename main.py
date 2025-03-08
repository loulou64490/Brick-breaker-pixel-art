"""
Fichier principal du jeu Brick Breaker
"""
import sys
import pygame

from src.constantes import screen
from src.jeu import Jeu
from src.ecran_demarrage import afficher_ecran_demarrage
from src.ecran_fin_partie import afficher_ecran_game_over, afficher_ecran_victoire
from src.sons import jouer_musique_jeu

# Initialisation de Pygame
pygame.init()
# Initialisation du module audio
pygame.mixer.init()
pygame.display.set_caption("Brick Breaker pixel art")

# Initialisation de l'horloge pour limiter les FPS
clock = pygame.time.Clock()
FPS = 60  # Images par seconde

def main():
    """Fonction principale du jeu"""
    
    while True:
        # Afficher l'écran de démarrage
        commencer_jeu = afficher_ecran_demarrage()
        
        # Si l'utilisateur a fermé la fenêtre pendant l'écran de démarrage
        if not commencer_jeu:
            pygame.quit()
            sys.exit()
        
        # Jouer la musique du jeu lorsqu'on commence une partie
        jouer_musique_jeu()
        
        # Initialisation du jeu
        jeu = Jeu()
        partie_en_cours = True
        
        # Boucle de jeu
        while partie_en_cours:
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
            
            # Vérifier si la partie est terminée
            if jeu.partie_terminee:
                # Afficher les écrans de fin appropriés
                if jeu.vies <= 0:
                    # Game over
                    retour_menu = afficher_ecran_game_over(jeu.background_image)
                    partie_en_cours = False
                elif jeu.victoire_totale:
                    # Victoire totale
                    retour_menu = afficher_ecran_victoire(jeu.background_image)
                    partie_en_cours = False
                
                # Si l'utilisateur a fermé la fenêtre pendant l'écran de fin
                if not retour_menu:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
