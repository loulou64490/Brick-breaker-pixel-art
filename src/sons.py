"""
Module pour la gestion des sons et de la musique du jeu
"""
import pygame

# Initialisation du module son si nécessaire
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Chemins des fichiers musique
MUSIQUES = {
    'demarrage': 'assets/sound/take_five.mp3',
    'jeu': 'assets/sound/cantaloop_island.mp3',
    'game_over': 'assets/sound/nocturne.mp3',
    'victoire': 'assets/sound/i_wish.mp3'
}

# Chargement des effets sonores
son_bonus = pygame.mixer.Sound('assets/sound/bonus2.wav')
son_rebond = pygame.mixer.Sound('assets/sound/bounce.wav')
son_explosion = pygame.mixer.Sound('assets/sound/explosion.wav')

# Réglage du volume des effets sonores (valeurs entre 0.0 et 1.0)
son_bonus.set_volume(0.7)
son_rebond.set_volume(0.5)
son_explosion.set_volume(0.6)

def jouer_musique(nom_musique):
    """Joue une musique spécifique
    
    Args:
        nom_musique (str): Identifiant de la musique à jouer ('demarrage', 'jeu', 'game_over', 'victoire')
    """
    # Arrêter toute musique en cours
    pygame.mixer.music.stop()
    
    # Vérifier que le nom de musique est valide
    if nom_musique not in MUSIQUES:
        print(f"Musique '{nom_musique}' inconnue")
        return
        
    # Charger et jouer la musique
    try:
        pygame.mixer.music.load(MUSIQUES[nom_musique])
        pygame.mixer.music.set_volume(0.5)  # Volume à 50%
        pygame.mixer.music.play(-1)  # -1 pour jouer en boucle infinie
    except pygame.error:
        print(f"Impossible de charger la musique '{nom_musique}'")

# Fonctions spécifiques pour faciliter l'appel
def jouer_musique_demarrage():
    """Joue la musique de l'écran de démarrage"""
    jouer_musique('demarrage')

def jouer_musique_jeu():
    """Joue la musique principale du jeu"""
    jouer_musique('jeu')

def jouer_musique_game_over():
    """Joue la musique de l'écran de game over"""
    jouer_musique('game_over')

def jouer_musique_victoire():
    """Joue la musique de l'écran de victoire"""
    jouer_musique('victoire')

def jouer_son_bonus():
    """Joue le son lorsqu'un bonus est récupéré"""
    son_bonus.play()

def jouer_son_rebond():
    """Joue le son lorsque la balle rebondit"""
    #son_rebond.play() # Commenté pour éviter le bruit constant

def jouer_son_explosion():
    """Joue le son lorsqu'une brique se casse"""
    son_explosion.play() 