"""
Module contenant les fonctions liées à la gestion des bonus
"""
from src.balle import Balle

def appliquer_bonus(bonus, vies, balles, raquette):
    """
    Applique l'effet d'un bonus ramassé par le joueur.
    
    Args:
        bonus (Bonus): Le bonus à appliquer
        vies (int): Nombre de vies actuelles du joueur
        balles (list): Liste des balles actuellement en jeu
        raquette (Raquette): Raquette du joueur
    
    Returns:
        tuple: (vies, balles) - Nombre de vies mis à jour et liste des balles mise à jour
    """
    import random  # Importé ici pour éviter les imports circulaires
    
    if bonus.type == 'vie_plus':
        # Ajouter une vie
        vies += 1
        
    elif bonus.type == 'balle_plus':
        # Ajouter une nouvelle balle à côté de la raquette
        nouvelle_balle = Balle(raquette.x, raquette.y - raquette.height, 
                              random.uniform(-1, 1) * 2, -2)
        nouvelle_balle.sur_raquette = False
        balles.append(nouvelle_balle)
        
    elif bonus.type == 'multi_balles':
        # Dupliquer toutes les balles existantes
        nouvelles_balles = []
        for balle in balles:
            if not balle.sur_raquette:
                # Créer une balle similaire mais avec un angle légèrement différent
                vx = balle.vx * 0.9 + random.uniform(-0.5, 0.5)
                vy = balle.vy * 0.9 + random.uniform(-0.5, 0.5)
                nouvelle_balle = Balle(balle.x, balle.y, vx, vy)
                nouvelle_balle.sur_raquette = False
                nouvelles_balles.append(nouvelle_balle)
        
        # Ajouter les nouvelles balles à la liste
        balles.extend(nouvelles_balles)
        
    elif bonus.type == 'raquette_large':
        # Élargir temporairement la raquette
        raquette.elargir()
    
    return vies, balles 