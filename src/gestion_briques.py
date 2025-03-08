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
    
    # Calculer combien de briques peuvent tenir sur une ligne
    briques_par_ligne = (XMAX - 2 * espacement_h) // (largeur + espacement_h)
    
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

def generer_briques(couleurs_niveau, liste_briques, XMAX, TYPES_BRIQUES):
    """
    Génère les briques en les disposant de manière aléatoire selon différents patterns.
    Utilise uniquement les couleurs définies pour le niveau actuel.
    
    Args:
        couleurs_niveau (list): Liste des couleurs disponibles pour ce niveau
        liste_briques (list): Liste où ajouter les briques créées
        XMAX (int): Largeur maximale de l'écran
        TYPES_BRIQUES (dict): Dictionnaire contenant les informations sur les types de briques
    """
    # Paramètres de disposition
    espacement_h = 7  # espacement horizontal
    espacement_v = 7  # espacement vertical
    marge_haut = 10  # Marge par rapport au haut de l'écran
    
    # Liste des patterns possibles
    patterns = [
        'normale',     # Ligne uniforme d'un seul type de brique
        'double',      # Deux lignes du même type de brique
        'alternance',  # Alternance de deux types de briques
        'triangle',    # Disposition en triangle
        'zigzag',      # Disposition en zigzag
        'aléatoire'    # Chaque brique est d'un type aléatoire
    ]
    
    # Types de briques disponibles
    types_disponibles = list(TYPES_BRIQUES.keys())
    
    # Nombre de lignes (aléatoire entre 3 et 5)
    nombre_lignes = random.randint(3, 5)
    
    # Traiter chaque ligne avec un pattern aléatoire
    y = marge_haut
    
    for i in range(nombre_lignes):
        # Choisir un pattern aléatoire
        pattern = random.choice(patterns)
        
        if pattern == 'normale':
            # Une ligne de briques d'un type aléatoire
            type_brique = random.choice(types_disponibles)
            creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'double':
            # Deux rangées du même type de briques
            type_brique = random.choice(types_disponibles)
            creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v/2
            creer_ligne_briques(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'alternance':
            # Alternance de deux types de briques
            types = random.sample(types_disponibles, 2)
            creer_ligne_mixte(y, types, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += max(TYPES_BRIQUES[types[0]][1], TYPES_BRIQUES[types[1]][1]) + espacement_v
            
        elif pattern == 'triangle':
            # Disposition en triangle (plus de briques au centre)
            type_brique = random.choice(types_disponibles)
            creer_ligne_triangle(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'zigzag':
            # Disposition en zigzag
            type_brique = random.choice(types_disponibles)
            creer_ligne_zigzag(y, type_brique, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += TYPES_BRIQUES[type_brique][1] + espacement_v
            
        elif pattern == 'aléatoire':
            # Chaque brique est d'un type aléatoire
            creer_ligne_aleatoire(y, types_disponibles, espacement_h, XMAX, couleurs_niveau, liste_briques, TYPES_BRIQUES)
            y += max(TYPES_BRIQUES[t][1] for t in types_disponibles) + espacement_v 