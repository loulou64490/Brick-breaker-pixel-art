"""
Module principal contenant la classe Jeu qui gère le déroulement du jeu
"""
import random
import pygame
from src.constantes import screen, XMAX, YMAX
from src.balle import Balle
from src.raquette import Raquette
from src.brique import Brique
from src.bonus import Bonus
from src.niveaux import NIVEAUX, NOMBRE_MAX_NIVEAUX
from src.sprites import TYPES_BRIQUES, sprite_images

class Jeu:
    """Classe principale qui gère le déroulement du jeu."""
    
    def __init__(self):
        """Initialise une nouvelle partie."""
        self.balles = [Balle()]  # Liste de balles (on commence avec une seule)
        self.raquette = Raquette()
        self.liste_briques = []
        self.liste_bonus = []  # Liste des bonus actifs
        self.vies = 3  # Nombre de vies initial
        self.partie_terminee = False  # État de la partie
        self.niveau = 1  # Niveau de départ
        self.victoire_totale = False  # Indique si tous les niveaux sont terminés
        
        # Chargement des paramètres du niveau actuel
        self.charger_niveau(self.niveau)

    def charger_niveau(self, niveau):
        """
        Charge les paramètres spécifiques du niveau et génère les briques.
        
        Args:
            niveau (int): Le numéro du niveau à charger
        """
        # Vérifier que le niveau existe
        if niveau > NOMBRE_MAX_NIVEAUX:
            self.victoire_totale = True
            self.partie_terminee = True
            return
            
        # Récupérer les paramètres du niveau
        params_niveau = NIVEAUX[niveau]
        
        # Charger l'arrière-plan
        self.background_image = pygame.image.load(params_niveau['arriere_plan'])
        self.bg_width = self.background_image.get_width()
        self.bg_height = self.background_image.get_height()
        # Calculer la position pour centrer l'image
        self.bg_x = (XMAX - self.bg_width) // 2
        self.bg_y = (YMAX - self.bg_height) // 2
        
        # Sauvegarder les couleurs disponibles pour ce niveau
        self.couleurs_niveau = params_niveau['couleurs_briques']
        
        # Nettoyer les briques précédentes et générer les nouvelles
        self.liste_briques = []
        self.liste_bonus = []  # Vider aussi les bonus en cours
        self.generer_briques()
        
        # Réinitialiser la balle sur la raquette
        self.balles = [Balle()]
        self.raquette = Raquette()

    def generer_briques(self):
        """
        Génère les briques en les disposant de manière aléatoire selon différents patterns.
        Utilise uniquement les couleurs définies pour le niveau actuel.
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
                self.creer_ligne_briques(y, type_brique, espacement_h)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v
                
            elif pattern == 'double':
                # Deux rangées du même type de briques
                type_brique = random.choice(types_disponibles)
                self.creer_ligne_briques(y, type_brique, espacement_h)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v/2
                self.creer_ligne_briques(y, type_brique, espacement_h)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v
                
            elif pattern == 'alternance':
                # Alternance de deux types de briques
                types = random.sample(types_disponibles, 2)
                self.creer_ligne_mixte(y, types, espacement_h)
                y += max(TYPES_BRIQUES[types[0]][1], TYPES_BRIQUES[types[1]][1]) + espacement_v
                
            elif pattern == 'triangle':
                # Disposition en triangle (plus de briques au centre)
                type_brique = random.choice(types_disponibles)
                self.creer_ligne_triangle(y, type_brique, espacement_h)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v
                
            elif pattern == 'zigzag':
                # Disposition en zigzag
                type_brique = random.choice(types_disponibles)
                self.creer_ligne_zigzag(y, type_brique, espacement_h)
                y += TYPES_BRIQUES[type_brique][1] + espacement_v
                
            elif pattern == 'aléatoire':
                # Chaque brique est d'un type aléatoire
                self.creer_ligne_aleatoire(y, types_disponibles, espacement_h)
                y += max(TYPES_BRIQUES[t][1] for t in types_disponibles) + espacement_v

    def creer_brique(self, x, y, type_brique, couleur=None):
        """
        Crée une brique avec une couleur spécifique ou aléatoire parmi celles du niveau.
        
        Args:
            x (int): Position x du centre de la brique
            y (int): Position y du centre de la brique
            type_brique (str): Type de brique
            couleur (str, optional): Couleur spécifique ou None pour aléatoire
        
        Returns:
            Brique: La brique créée
        """
        # Si aucune couleur n'est spécifiée, en choisir une aléatoirement parmi celles du niveau
        couleur_finale = couleur if couleur else random.choice(self.couleurs_niveau)
        return Brique(x, y, type_brique, couleur_finale)

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
            brique = self.creer_brique(x, y + hauteur/2, type_brique)
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
            brique = self.creer_brique(x, y + hauteur/2, type_brique)
            self.liste_briques.append(brique)
            
            # Mettre à jour la position horizontale pour la prochaine brique
            x_courant += largeur + espacement_h

    def creer_ligne_triangle(self, y, type_brique, espacement_h):
        """
        Crée une ligne de briques en forme de triangle (plus dense au centre).
        
        Args:
            y (int): Ordonnée du centre de la ligne
            type_brique (str): Type de brique à créer
            espacement_h (int): Espacement horizontal entre les briques
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
                brique = self.creer_brique(x, y + hauteur/2, type_brique)
                self.liste_briques.append(brique)

    def creer_ligne_zigzag(self, y, type_brique, espacement_h):
        """
        Crée une ligne de briques en zigzag.
        
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
        
        # Décalage vertical pour le zigzag
        decalage_zigzag = hauteur / 2
        
        # Création des briques en zigzag
        for colonne in range(int(briques_par_ligne)):
            # Calculer la position du centre de la brique
            x = marge_gauche + colonne * (largeur + espacement_h) + largeur/2
            
            # Alterner la position verticale (zigzag)
            y_decale = y + (decalage_zigzag if colonne % 2 == 0 else -decalage_zigzag)
            
            # Créer et ajouter la brique
            brique = self.creer_brique(x, y_decale + hauteur/2, type_brique)
            self.liste_briques.append(brique)

    def creer_ligne_aleatoire(self, y, types_briques, espacement_h):
        """
        Crée une ligne de briques avec des types aléatoires.
        
        Args:
            y (int): Ordonnée du centre de la ligne
            types_briques (list): Liste des types de briques disponibles
            espacement_h (int): Espacement horizontal entre les briques
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
                brique = self.creer_brique(x, y + hauteur/2, type_brique)
                self.liste_briques.append(brique)
            
            # Mettre à jour la position horizontale pour la prochaine brique
            x_courant += largeur + espacement_h

    def gestion_evenements(self):
        """Gère les événements utilisateur comme les clics et la fermeture du jeu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # Signale qu'il faut quitter le jeu
                
            elif event.type == pygame.KEYDOWN:
                # Touche espace pour recommencer après fin de partie ou passer au niveau suivant
                if event.key == pygame.K_SPACE:
                    if self.partie_terminee and self.victoire_totale:
                        # Recommencer le jeu depuis le début
                        self.__init__()
                    elif self.partie_terminee:
                        # Recommencer le niveau actuel
                        self.__init__()
                    elif all(balle.sur_raquette for balle in self.balles):
                        # Lancer les balles qui sont sur la raquette
                        for balle in self.balles:
                            if balle.sur_raquette:
                                balle.sur_raquette = False
                                balle.vitesse_par_angle(60)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if all(balle.sur_raquette for balle in self.balles) and not self.partie_terminee:
                        # Lancer toutes les balles qui sont sur la raquette
                        for balle in self.balles:
                            if balle.sur_raquette:
                                balle.sur_raquette = False
                                balle.vitesse_par_angle(60)
        
        return False  # Ne pas quitter le jeu

    def mise_a_jour(self):
        """Met à jour l'état du jeu: position des objets, collisions, etc."""
        # Si la partie est terminée, ne rien mettre à jour
        if self.partie_terminee:
            return
            
        # Récupérer la position horizontale de la souris
        x_souris = pygame.mouse.get_pos()[0]
        
        # Déplacer la raquette
        self.raquette.deplacer(x_souris)
        
        # Mettre à jour l'état de la raquette (bonus temporaires)
        self.raquette.mise_a_jour()
        
        # Balles à enlever (perdues ou sur la raquette après une perte)
        balles_a_supprimer = []
        
        # Déplacer les balles et vérifier les collisions
        for i, balle in enumerate(self.balles):
            perdue = balle.deplacer(self.raquette)
            
            # Si la balle est perdue et ce n'est pas la dernière, on la supprime
            if perdue:
                if len(self.balles) > 1:
                    balles_a_supprimer.append(i)
                else:
                    # C'est la dernière balle, on perd une vie
                    self.vies -= 1
                    if self.vies <= 0:
                        self.partie_terminee = True
            
            # Vérifier les collisions avec les briques
            for brique in self.liste_briques:
                if brique.en_vie():
                    collision, bonus_genere, bonus_x, bonus_y = brique.collision_balle(balle)
                    
                    # Si un bonus est généré, l'ajouter à la liste des bonus actifs
                    if bonus_genere:
                        self.liste_bonus.append(Bonus(bonus_x, bonus_y))
        
        # Supprimer les balles perdues (en partant de la fin pour ne pas perturber les indices)
        for i in sorted(balles_a_supprimer, reverse=True):
            if i < len(self.balles):
                self.balles.pop(i)
        
        # Déplacer et mettre à jour les bonus
        bonus_a_supprimer = []
        for i, bonus in enumerate(self.liste_bonus):
            bonus.deplacer()
            
            # Vérifier si le bonus est ramassé par la raquette
            if bonus.collision_raquette(self.raquette):
                self.appliquer_bonus(bonus)
                bonus_a_supprimer.append(i)
                
            # Supprimer les bonus inactifs
            if not bonus.actif:
                bonus_a_supprimer.append(i)
        
        # Supprimer les bonus à enlever
        for i in sorted(bonus_a_supprimer, reverse=True):
            if i < len(self.liste_bonus):
                self.liste_bonus.pop(i)
        
        # Vérifier si toutes les briques sont détruites (victoire de niveau)
        briques_restantes = sum(1 for brique in self.liste_briques if brique.en_vie())
        if briques_restantes == 0:
            # Passer au niveau suivant
            self.niveau += 1
            
            if self.niveau > NOMBRE_MAX_NIVEAUX:
                # Victoire totale si tous les niveaux sont complétés
                self.partie_terminee = True
                self.victoire_totale = True
            else:
                # Charger le niveau suivant
                self.charger_niveau(self.niveau)
    
    def appliquer_bonus(self, bonus):
        """
        Applique l'effet d'un bonus ramassé par le joueur.
        
        Args:
            bonus (Bonus): Le bonus à appliquer
        """
        if bonus.type == 'vie_plus':
            # Ajouter une vie
            self.vies += 1
            
        elif bonus.type == 'balle_plus':
            # Ajouter une nouvelle balle à côté de la raquette
            nouvelle_balle = Balle(self.raquette.x, self.raquette.y - self.raquette.height, 
                                  random.uniform(-1, 1) * 2, -2)
            nouvelle_balle.sur_raquette = False
            self.balles.append(nouvelle_balle)
            
        elif bonus.type == 'multi_balles':
            # Dupliquer toutes les balles existantes
            nouvelles_balles = []
            for balle in self.balles:
                if not balle.sur_raquette:
                    # Créer une balle similaire mais avec un angle légèrement différent
                    vx = balle.vx * 0.9 + random.uniform(-0.5, 0.5)
                    vy = balle.vy * 0.9 + random.uniform(-0.5, 0.5)
                    nouvelle_balle = Balle(balle.x, balle.y, vx, vy)
                    nouvelle_balle.sur_raquette = False
                    nouvelles_balles.append(nouvelle_balle)
            
            # Ajouter les nouvelles balles à la liste
            self.balles.extend(nouvelles_balles)
            
        elif bonus.type == 'raquette_large':
            # Élargir temporairement la raquette
            self.raquette.elargir()
    
    def affichage(self):
        """Affiche tous les éléments du jeu à l'écran."""
        # Fond noir pour les bords potentiels
        screen.fill((0, 0, 0))
        
        # Affichage de l'image de fond centrée
        screen.blit(self.background_image, (self.bg_x, self.bg_y))
        
        # Affichage des briques encore en vie
        for brique in self.liste_briques:
            if brique.en_vie():
                brique.afficher()
        
        # Affichage des bonus actifs
        for bonus in self.liste_bonus:
            bonus.afficher()
        
        # Affichage de la raquette
        self.raquette.afficher()
        
        # Affichage des balles
        for balle in self.balles:
            balle.afficher()
                
        # Affichage des vies
        self.afficher_vies()
        
        # Affichage de l'écran de fin si la partie est terminée
        if self.partie_terminee:
            self.afficher_fin_partie()
            
    def afficher_vies(self):
        """Affiche les icônes de vie en haut à droite de l'écran."""
        if self.vies <= 0:
            return  # Pas de vies à afficher
            
        # Déterminer le sprite principal selon le nombre de vies (1, 2 ou 3+)
        if self.vies >= 3:
            sprite_principal = sprite_images['vie3']
            vies_principales = 3
        elif self.vies == 2:
            sprite_principal = sprite_images['vie2']
            vies_principales = 2
        else:  # self.vies == 1
            sprite_principal = sprite_images['vie1']
            vies_principales = 1
        
        # Calculer combien de vies supplémentaires il faut afficher
        vies_restantes = self.vies - vies_principales
        
        largeur_vie = sprite_principal.get_width()
        hauteur_vie = sprite_principal.get_height()
        marge = 5  # Espacement entre les icônes
        
        # Position pour le sprite principal (en haut à droite de l'écran)
        x = XMAX - largeur_vie - 10  # 10 pixels de marge par rapport au bord droit
        y = 10
        
        # Afficher le sprite principal
        screen.blit(sprite_principal, (x, y))
        
        # Afficher les vies supplémentaires de façon optimisée
        while vies_restantes > 0:
            x -= (largeur_vie + marge)
            
            if vies_restantes >= 3:
                # Utiliser un coeur de 3 vies
                screen.blit(sprite_images['vie3'], (x, y))
                vies_restantes -= 3
            elif vies_restantes == 2:
                # Utiliser un coeur de 2 vies
                screen.blit(sprite_images['vie2'], (x, y))
                vies_restantes -= 2
            else:  # vies_restantes == 1
                # Utiliser un coeur de 1 vie
                screen.blit(sprite_images['vie1'], (x, y))
                vies_restantes -= 1
            
    def afficher_fin_partie(self):
        """Affiche un indicateur visuel de fin de partie sans texte."""
        # Créer une surface semi-transparente
        overlay = pygame.Surface((XMAX, YMAX), pygame.SRCALPHA)
        
        # Choisir la couleur en fonction de la situation
        if self.vies <= 0:
            # Rouge pour défaite
            overlay.fill((255, 50, 50, 128))
        elif self.victoire_totale:
            # Or pour victoire totale
            overlay.fill((255, 215, 0, 128))
        else:
            # Vert pour niveau terminé
            overlay.fill((50, 255, 50, 128))
        
        # Afficher l'overlay
        screen.blit(overlay, (0, 0)) 