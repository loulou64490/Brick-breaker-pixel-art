"""
Module contenant la configuration des niveaux du jeu
"""

# Définition des niveaux avec leurs paramètres spécifiques
NIVEAUX = {
    1: {
        'arriere_plan': 'assets/background/1.png',
        'couleurs_briques': ['bleue', 'rouge', 'violette'],
        'description': 'Niveau débutant'
    },
    2: {
        'arriere_plan': 'assets/background/2.png',
        'couleurs_briques': ['jaune', 'orange', 'rouge', 'violette'],
        'description': 'Apprentissage'
    },
    3: {
        'arriere_plan': 'assets/background/3.png',
        'couleurs_briques': ['verte'],
        'description': 'Initiation aux formations'
    },
    4: {
        'arriere_plan': 'assets/background/4.png',
        'couleurs_briques': ['bleue'],
        'description': 'Diversité colorée'
    },
    5: {
        'arriere_plan': 'assets/background/5.png',
        'couleurs_briques': ['orange'],
        'description': 'Niveau Cœur'
    },
    6: {
        'arriere_plan': 'assets/background/6.png',
        'couleurs_briques': ['violette', 'bleue', 'orange', 'jaune'],
        'description': 'Défi aquatique'
    },
    7: {
        'arriere_plan': 'assets/background/7.png',
        'couleurs_briques': ['violette'],
        'description': 'Labyrinthe'
    },
    8: {
        'arriere_plan': 'assets/background/8.png',
        'couleurs_briques': ['jaune', 'bleue', 'orange'],
        'description': 'Challenge avancé'
    },
    9: {
        'arriere_plan': 'assets/background/9.png',
        'couleurs_briques': ['bleue', 'jaune'],
        'description': 'Pré-boss'
    },
    10: {
        'arriere_plan': 'assets/background/10.png',
        'couleurs_briques': ['rouge', 'orange', 'jaune', 'violette'],
        'description': 'Boss final'
    }
}

# Nombre total de niveaux disponibles
NOMBRE_MAX_NIVEAUX = len(NIVEAUX) 