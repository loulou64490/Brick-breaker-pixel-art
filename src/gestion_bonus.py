"""
Module redirigeant vers bonus.py pour maintenir la compatibilité
"""
from src.bonus import Bonus

def appliquer_bonus(bonus, vies, balles, raquette):
    """
    Redirige vers la méthode appliquer() de la classe Bonus.
    
    Cette fonction est maintenue pour la compatibilité avec le code existant.
    Elle sera supprimée dans une future version.
    
    Args:
        bonus (Bonus): Le bonus à appliquer
        vies (int): Nombre de vies actuelles du joueur
        balles (list): Liste des balles actuellement en jeu
        raquette (Raquette): Raquette du joueur
    
    Returns:
        tuple: (vies, balles) - Nombre de vies mis à jour et liste des balles mise à jour
    """
    return bonus.appliquer(vies, balles, raquette)