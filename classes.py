import math
import pygame
import random

from constantes import *

screen = pygame.display.set_mode((XMAX, YMAX), pygame.SCALED)

# Liste des couleurs disponibles pour les briques
COULEURS_DISPONIBLES = ['bleue', 'verte', 'jaune', 'orange', 'rouge', 'violette']

# Structure pour les types de briques:
# 'type': (largeur, hauteur, nombre_de_vies, {couleur: (x_base, y_base)})
# où x_base et y_base sont les coordonnées de la première brique (niveau de vie max)
TYPES_BRIQUES = {
    'standard': (32, 9, 3, {
        'bleue': (0, 7),
        'verte': (0, 23),
        'jaune': (0, 39),
        'orange': (0, 55),
        'rouge': (0, 71),
        'violette': (0, 87)
    }),
    'moyenne': (32, 16, 3, {
        'bleue': (112, 0),
        'verte': (112, 16),
        'jaune': (112, 32),
        'orange': (112, 48),
        'rouge': (112, 64),
        'violette': (112, 80)
    }),
    'petite': (16, 16, 2, {
        'bleue': (224, 0),
        'verte': (224, 16),
        'jaune': (224, 32),
        'orange': (224, 48),
        'rouge': (224, 64),
        'violette': (224, 80)
    })
}

# Types de bonus disponibles avec leurs positions dans le sprite sheet
TYPES_BONUS = {
    'vie_plus': ('sprites', 112, 59, 8, 8),     # Bonus de vie supplémentaire
    'balle_plus': ('sprites', 112, 27, 8, 8),   # Bonus de nouvelle balle
    'multi_balles': ('sprites', 112, 43, 8, 8), # Bonus multiplication des balles
    'raquette_large': ('sprites', 112, 91, 8, 8) # Bonus raquette élargie
}

# Dictionnaire contenant les positions et tailles des sprites dans les sprite sheets
sprites = {
    'balle': ('sprites', 144, 8, 8, 8),
    'raquette': ('sprites', 64, 7, 32, 9),
    'raquette_gauche': ('raquette', 96, 7, 4, 9),
    'raquette_milieu': ('raquette', 112, 7, 3, 9),
    'raquette_droite': ('raquette', 128, 7, 4, 9),
    'vie3': ('hearts', 115, 3, 11, 10),  # Ajout du sprite pour les vies
    'vie2': ('hearts', 82, 3, 11, 10),  # Ajout du sprite pour les vies
    'vie1': ('hearts', 34, 3, 11, 10),  # Ajout du sprite pour les vies
}

# Ajouter les bonus au dictionnaire de sprites
for nom_bonus, (sheet_name, x, y, width, height) in TYPES_BONUS.items():
    sprites[nom_bonus] = (sheet_name, x, y, width, height)

# Génération automatique des sprites pour tous les types de briques
for type_brique, (largeur, hauteur, nb_vies, positions) in TYPES_BRIQUES.items():
    for couleur, (x_base, y_base) in positions.items():
        for niveau in range(nb_vies, 0, -1):
            # Calculer la position X en fonction du niveau de vie et de la position de base
            x = x_base + (nb_vies - niveau) * largeur
            
            # Ajouter au dictionnaire
            nom_sprite = f'brique{type_brique}_{niveau}_{couleur}'
            sprites[nom_sprite] = ('bricks', x, y_base, largeur, hauteur)

# Dictionnaire pour stocker les différentes sprite sheets
sprite_sheets = {
    'sprites': pygame.image.load('assets/paddles_and_balls.png').convert_alpha(),
    'hearts': pygame.image.load('assets/hearts.png').convert_alpha(),
    'bricks': pygame.image.load('assets/bricks.png').convert_alpha(),
    'raquette': pygame.image.load('assets/paddle_part.png').convert_alpha(),
}

# Fonction pour extraire un sprite de la sprite sheet
def get_sprite(name):
    """
    Extrait un sprite spécifique d'une sprite sheet.
    
    Args:
        name (str): Nom du sprite à extraire
        
    Returns:
        Surface: L'image du sprite extraite
    """
    sheet_name, x, y, width, height = sprites[name]
    sprite_sheet = sprite_sheets[sheet_name]
    rect = pygame.Rect(x, y, width, height)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sprite_sheet, (0, 0), rect)
    return image

