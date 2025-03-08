"""
Module contenant la configuration des niveaux du jeu
"""

# Définition des niveaux avec leurs paramètres spécifiques
NIVEAUX = {
    1: {
        'arriere_plan': 'assets/background/1.png',
        'couleurs_briques': ['bleue', 'rouge', 'violette']
    },
    2: {
        'arriere_plan': 'assets/background/2.png',
        'couleurs_briques': ['jaune', 'orange', 'rouge', 'violette']
    }
}

# Nombre total de niveaux disponibles
NOMBRE_MAX_NIVEAUX = len(NIVEAUX) 