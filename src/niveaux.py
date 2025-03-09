"""
Module contenant la configuration des niveaux du jeu
"""

# Définition des niveaux avec leurs paramètres spécifiques
NIVEAUX = {
    1: {
        'arriere_plan': 'assets/background/1.png',
        'couleurs_briques': ['bleue', 'rouge', 'violette'],
    },
    2: {
        'arriere_plan': 'assets/background/2.png',
        'couleurs_briques': ['jaune', 'orange', 'rouge', 'violette'],
    },
    3: {
        'arriere_plan': 'assets/background/3.png',
        'couleurs_briques': ['verte'],
    },
    4: {
        'arriere_plan': 'assets/background/4.png',
        'couleurs_briques': ['bleue'],
    },
    5: {
        'arriere_plan': 'assets/background/5.png',
        'couleurs_briques': ['orange'],
    },
    6: {
        'arriere_plan': 'assets/background/6.png',
        'couleurs_briques': ['violette', 'bleue', 'orange', 'jaune'],
    },
    7: {
        'arriere_plan': 'assets/background/7.png',
        'couleurs_briques': ['violette'],
    },
    8: {
        'arriere_plan': 'assets/background/8.png',
        'couleurs_briques': ['jaune', 'bleue', 'orange'],
    },
    9: {
        'arriere_plan': 'assets/background/9.png',
        'couleurs_briques': ['bleue', 'jaune'],
    },
    10: {
        'arriere_plan': 'assets/background/10.png',
        'couleurs_briques': ['rouge', 'orange', 'jaune', 'violette'],
    }
}

# Nombre total de niveaux disponibles
NOMBRE_MAX_NIVEAUX = len(NIVEAUX) 