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
from src.sons import jouer_son_bonus, jouer_son_rebond, jouer_son_explosion

# Importation des modules créés pour la refactorisation
from src.gestion_briques import generer_briques, creer_brique
from src.gestion_niveaux import charger_niveau, initialiser_niveau
from src.gestion_affichage import afficher_vies
from src.ecrans import charger_police, creer_overlay
from src.boutons import Bouton

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
        self.en_pause = False  # État de pause du jeu
        self.retour_menu = False  # Indique si le joueur veut retourner au menu principal
        self.polices = charger_police()  # Charger les polices personnalisées
        
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
        
        # Afficher les informations du niveau (pour le débogage)
        description = NIVEAUX[niveau].get('description', f'Niveau {niveau}')
        print(f"Niveau {niveau} chargé: {description}")

    def gestion_evenements(self):
        """Gère les événements utilisateur comme les clics et la fermeture du jeu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Libérer la souris avant de quitter
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                return True  # Signale qu'il faut quitter le jeu
                
            elif event.type == pygame.KEYDOWN:
                # Touche pour mettre en pause (P ou Échap)
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    self.en_pause = not self.en_pause
                    # Afficher/cacher le curseur selon l'état de pause
                    pygame.mouse.set_visible(self.en_pause)
                    pygame.event.set_grab(not self.en_pause)
                
                # Touche espace pour lancer les balles sur la raquette (si pas en pause)
                elif event.key == pygame.K_SPACE and not self.en_pause:
                    if not self.partie_terminee and all(balle.sur_raquette for balle in self.balles):
                        # Lancer les balles qui sont sur la raquette
                        for balle in self.balles:
                            if balle.sur_raquette:
                                balle.sur_raquette = False
                                balle.vitesse_par_angle(random.randint(30, 120))
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if self.en_pause:
                        # Vérifier si le bouton "Menu principal" est cliqué en pause
                        pos = pygame.mouse.get_pos()
                        if hasattr(self, 'bouton_menu_principal') and self.bouton_menu_principal.est_clique(pos):
                            self.retour_menu = True
                            self.partie_terminee = True
                            self.en_pause = False
                    elif all(balle.sur_raquette for balle in self.balles) and not self.partie_terminee:
                        # Lancer toutes les balles qui sont sur la raquette
                        for balle in self.balles:
                            if balle.sur_raquette:
                                balle.sur_raquette = False
                                balle.vitesse_par_angle(random.randint(88, 92))
        
        return False  # Ne pas quitter le jeu

    def mise_a_jour(self):
        """Met à jour l'état du jeu: position des objets, collisions, etc."""
        # Si la partie est terminée ou en pause, ne rien mettre à jour
        if self.partie_terminee or self.en_pause:
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
                    
                    # Si collision, jouer le son de rebond
                    if collision:
                        jouer_son_rebond()
                        
                        # Si la brique est détruite, jouer le son d'explosion
                        if not brique.en_vie():
                            jouer_son_explosion()
                    
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
                # Jouer le son du bonus
                jouer_son_bonus()
                
                # Appliquer le bonus directement avec sa méthode
                self.vies, self.balles = bonus.appliquer(self.vies, self.balles, self.raquette)
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
                print("Félicitations ! Vous avez terminé tous les niveaux !")
            else:
                # Charger le niveau suivant
                print(f"Niveau {self.niveau-1} terminé ! Passage au niveau {self.niveau}")
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
        
        # Afficher l'écran de pause si le jeu est en pause
        if self.en_pause:
            self.afficher_ecran_pause()
    
    def afficher_ecran_pause(self):
        """Affiche l'écran de pause avec les options"""
        # Créer un overlay semi-transparent
        overlay = creer_overlay((0, 0, 0), 150)
        screen.blit(overlay, (0, 0))
        
        # Afficher le titre "PAUSE"
        titre_texte = self.polices['titre'].render("PAUSE", True, (255, 255, 255))
        titre_rect = titre_texte.get_rect(center=(XMAX // 2, YMAX // 2 - 50))
        screen.blit(titre_texte, titre_rect)
        
        # Créer le bouton "Menu principal"
        self.bouton_menu_principal = Bouton(XMAX/2, YMAX/2 + 30, 145, 25, "Menu principal", self.polices['bouton'])
        
        # Mettre à jour l'état du bouton
        self.bouton_menu_principal.verifier_survol(pygame.mouse.get_pos())
        
        # Dessiner le bouton
        self.bouton_menu_principal.dessiner()