# Précharger les images des sprites
sprite_images = {name: get_sprite(name) for name in sprites}

class Bonus:
    """Classe représentant un bonus qui tombe d'une brique détruite."""
    
    def __init__(self, x, y):
        """
        Initialise un nouveau bonus à la position spécifiée.
        
        Args:
            x (int): Position x initiale
            y (int): Position y initiale
        """
        # Choisir un type de bonus au hasard
        self.type = random.choice(list(TYPES_BONUS.keys()))
        self.sprite = sprite_images[self.type]
        self.width, self.height = self.sprite.get_size()
        self.x = x
        self.y = y
        self.vitesse = 1  # Vitesse de chute
        self.actif = True  # Le bonus est actif tant qu'il n'est pas ramassé ou perdu
        
    def deplacer(self):
        """Fait tomber le bonus vers le bas de l'écran."""
        self.y += self.vitesse
        # Désactiver le bonus s'il sort de l'écran
        if self.y > YMAX + self.height:
            self.actif = False
            
    def collision_raquette(self, raquette):
        """
        Vérifie si le bonus entre en collision avec la raquette.
        
        Args:
            raquette (Raquette): La raquette à tester
            
        Returns:
            bool: True s'il y a collision, False sinon
        """
        horizontal = abs(self.x - raquette.x) < (self.width/2 + raquette.width/2)
        vertical = abs(self.y - raquette.y) < (self.height/2 + raquette.height/2)
        return horizontal and vertical
            
    def afficher(self):
        """Affiche le bonus à sa position actuelle."""
        if self.actif:
            screen.blit(self.sprite, (self.x - self.width/2, self.y - self.height/2))

class Balle:
    """Classe représentant la balle du jeu."""
    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        """
        Initialise une nouvelle balle.
        
        Args:
            x (int, optional): Position x initiale. Si None, position par défaut.
            y (int, optional): Position y initiale. Si None, position par défaut.
            vx (float, optional): Vitesse x initiale. Si None, la balle est sur la raquette.
            vy (float, optional): Vitesse y initiale. Si None, la balle est sur la raquette.
        """
        self.x = x if x is not None else 400
        self.y = y if y is not None else 400
        self.vx = vx
        self.vy = vy
        self.vitesse = 3
        self.sur_raquette = vx is None or vy is None  # Si pas de vitesse spécifiée, la balle est sur la raquette
        self.sprite = sprite_images['balle']
        
        # Définir la taille exacte en fonction du sprite
        self.width, self.height = self.sprite.get_size()
        self.rayon = self.width / 2  # Pour les calculs de collision circulaire
        
        # Initialiser la vitesse avec un angle par défaut si la balle n'est pas sur la raquette
        if not self.sur_raquette:
            self.vitesse = math.sqrt(vx**2 + vy**2)  # Garder la même norme de vitesse
        else:
            self.vitesse_par_angle(60)

    def vitesse_par_angle(self, angle):
        """
        Définit la vitesse de la balle en fonction d'un angle.
        
        Args:
            angle (float): Angle en degrés (0° = droite, 90° = haut)
        """
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def afficher(self):
        """Affiche la balle à sa position actuelle."""
        screen.blit(self.sprite, (self.x - self.width/2, self.y - self.height/2))

    def rebond_raquette(self, raquette):
        """
        Calcule le rebond de la balle sur la raquette.
        L'angle dépend de la position de la balle par rapport au centre de la raquette.
        
        Args:
            raquette (Raquette): La raquette avec laquelle la balle entre en collision
        """
        # Écart horizontal entre le centre de la raquette et la balle
        diff = raquette.x - self.x
        
        # Écart tangent (basé sur les sprites)
        longueur_totale = raquette.width / 2 + self.width / 2
        
        # Formule où l'angle est proportionnel à l'écart au centre de la raquette
        angle = 90 + 80 * diff / longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette):
        """
        Déplace la balle et gère les rebonds sur les murs et la raquette.
        
        Args:
            raquette (Raquette): La raquette du joueur
        Returns:
            bool: True si la balle est perdue, False sinon
        """
        perdue = False
        
        if self.sur_raquette:
            # On met la balle sur la raquette
            self.y = raquette.y - self.height/2 - raquette.height/2
            self.x = raquette.x
        else:
            # Déplacement de la balle
            self.x += self.vx
            self.y += self.vy
            
            # Gestion des collisions
            # Avec la raquette
            if raquette.collision_balle(self) and self.vy > 0:  # Collision et balle descendante
                self.rebond_raquette(raquette)
                
            # Avec les bords de l'écran
            if self.x + self.width/2 > XMAX:
                self.vx = -self.vx
                self.x = XMAX - self.width/2  # Éviter que la balle sorte de l'écran
            
            if self.x - self.width/2 < XMIN:
                self.vx = -self.vx
                self.x = XMIN + self.width/2  # Éviter que la balle sorte de l'écran
            
            if self.y + self.height/2 > YMAX:
                self.sur_raquette = True
                perdue = True  # Indique que la balle est perdue
            
            if self.y - self.height/2 < YMIN:
                self.vy = -self.vy
                self.y = YMIN + self.height/2  # Éviter que la balle sorte de l'écran
                
        return perdue


