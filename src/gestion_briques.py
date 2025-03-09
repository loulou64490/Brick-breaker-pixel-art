"""
Module contenant les fonctions de génération des briques pour le jeu
"""
import random
from src.brique import Brique

def creer_brique(x, y, type_brique, couleurs_niveau, couleur=None):
    """
    Crée une brique avec une couleur spécifique ou aléatoire parmi celles du niveau.
    
    Args:
        x (int): Position x du centre de la brique
        y (int): Position y du centre de la brique
        type_brique (str): Type de brique
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        couleur (str, optional): Couleur spécifique ou None pour aléatoire
    
    Returns:
        Brique: La brique créée
    """
    # Si aucune couleur n'est spécifiée, en choisir une aléatoirement parmi celles du niveau
    couleur_finale = couleur if couleur else random.choice(couleurs_niveau)
    return Brique(x, y, type_brique, couleur_finale)

def creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une ligne de briques du même type.
    
    Args:
        y (int): Ordonnée du centre de la ligne
        type_brique (str): Type de brique à créer
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer les dimensions du type de brique
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Pour les petits écrans, on peut réduire davantage l'espacement si nécessaire
    if XMAX <= 240:
        espacement_h = max(3, espacement_h - 2)  # Réduire l'espacement mais garder au moins 3px
    
    # Calculer combien de briques peuvent tenir sur une ligne
    briques_par_ligne = (XMAX - 2 * espacement_h) // (largeur + espacement_h)
    
    # Pour les petits écrans, limiter le nombre maximal de briques par ligne
    if XMAX <= 240:
        briques_par_ligne = min(briques_par_ligne, 6)  # Maximum 6 briques par ligne
    
    # Calculer la largeur totale occupée par les briques et les espacements
    largeur_totale = briques_par_ligne * largeur + (briques_par_ligne - 1) * espacement_h
    
    # Calculer la marge gauche pour centrer les briques horizontalement
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Création des briques
    for colonne in range(int(briques_par_ligne)):
        # Calculer la position du centre de la brique
        x = marge_gauche + colonne * (largeur + espacement_h) + largeur/2
        
        # Créer et ajouter la brique
        brique = creer_brique(x, y + hauteur/2, type_brique, couleurs_niveau)
        liste_briques.append(brique)

