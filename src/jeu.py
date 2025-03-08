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

# Importation des modules créés pour la refactorisation
from src.gestion_briques import generer_briques, creer_brique
from src.gestion_niveaux import charger_niveau, initialiser_niveau
from src.gestion_bonus import appliquer_bonus
from src.gestion_affichage import afficher_vies, afficher_fin_partie

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
        # Utiliser la fonction de gestion_niveaux
        victoire_totale, partie_terminee, background_image, bg_x, bg_y, couleurs_niveau, liste_briques, liste_bonus, balles, raquette = initialiser_niveau(niveau, TYPES_BRIQUES)
        
        # Mettre à jour les attributs de l'objet
        self.victoire_totale = victoire_totale
        self.partie_terminee = partie_terminee
        
        # Si victoire totale, ne rien faire de plus
        if self.victoire_totale:
            return
            
        # Mettre à jour les attributs liés au niveau
        self.background_image = background_image
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.couleurs_niveau = couleurs_niveau
        
        # Nettoyer les briques précédentes et générer les nouvelles
        self.liste_briques = liste_briques
        self.liste_bonus = liste_bonus
        
        # Réinitialiser la balle sur la raquette et la raquette
        if raquette:
            self.balles = balles
            self.raquette = raquette

    def generer_briques(self):
        """
        Génère les briques en les disposant de manière aléatoire selon différents patterns.
        Utilise uniquement les couleurs définies pour le niveau actuel.
        """
        # Utiliser la fonction de gestion_briques
        self.liste_briques = []
        generer_briques(self.couleurs_niveau, self.liste_briques, XMAX, TYPES_BRIQUES)

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
                # Utiliser la fonction du module gestion_bonus
                self.vies, self.balles = appliquer_bonus(bonus, self.vies, self.balles, self.raquette)
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
                
        # Affichage des vies (utiliser la fonction du module gestion_affichage)
        afficher_vies(self.vies, XMAX)
        
        # Affichage de l'écran de fin si la partie est terminée (utiliser la fonction du module gestion_affichage)
        afficher_fin_partie(self.partie_terminee, self.vies, self.victoire_totale) 