class Raquette:
    """Classe représentant la raquette contrôlée par le joueur."""
    
    def __init__(self):
        """Initialise une nouvelle raquette."""
        # Utilisation des sprites individuels
        self.sprite_gauche = sprite_images['raquette_gauche']
        self.sprite_milieu = sprite_images['raquette_milieu']
        self.sprite_droite = sprite_images['raquette_droite']
        
        # Dimensions des parties constituantes
        self.larg_gauche = self.sprite_gauche.get_width()
        self.larg_milieu = self.sprite_milieu.get_width()
        self.larg_droite = self.sprite_droite.get_width()
        self.height = self.sprite_milieu.get_height()  # La hauteur est la même pour tous
        
        # Par défaut - raquette normale avec 8 sections milieu
        self.nb_sections_milieu = 8
        self.elargie = False
        
        # Calcul de la largeur totale
        self.width = self.larg_gauche + (self.nb_sections_milieu * self.larg_milieu) + self.larg_droite
        
        # Position
        self.x = XMAX / 2
        self.y = YMAX - self.height/2
        
        # Temps d'élargissement
        self.temps_elargie = 0

    def afficher(self):
        """Affiche la raquette composée de plusieurs sprites."""
        # Position de début (partie gauche)
        x_debut = self.x - self.width/2
        y_pos = self.y - self.height/2
        
        # Afficher la partie gauche
        screen.blit(self.sprite_gauche, (x_debut, y_pos))
        x_courant = x_debut + self.larg_gauche
        
        # Afficher les sections du milieu
        for i in range(self.nb_sections_milieu):
            screen.blit(self.sprite_milieu, (x_courant, y_pos))
            x_courant += self.larg_milieu
            
        # Afficher la partie droite
        screen.blit(self.sprite_droite, (x_courant, y_pos))
    
    def elargir(self):
        """Élargit temporairement la raquette en augmentant le nombre de sections milieu."""
        if not self.elargie:
            # Agrandir la raquette en ajoutant des sections au milieu
            self.nb_sections_milieu = 14  # Augmenter le nombre de sections du milieu
            
            # Recalculer la largeur totale
            self.width = self.larg_gauche + (self.nb_sections_milieu * self.larg_milieu) + self.larg_droite
            
            self.elargie = True
            self.temps_elargie = 600  # 10 secondes à 60 FPS
    
    def mise_a_jour(self):
        """Met à jour l'état de la raquette (bonus temporaires)."""
        if self.elargie:
            self.temps_elargie -= 1
            if self.temps_elargie <= 0:
                # Revenir à la taille normale
                self.nb_sections_milieu = 8
                # Recalculer la largeur totale
                self.width = self.larg_gauche + (self.nb_sections_milieu * self.larg_milieu) + self.larg_droite
                self.elargie = False

    def deplacer(self, x):
        """
        Déplace la raquette horizontalement en limitant sa position à l'écran.
        
        Args:
            x (int): Nouvelle position x souhaitée (généralement la position de la souris)
        """
        # On limite la position x pour que la raquette ne dépasse pas de l'écran
        if x + self.width / 2 > XMAX:
            self.x = XMAX - self.width / 2
        elif x - self.width / 2 < XMIN:
            self.x = XMIN + self.width / 2
        else:
            self.x = x

    def collision_balle(self, balle):
        """
        Vérifie s'il y a collision entre la raquette et la balle.
        
        Args:
            balle (Balle): La balle à tester
            
        Returns:
            bool: True s'il y a collision, False sinon
        """
        horizontal = abs(self.x - balle.x) < balle.width/2 + self.width/2
        vertical = abs(self.y - balle.y) < balle.height/2 + self.height/2
        return horizontal and vertical


