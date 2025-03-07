import sys
import random

from classes import *

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("Brick Breaker pixel art")

# Chargement et positionnement de l'image de fond
background_image = pygame.image.load('assets/background.png')
bg_width = background_image.get_width()
bg_height = background_image.get_height()
# Calculer la position pour centrer l'image
bg_x = (XMAX - bg_width) // 2
bg_y = (YMAX - bg_height) // 2

# Initialisation de l'horloge pour limiter les FPS
clock = pygame.time.Clock()
FPS = 60  # Images par seconde


class Jeu:
    """Classe principale qui gère le déroulement du jeu."""
    
    def __init__(self):
        """Initialise une nouvelle partie."""
        self.balle = Balle()
        self.raquette = Raquette()
        self.liste_briques = []
        
        # Génération des briques
        self.generer_briques()

    def generer_briques(self):
        """
        Génère les briques en les disposant de manière organisée et centrée sur l'écran.
        """
        # Paramètres de disposition
        espacement_h = 5  # espacement horizontal
        espacement_v = 5  # espacement vertical
        nombre_lignes = 5  # Nombre de lignes de briques
        marge_haut = 10  # Marge par rapport au haut de l'écran
        
        # On va créer une disposition mixte avec les différents types de briques
        
        # 1. Déterminer la largeur disponible pour placer les briques
        largeur_disponible = XMAX - 2 * espacement_h
        
        # 2. Pour chaque ligne, décider du type de briques et de la disposition
        y = marge_haut
        
        # Types de briques à utiliser pour chaque ligne (différentes configurations)
        configurations_lignes = [
            # Ligne 1: Alternance de briques standard
            {'type': 'standard', 'disposition': 'normale'},
            # Ligne 2: Briques moyennes uniquement
            {'type': 'moyenne', 'disposition': 'normale'},
            # Ligne 3: Mélange de briques petites
            {'type': 'petite', 'disposition': 'double'},
            # Ligne 4: Alternance de briques standard et moyennes
            {'type': 'mixte', 'disposition': 'mixte'},
            # Ligne 5: Briques petites et standard en alternance
            {'type': 'mixte2', 'disposition': 'mixte2'}
        ]
        
        # Traiter chaque ligne selon sa configuration
        for config in configurations_lignes:
            if config['type'] == 'standard':
                # Une ligne de briques standard
                self.creer_ligne_briques(y, 'standard', espacement_h)
                y += TYPES_BRIQUES['standard'][1] + espacement_v
                
            elif config['type'] == 'moyenne':
                # Une ligne de briques moyennes
                self.creer_ligne_briques(y, 'moyenne', espacement_h)
                y += TYPES_BRIQUES['moyenne'][1] + espacement_v
                
            elif config['type'] == 'petite':
                # Deux rangées de petites briques (car elles sont plus petites)
                if config['disposition'] == 'double':
                    self.creer_ligne_briques(y, 'petite', espacement_h)
                    y += TYPES_BRIQUES['petite'][1] + espacement_v/2
                    self.creer_ligne_briques(y, 'petite', espacement_h)
                    y += TYPES_BRIQUES['petite'][1] + espacement_v
                else:
                    self.creer_ligne_briques(y, 'petite', espacement_h)
                    y += TYPES_BRIQUES['petite'][1] + espacement_v
                    
            elif config['type'] == 'mixte':
                # Alternance de briques standard et moyennes
                self.creer_ligne_mixte(y, ['standard', 'moyenne'], espacement_h)
                y += max(TYPES_BRIQUES['standard'][1], TYPES_BRIQUES['moyenne'][1]) + espacement_v
                
            elif config['type'] == 'mixte2':
                # Alternance de briques petites et standard
                self.creer_ligne_mixte(y, ['petite', 'standard'], espacement_h)
                y += max(TYPES_BRIQUES['petite'][1], TYPES_BRIQUES['standard'][1]) + espacement_v

    def creer_ligne_briques(self, y, type_brique, espacement_h):
        """
        Crée une ligne de briques du même type.
        
        Args:
            y (int): Ordonnée du centre de la ligne
            type_brique (str): Type de brique à créer
            espacement_h (int): Espacement horizontal entre les briques
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
            brique = Brique(x, y + hauteur/2, type_brique)
            self.liste_briques.append(brique)

    def creer_ligne_mixte(self, y, types_briques, espacement_h):
        """
        Crée une ligne avec alternance de types de briques.
        
        Args:
            y (int): Ordonnée du centre de la ligne
            types_briques (list): Liste des types de briques à alterner
            espacement_h (int): Espacement horizontal entre les briques
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
            brique = Brique(x, y + hauteur/2, type_brique)
            self.liste_briques.append(brique)
            
            # Mettre à jour la position horizontale pour la prochaine brique
            x_courant += largeur + espacement_h

    def gestion_evenements(self):
        """Gère les événements utilisateur comme les clics et la fermeture du jeu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if self.balle.sur_raquette:
                        # Lancer la balle
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        """Met à jour l'état du jeu: position des objets, collisions, etc."""
        # Récupérer la position horizontale de la souris
        x_souris = pygame.mouse.get_pos()[0]
        
        # Déplacer la balle
        self.balle.deplacer(self.raquette)
        
        # Vérifier les collisions avec les briques
        for brique in self.liste_briques:
            if brique.en_vie():
                brique.collision_balle(self.balle)
        
        # Déplacer la raquette
        self.raquette.deplacer(x_souris)

    def affichage(self):
        """Affiche tous les éléments du jeu à l'écran."""
        # Fond noir pour les bords potentiels
        screen.fill((0, 0, 0))
        
        # Affichage de l'image de fond centrée
        screen.blit(background_image, (bg_x, bg_y))
        
        # Affichage des éléments du jeu
        self.balle.afficher()
        self.raquette.afficher()
        
        # Affichage des briques encore en vie
        for brique in self.liste_briques:
            if brique.en_vie():
                brique.afficher()


# Initialisation et boucle principale du jeu
jeu = Jeu()
while True:
    # Gestion des événements
    jeu.gestion_evenements()
    
    # Mise à jour de l'état du jeu
    jeu.mise_a_jour()
    
    # Affichage
    jeu.affichage()
    
    # Rafraîchissement de l'écran
    pygame.display.flip()
    
    # Limitation de la fréquence d'images
    clock.tick(FPS)
