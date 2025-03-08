"""
Module contenant les fonctions liées à la gestion des niveaux du jeu
"""
import pygame
from src.constantes import XMAX, YMAX
from src.balle import Balle
from src.raquette import Raquette
from src.niveaux import NIVEAUX, NOMBRE_MAX_NIVEAUX
from src.gestion_briques import generer_briques

def charger_niveau(niveau, TYPES_BRIQUES):
    """
    Charge les paramètres spécifiques du niveau.
    
    Args:
        niveau (int): Le numéro du niveau à charger
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    
    Returns:
        tuple: (victoire_totale, partie_terminee, background_image, bg_x, bg_y, couleurs_niveau)
              ou (True, True, None, None, None, None) si victoire totale
    """
    # Vérifier que le niveau existe
    if niveau > NOMBRE_MAX_NIVEAUX:
        return True, True, None, None, None, None
        
    # Récupérer les paramètres du niveau
    params_niveau = NIVEAUX[niveau]
    
    # Charger l'arrière-plan
    background_image = pygame.image.load(params_niveau['arriere_plan'])
    bg_width = background_image.get_width()
    bg_height = background_image.get_height()
    
    # Calculer la position pour centrer l'image
    bg_x = (XMAX - bg_width) // 2
    bg_y = (YMAX - bg_height) // 2
    
    # Sauvegarder les couleurs disponibles pour ce niveau
    couleurs_niveau = params_niveau['couleurs_briques']
    
    return False, False, background_image, bg_x, bg_y, couleurs_niveau

def initialiser_niveau(niveau, TYPES_BRIQUES):
    """
    Initialise un nouveau niveau en créant les briques et en réinitialisant les éléments du jeu.
    
    Args:
        niveau (int): Le numéro du niveau à initialiser
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    
    Returns:
        tuple: (victoire_totale, partie_terminee, background_image, bg_x, bg_y, 
                couleurs_niveau, liste_briques, liste_bonus, balles, raquette)
    """
    # Charger les paramètres du niveau
    victoire_totale, partie_terminee, background_image, bg_x, bg_y, couleurs_niveau = charger_niveau(niveau, TYPES_BRIQUES)
    
    # Si victoire totale, retourner les valeurs correspondantes
    if victoire_totale:
        return victoire_totale, partie_terminee, background_image, bg_x, bg_y, couleurs_niveau, [], [], [], None
    
    # Nettoyer les listes et générer les nouvelles briques
    liste_briques = []
    liste_bonus = []
    
    # Générer les briques pour ce niveau
    generer_briques(couleurs_niveau, liste_briques, XMAX, TYPES_BRIQUES)
    
    # Réinitialiser la balle sur la raquette
    balles = [Balle()]
    raquette = Raquette()
    
    return victoire_totale, partie_terminee, background_image, bg_x, bg_y, couleurs_niveau, liste_briques, liste_bonus, balles, raquette 