import sys

from classes import *

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("Brick Breaker pixel art")

# Chargement et positionnement de l'image de fond
background_image = pygame.image.load('assets/wallpaper.png')
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
        # Récupérer les dimensions d'une brique (basée sur le premier sprite)
        brique_test = Brique(0, 0)
        brique_width = brique_test.width
        brique_height = brique_test.height
        
        # Paramètres de disposition
        espacement_h = 5  # espacement horizontal
        espacement_v = 5  # espacement vertical
        nombre_lignes = 5  # Nombre de lignes de briques
        
        # Calculer combien de briques peuvent tenir sur une ligne
        briques_par_ligne = (XMAX - 2 * espacement_h) // (brique_width + espacement_h)
        
        # Calculer la largeur totale occupée par les briques et les espacements
        largeur_totale = briques_par_ligne * brique_width + (briques_par_ligne - 1) * espacement_h
        
        # Calculer la marge gauche pour centrer les briques horizontalement
        marge_gauche = (XMAX - largeur_totale) / 2
        
        # Marge par rapport au haut de l'écran
        marge_haut = 5
        
        # Génération des briques
        for ligne in range(nombre_lignes):
            for colonne in range(int(briques_par_ligne)):
                # Calculer la position du centre de la brique
                x = marge_gauche + colonne * (brique_width + espacement_h) + brique_width/2
                y = marge_haut + ligne * (brique_height + espacement_v) + brique_height/2
                
                # Possibilité d'ajouter différentes couleurs selon la ligne
                couleur = 'grise'  # Par défaut, mais pourrait varier
                
                # Créer et ajouter la brique
                brique = Brique(x, y, couleur)
                self.liste_briques.append(brique)

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