class Brique:
    """Classe représentant une brique destructible."""
    
    def __init__(self, x, y, type_brique='standard', couleur=None):
        """
        Initialise une nouvelle brique.
        
        Args:
            x (int): Position x du centre de la brique
            y (int): Position y du centre de la brique
            type_brique (str): Type de brique ('standard', 'moyenne', 'petite')
            couleur (str, optional): Couleur de la brique. Si None, une couleur aléatoire est choisie.
        """
        self.x = x  # abscisse du centre de la brique
        self.y = y  # ordonnée du centre de la brique
        self.type_brique = type_brique
        
        # Récupérer les propriétés du type de brique
        self.largeur, self.hauteur, self.vie_max, _ = TYPES_BRIQUES[type_brique]
        self.vie = self.vie_max  # Chaque brique commence avec son nombre maximal de vies
        
        # Si aucune couleur n'est spécifiée, en choisir une aléatoirement
        self.couleur = couleur #si couleur else random.choice(COULEURS_DISPONIBLES)
        
        # Dimensions de la brique
        self.width = self.largeur
        self.height = self.hauteur

        # Probabilité de générer un bonus quand la brique est détruite (en pourcentage)
        self.chance_bonus = 30  # 30% de chance

    def en_vie(self):
        """
        Vérifie si la brique est encore en vie.
        
        Returns:
            bool: True si la brique a encore de la vie, False sinon
        """
        return self.vie > 0

    def afficher(self):
        """Affiche la brique avec le sprite correspondant au niveau de vie actuel."""
        if self.en_vie():
            # Sélectionne le sprite selon le type, le niveau de vie et la couleur
            sprite_name = f'brique{self.type_brique}_{self.vie}_{self.couleur}'
            if sprite_name in sprite_images:
                sprite = sprite_images[sprite_name]
                screen.blit(sprite, (self.x - self.width/2, self.y - self.height/2))

    def collision_balle(self, balle):
        """
        Vérifie et gère la collision avec une balle.
        Si collision, fait rebondir la balle et réduit la vie de la brique.
        
        Args:
            balle (Balle): La balle à tester
            
        Returns:
            tuple: (bool, bool, int, int) - collision, bonus généré, position x du bonus, position y du bonus
        """
        # Pas de collision si la brique est déjà détruite
        if not self.en_vie():
            return False, False, 0, 0
        
        # Vérifier la collision avec la balle en utilisant les dimensions exactes des sprites
        horizontal = abs(self.x - balle.x) < (self.width / 2 + balle.width / 2)
        vertical = abs(self.y - balle.y) < (self.height / 2 + balle.height / 2)
        
        if horizontal and vertical:
            # Déterminer de quel côté vient la balle pour le rebond correct
            dx = balle.x - self.x
            dy = balle.y - self.y
            
            # Calculer les distances de pénétration
            penetration_x = self.width / 2 + balle.width / 2 - abs(dx)
            penetration_y = self.height / 2 + balle.height / 2 - abs(dy)
            
            # Rebond sur l'axe de moindre pénétration
            if penetration_x < penetration_y:
                # Rebond horizontal
                balle.vx = -balle.vx
            else:
                # Rebond vertical
                balle.vy = -balle.vy
            
            # Réduire la vie de la brique
            self.vie -= 1
            
            # Vérifier si la brique est détruite et déterminer si un bonus est généré
            bonus_genere = False
            if not self.en_vie() and random.randint(1, 100) <= self.chance_bonus:
                bonus_genere = True
            
            return True, bonus_genere, self.x, self.y
        
        return False, False, 0, 0