def creer_ligne_mixte(y, types_briques, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une ligne avec alternance de types de briques.
    
    Args:
        y (int): Ordonnée du centre de la ligne
        types_briques (list): Liste des types de briques à alterner
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Calculer la largeur moyenne des briques pour estimer le nombre par ligne
    largeur_moyenne = sum(TYPES_BRIQUES[t][0] for t in types_briques) / len(types_briques)
    
    # Estimer le nombre de briques qui peuvent tenir sur la ligne
    briques_approx = int((XMAX - 2 * espacement_h) / (largeur_moyenne + espacement_h))
    
    # Prévoir la séquence exacte des types de briques
    sequence_briques = []
    for i in range(briques_approx):
        type_index = i % len(types_briques)
        sequence_briques.append(types_briques[type_index])
    
    # Calculer la largeur totale réelle
    largeur_totale = sum(TYPES_BRIQUES[t][0] for t in sequence_briques) + (len(sequence_briques) - 1) * espacement_h
    
    # Calculer la marge gauche pour centrer
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Création des briques
    x_courant = marge_gauche
    for type_brique in sequence_briques:
        largeur = TYPES_BRIQUES[type_brique][0]
        hauteur = TYPES_BRIQUES[type_brique][1]
        
        # Calculer la position du centre de la brique
        x = x_courant + largeur / 2
        
        # Créer et ajouter la brique
        brique = creer_brique(x, y + hauteur/2, type_brique, couleurs_niveau)
        liste_briques.append(brique)
        
        # Mettre à jour la position horizontale pour la prochaine brique
        x_courant += largeur + espacement_h

def creer_ligne_triangle(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une ligne de briques en forme de triangle (plus dense au centre).
    
    Args:
        y (int): Ordonnée du centre de la ligne
        type_brique (str): Type de brique à créer
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer les dimensions du type de brique
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Calculer combien de briques peuvent tenir sur une ligne
    briques_max = (XMAX - 2 * espacement_h) // (largeur + espacement_h)
    
    # Pour un triangle, on place moins de briques sur les côtés
    briques_utilisees = max(3, int(briques_max * 0.7))  # Au moins 3 briques
    
    # Assurons-nous que c'est un nombre impair pour la symétrie
    if briques_utilisees % 2 == 0:
        briques_utilisees -= 1
        
    # Calculer la largeur totale occupée par les briques et les espacements
    largeur_totale = briques_utilisees * largeur + (briques_utilisees - 1) * espacement_h
    
    # Calculer la marge gauche pour centrer les briques horizontalement
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Création des briques avec plus de probabilité au centre
    for colonne in range(briques_utilisees):
        # Plus on est proche du centre, plus la probabilité d'avoir une brique est élevée
        centre = briques_utilisees // 2
        distance_centre = abs(colonne - centre)
        probabilite = 1.0 - (distance_centre / (briques_utilisees / 2)) * 0.7
        
        if random.random() < probabilite:
            # Calculer la position du centre de la brique
            x = marge_gauche + colonne * (largeur + espacement_h) + largeur/2
            
            # Créer et ajouter la brique
            brique = creer_brique(x, y + hauteur/2, type_brique, couleurs_niveau)
            liste_briques.append(brique)

def creer_ligne_zigzag(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une ligne de briques en zigzag.
    
    Args:
        y (int): Ordonnée du centre de la ligne
        type_brique (str): Type de brique à créer
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer les dimensions du type de brique
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Calculer combien de briques peuvent tenir sur une ligne
    briques_par_ligne = (XMAX - 2 * espacement_h) // (largeur + espacement_h)
    
    # Calculer la largeur totale occupée par les briques et les espacements
    largeur_totale = briques_par_ligne * largeur + (briques_par_ligne - 1) * espacement_h
    
    # Calculer la marge gauche pour centrer les briques horizontalement
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Décalage vertical pour le zigzag
    decalage_zigzag = hauteur / 2
    
    # Création des briques en zigzag
    for colonne in range(int(briques_par_ligne)):
        # Calculer la position du centre de la brique
        x = marge_gauche + colonne * (largeur + espacement_h) + largeur/2
        
        # Alterner la position verticale (zigzag)
        y_decale = y + (decalage_zigzag if colonne % 2 == 0 else -decalage_zigzag)
        
        # Créer et ajouter la brique
        brique = creer_brique(x, y_decale + hauteur/2, type_brique, couleurs_niveau)
        liste_briques.append(brique)

def creer_ligne_aleatoire(y, types_briques, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une ligne de briques avec des types aléatoires.
    
    Args:
        y (int): Ordonnée du centre de la ligne
        types_briques (list): Liste des types de briques disponibles
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Calculer la largeur moyenne des briques pour estimer le nombre par ligne
    largeur_moyenne = sum(TYPES_BRIQUES[t][0] for t in types_briques) / len(types_briques)
    hauteur_max = max(TYPES_BRIQUES[t][1] for t in types_briques)
    
    # Estimer le nombre de briques qui peuvent tenir sur la ligne
    briques_approx = int((XMAX - 2 * espacement_h) / (largeur_moyenne + espacement_h))
    
    # Générer une séquence aléatoire de types de briques
    sequence_briques = [random.choice(types_briques) for _ in range(briques_approx)]
    
    # Calculer la largeur totale réelle
    largeur_totale = sum(TYPES_BRIQUES[t][0] for t in sequence_briques) + (len(sequence_briques) - 1) * espacement_h
    
    # Calculer la marge gauche pour centrer
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Création des briques
    x_courant = marge_gauche
    for type_brique in sequence_briques:
        largeur = TYPES_BRIQUES[type_brique][0]
        hauteur = TYPES_BRIQUES[type_brique][1]
        
        # Calculer la position du centre de la brique
        x = x_courant + largeur / 2
        
        # Créer et ajouter la brique avec une probabilité aléatoire
        if random.random() < 0.8:  # 80% de chance d'avoir une brique
            brique = creer_brique(x, y + hauteur/2, type_brique, couleurs_niveau)
            liste_briques.append(brique)
        
        # Mettre à jour la position horizontale pour la prochaine brique
        x_courant += largeur + espacement_h

def creer_formation_arcade(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une formation ressemblant aux ennemis des jeux d'arcade rétro.
    
    Args:
        y (int): Ordonnée du centre de la formation
        type_brique (str): Type de brique à créer
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer les dimensions du type de brique
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Définir la formation: adaptée pour un écran plus petit
    if XMAX <= 240:
        formation = [
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1],
        ]
    else:
        # Formation originale pour les grands écrans
        formation = [
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
    
    # Calculer la largeur totale de la formation
    cols = len(formation[0])
    largeur_totale = cols * largeur + (cols - 1) * espacement_h
    
    # Centrer la formation
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Créer les briques selon la formation
    for ligne, row in enumerate(formation):
        for col, cell in enumerate(row):
            if cell == 1:
                x = marge_gauche + col * (largeur + espacement_h) + largeur/2
                y_pos = y + ligne * (hauteur + espacement_h) + hauteur/2
                
                # Choisir une couleur selon la ligne pour un effet visuel
                couleur = couleurs_niveau[ligne % len(couleurs_niveau)]
                
                brique = creer_brique(x, y_pos, type_brique, couleurs_niveau, couleur)
                liste_briques.append(brique)

def creer_formation_coeur(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une formation en forme de cœur.
    
    Args:
        y (int): Ordonnée du centre de la formation
        type_brique (str): Type de brique à créer
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer les dimensions du type de brique
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Définir la formation en forme de cœur, adaptée pour petits écrans
    if XMAX <= 240:
        formation = [
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
        ]
    else:
        # Formation originale pour grands écrans
        formation = [
            [0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ]
    
    # Calculer la largeur totale de la formation
    cols = len(formation[0])
    largeur_totale = cols * largeur + (cols - 1) * espacement_h
    
    # Centrer la formation
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Créer les briques selon la formation
    for ligne, row in enumerate(formation):
        for col, cell in enumerate(row):
            if cell == 1:
                x = marge_gauche + col * (largeur + espacement_h) + largeur/2
                y_pos = y + ligne * (hauteur + espacement_h) + hauteur/2
                
                # Utiliser une couleur rouge ou rose pour le cœur si disponible
                coeurs_couleurs = [c for c in couleurs_niveau if "rouge" in c or "rose" in c]
                if coeurs_couleurs:
                    couleur = random.choice(coeurs_couleurs)
                else:
                    couleur = random.choice(couleurs_niveau)
                
                brique = creer_brique(x, y_pos, type_brique, couleurs_niveau, couleur)
                liste_briques.append(brique)

def creer_labyrinthe(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une formation en forme de labyrinthe simple avec des chemins pour la balle.
    
    Args:
        y (int): Ordonnée du centre de la formation
        type_brique (str): Type de brique à créer
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer les dimensions du type de brique
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Créer un labyrinthe simple adapté à la taille de l'écran
    if XMAX <= 240:
        formations = [
            # Labyrinthe simplifié pour petit écran
            [
                [1, 1, 0, 1, 1],
                [1, 0, 0, 0, 1],
                [0, 0, 1, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 1],
            ],
            # Autre variante
            [
                [1, 0, 1, 0, 1],
                [0, 0, 1, 0, 0],
                [1, 1, 0, 1, 1],
                [0, 0, 0, 0, 0],
                [1, 0, 1, 0, 1],
            ]
        ]
    else:
        # Labyrinthes originaux pour grands écrans
        formations = [
            [
                [1, 1, 1, 1, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 1, 1],
            ]
        ]
    
    # Choisir un labyrinthe aléatoirement
    formation = random.choice(formations)
    
    # Calculer la largeur totale du labyrinthe
    cols = len(formation[0])
    largeur_totale = cols * largeur + (cols - 1) * espacement_h
    
    # Centrer le labyrinthe
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Créer les briques selon la formation du labyrinthe
    for ligne, row in enumerate(formation):
        for col, cell in enumerate(row):
            if cell == 1:
                x = marge_gauche + col * (largeur + espacement_h) + largeur/2
                y_pos = y + ligne * (hauteur + espacement_h) + hauteur/2
                
                # Varier les types de briques pour rendre le labyrinthe plus difficile
                # Pour les petits écrans, réduire la probabilité de briques résistantes
                chances_resistantes = 0.15 if XMAX <= 240 else 0.2
                
                if random.random() < chances_resistantes:
                    types_resistants = [t for t in TYPES_BRIQUES.keys() if "double" in t or "metal" in t]
                    if types_resistants:
                        type_special = random.choice(types_resistants)
                        brique = creer_brique(x, y_pos, type_special, couleurs_niveau)
                    else:
                        brique = creer_brique(x, y_pos, type_brique, couleurs_niveau)
                else:
                    brique = creer_brique(x, y_pos, type_brique, couleurs_niveau)
                
                liste_briques.append(brique)

def creer_formation_boss(y, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES):
    """
    Crée une formation spéciale 'boss' avec des briques très résistantes.
    À utiliser pour les derniers niveaux.
    
    Args:
        y (int): Ordonnée du centre de la formation
        espacement_h (int): Espacement horizontal entre les briques
        XMAX (int): Largeur maximale de l'écran
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Récupérer le type de brique le plus résistant
    types_resistants = [t for t in TYPES_BRIQUES.keys() if "metal" in t or "double" in t]
    if not types_resistants:
        types_resistants = list(TYPES_BRIQUES.keys())
    
    type_brique = random.choice(types_resistants)
    largeur = TYPES_BRIQUES[type_brique][0]
    hauteur = TYPES_BRIQUES[type_brique][1]
    
    # Former un "visage" avec des briques résistantes, adapté pour petits écrans
    if XMAX <= 240:
        formation = [
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 1, 1, 0],
        ]
    else:
        # Formation originale pour grands écrans
        formation = [
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 0],
        ]
    
    # Calculer la largeur totale de la formation
    cols = len(formation[0])
    largeur_totale = cols * largeur + (cols - 1) * espacement_h
    
    # Centrer la formation
    marge_gauche = (XMAX - largeur_totale) / 2
    
    # Créer les briques selon la formation
    for ligne, row in enumerate(formation):
        for col, cell in enumerate(row):
            if cell == 1:
                x = marge_gauche + col * (largeur + espacement_h) + largeur/2
                y_pos = y + ligne * (hauteur + espacement_h) + hauteur/2
                
                # Utiliser le type de brique résistant pour toutes les briques
                brique = creer_brique(x, y_pos, type_brique, couleurs_niveau)
                liste_briques.append(brique)

def generer_briques(couleurs_niveau, liste_briques, XMAX, TYPES_BRIQUES, niveau=1):
    """
    Génère les briques en les disposant selon différents patterns.
    Utilise uniquement les couleurs définies pour le niveau actuel.
    La difficulté augmente avec le niveau.
    
    Args:
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        XMAX (int): Largeur maximale de l'écran
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
        niveau (int, optional): Numéro du niveau actuel pour ajuster la difficulté
    """
    # Paramètres de disposition adaptés pour un écran 240x160
    espacement_h = 5  # espacement horizontal réduit
    espacement_v = 5  # espacement vertical réduit
    marge_haut = 10  # Marge par rapport au haut de l'écran
    
    # Hauteur limite pour éviter la superposition avec la raquette (réserve ~40px en bas)
    hauteur_limite = 120  # YMAX (160) - 40 pour la zone de la raquette
    
    # Liste des patterns de base
    patterns_base = [
        'normale',     # Ligne uniforme d'un seul type de brique
        'double',      # Deux lignes du même type de brique
        'alternance',  # Alternance de deux types de briques
        'triangle',    # Disposition en triangle
        'zigzag',      # Disposition en zigzag
        'aléatoire'    # Chaque brique est d'un type aléatoire
    ]
    
    # Patterns avancés (ajoutés progressivement selon le niveau)
    patterns_avances = []
    if niveau >= 3:
        patterns_avances.append('arcade')  # Formation de style jeu d'arcade
    if niveau >= 5:
        patterns_avances.append('coeur')   # Formation en forme de cœur
    if niveau >= 7:
        patterns_avances.append('labyrinthe')  # Formation en labyrinthe
    if niveau >= 9:
        patterns_avances.append('boss')    # Formation de boss
    
    # Fusionner les patterns disponibles
    patterns = patterns_base + patterns_avances
    
    # Types de briques disponibles, avec plus de briques résistantes aux niveaux supérieurs
    types_disponibles = list(TYPES_BRIQUES.keys())
    types_resistants = [t for t in types_disponibles if "double" in t or "metal" in t]
    
    # Augmenter la probabilité de briques résistantes avec le niveau
    chance_resistante = min(0.1 + (niveau * 0.05), 0.5)  # Max 50% de chance
    
    # Nombre de lignes/formations (adapté pour un écran plus petit)
    nombre_formations = min(2 + (niveau // 3), 4)  # Max 4 formations pour un petit écran
    
    # Niveau spécial "boss" (dernier niveau)
    if niveau >= 10:  # Si c'est le dernier niveau
        # Créer une formation de boss spéciale, mais adaptée à la taille de l'écran
        creer_formation_boss(30, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
        return
    
    # Traiter chaque ligne/formation avec un pattern choisi
    y = marge_haut
    
    for i in range(nombre_formations):
        # Si on dépasse la hauteur limite, on arrête de générer des briques
        if y >= hauteur_limite:
            break
            
        # Choisir un pattern en favorisant les patterns avancés aux niveaux supérieurs
        if patterns_avances and random.random() < 0.3 + (niveau * 0.05):
            pattern = random.choice(patterns_avances)
        else:
            pattern = random.choice(patterns_base)  # Utiliser patterns_base pour plus de contrôle
        
        # Vérifier si le pattern avancé ne dépasserait pas l'écran
        hauteur_estimee = 0
        if pattern == 'arcade':
            hauteur_estimee = 5 * (TYPES_BRIQUES[list(TYPES_BRIQUES.keys())[0]][1] + espacement_h)
        elif pattern == 'coeur':
            hauteur_estimee = 6 * (TYPES_BRIQUES[list(TYPES_BRIQUES.keys())[0]][1] + espacement_h)
        elif pattern == 'labyrinthe':
            hauteur_estimee = 8 * (TYPES_BRIQUES[list(TYPES_BRIQUES.keys())[0]][1] + espacement_h)
        elif pattern == 'boss':
            hauteur_estimee = 6 * (TYPES_BRIQUES[list(TYPES_BRIQUES.keys())[0]][1] + espacement_h)
            
        # Si le pattern avancé dépasserait la limite, choisir un pattern de base
        if hauteur_estimee > 0 and y + hauteur_estimee > hauteur_limite:
            pattern = random.choice(['normale', 'triangle', 'zigzag'])  # Patterns moins hauts
        
        # Choisir un type de brique, avec une chance d'être résistante
        if types_resistants and random.random() < chance_resistante:
            type_brique = random.choice(types_resistants)
        else:
            type_brique = random.choice(types_disponibles)
        
        if pattern == 'normale':
            # Une ligne de briques d'un type donné
            creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'double':
            # Vérifier si deux lignes tiendraient dans l'espace restant
            hauteur_double = 2 * TYPES_BRIQUES[type_brique][1] + espacement_v/2
            if y + hauteur_double <= hauteur_limite:
                creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v/2
                creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v
            else:
                # Si pas assez d'espace, créer une seule ligne
                creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'alternance':
            # Alternance de deux types de briques
            types = random.sample(types_disponibles, min(2, len(types_disponibles)))
            creer_ligne_mixte(y, types, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += max(TYPES_BRIQUES[types[0]][1], TYPES_BRIQUES[types[1] if len(types) > 1 else types[0]][1]) + espacement_v
            
        elif pattern == 'triangle':
            # Disposition en triangle (plus de briques au centre)
            creer_ligne_triangle(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'zigzag':
            # Disposition en zigzag
            creer_ligne_zigzag(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'aléatoire':
            # Chaque brique est d'un type aléatoire
            creer_ligne_aleatoire(y, types_disponibles, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += max(TYPES_BRIQUES[t][1] for t in types_disponibles) + espacement_v
            
        elif pattern == 'arcade' and y + hauteur_estimee <= hauteur_limite:
            # Formation style arcade (version réduite)
            creer_formation_arcade(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += hauteur_estimee + espacement_v
            
        elif pattern == 'coeur' and y + hauteur_estimee <= hauteur_limite:
            # Formation en cœur (version réduite)
            creer_formation_coeur(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += hauteur_estimee + espacement_v
            
        elif pattern == 'labyrinthe' and y + hauteur_estimee <= hauteur_limite:
            # Formation en labyrinthe (version réduite)
            creer_labyrinthe(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += hauteur_estimee + espacement_v
            
        elif pattern == 'boss' and y + hauteur_estimee <= hauteur_limite:
            # Formation de boss intermédiaire
            creer_formation_boss(y, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += hauteur_estimee + espacement_v 