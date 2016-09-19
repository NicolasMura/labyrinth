# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Ce module contient les classes Carte et Labyrinthe utilisées
dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 2.0
"""

import global_variables_server
import os
import pickle
from robot import Robot
from obstacles import Obstacle, Mur, Porte, Sortie


class Carte:
    """
    Objet de transition entre un fichier et un labyrinthe.
    """

    def __init__(self, number, filename, name_to_print, string_initiale):
        """
        Initialisation d'une carte.

        La carte et son labyrinthe associé sont créés avec :
        - string_initiale issue du fichier <carte_filename>.txt
        """

        self.number = number
        self.filename = filename
        self.name_to_print = name_to_print
        self.string = string_initiale
        self.string_initiale = string_initiale
        self.char_matrice = []
        self.char_matrice_initiale = []
        self.labyrinth = self.create_labyrinth_from_string(string_initiale)
        self.largeur = self.labyrinth.largeur
        self.hauteur = self.labyrinth.hauteur

    def __repr__(self):
        return "<Carte {} - {}>".format(self.number, self.name_to_print)

    def create_labyrinth_from_string(self, string_initiale):
        """
        Création de la matrice char_matrice_initiale qui contiendra tous les
        caractères de la carte initiale, par ex. :
        char_matrice_initiale = [
            ['O', 'X', 'O', ' ', 'U'],
            ['O', ' ', 'O', ' ', 'O'],
            ['O', ' ', '.', ' ', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]

        On génère ensuite le labyrinthe associé.
        """

        char_line = []           # Liste de tous les caractères d'une ligne
        char_line_initiale = []  # idem pour la carte initiale
        obstacles = []           # Liste des obstacles

        ligne = 0
        colonne = 0
        robot = None
        # Parcours de la chaîne string_initiale
        for i in range(0, len(string_initiale)):

            # Si le caractère est un retour à la ligne on ajoute la ligne
            # créée aux matrices char_matrice / char_matrice_initiale et on
            # réinitialise char_line /char_line_initiale pour la ligne suivante
            if string_initiale[i] == "\n":
                self.char_matrice.append(char_line)
                self.char_matrice_initiale.append(char_line_initiale)
                char_line, char_line_initiale = [], []
                colonne = 0
                ligne += 1
            # Sinon, on l'ajoute aux listes char_line / char_line_initiale
            else:
                char_line.append(string_initiale[i])
                char_line_initiale.append(string_initiale[i])
                if string_initiale[i] == Robot.symbole:
                    if robot is not None:
                        raise ValueError("Erreur lors de la génération du labyrinthe : il ne peut y avoir qu'un seul robot.")
                    robot = Robot(colonne, ligne)  # Création du robot
                # Création des obstacles:
                elif string_initiale[i] == Mur.symbole:
                    obstacles.append(Mur(colonne, ligne, Mur.name))
                elif string_initiale[i] == Porte.symbole:
                    obstacles.append(Porte(colonne, ligne, Porte.name))
                elif string_initiale[i] == Sortie.symbole:
                    obstacles.append(Sortie(colonne, ligne, Sortie.name))
                elif string_initiale[i] == " ":
                    pass
                else:
                    raise ValueError("Erreur lors de la génération du labyrinthe : symbole '{}' inconnu.".format(string_initiale[i]))
                # Si c'est le dernier caractère
                if i == len(string_initiale)-1:
                    self.char_matrice.append(char_line)
                    self.char_matrice_initiale.append(char_line_initiale)
                colonne += 1

        # On récupère les largeur / hauteur de la carte
        self.largeur = len(self.char_matrice[0])
        self.hauteur = len(self.char_matrice)

        # Finalement, on crée l'objet Labyrinthe associé :
        self.labyrinth = Labyrinthe(
            robot, self.largeur, self.hauteur, obstacles)
        return self.labyrinth

    def update_carte_string(self, robot):
        """
        Fonction permettant de mettre à jour la matrice puis la chaîne
        associées à la carte.
        Elle remplace l'ancienne position du robot par un espace " " (ou "."
        pour une porte), et la nouvelle par un "X".
        """

        # On regarde si l'ancienne position du robot était une porte
        if self.char_matrice_initiale[robot.last_pos_y][robot.last_pos_x] == Porte.symbole:
            self.char_matrice[robot.last_pos_y][robot.last_pos_x] = Porte.symbole
        else:
            self.char_matrice[robot.last_pos_y][robot.last_pos_x] = " "

        # Affectation de la nouvelle position du robot
        self.char_matrice[robot.pos_y][robot.pos_x] = Robot.symbole

        # Mise à jour de la chaîne self.string
        self.string = ""
        nb_lignes = 0
        for ligne in self.char_matrice:
            for char in ligne:
                self.string += char
            if nb_lignes < len(self.char_matrice)-1:
                self.string += "\n"
            nb_lignes += 1


class Labyrinthe:
    """
    Classe représentant un labyrinthe.
    """

    def __init__(self, robot, largeur, hauteur, obstacles):
        """
        Un Labyrinthe est représenté par 4 objets :

        - un robot
        - une largeur
        - une hauteur
        - un ensemble d'obstacles
        """
        self.robot = robot
        self.largeur = largeur
        self.hauteur = hauteur
        self.obstacles = obstacles

    def robot_move(self, robot, sens, nb_cases):
        """
        Fonction permettant de déplacer le robot dans le labyrinthe,
        et renvoyant un dictionnaire :

        {
            "check" : check,
            "info" : info,
            "fin_partie" : fin_partie # True si on rencontre une obstacle de type Sortie,
        }
        """

        check = False
        info = ""
        fin_partie = False

        robot_move = False
        deplacement_interdit = False

        # On sauvegarde la position du robot
        robot.last_pos_x = robot.pos_x
        robot.last_pos_y = robot.pos_y

        i = 1
        while(i <= nb_cases):
            # On sauvegarde la position du robot avant le déplacement
            robot_pos_x_save = robot.pos_x
            robot_pos_y_save = robot.pos_y

            # On déplace le robot d'une case
            robot.move(sens)

            # On vérifie qu'on ne sort pas des limites du labyrinthe
            if robot.pos_x < 0 or robot.pos_x >= self.largeur or robot.pos_y < 0 or robot.pos_y >= self.hauteur:
                info = "Vous ne pouvez pas sortir des limites " \
                    "du labyrinthe !\n"
                robot.pos_x = robot_pos_x_save
                robot.pos_y = robot_pos_y_save
                deplacement_interdit = True
            # Sinon, on regarde si on est sur un obstacle
            else:
                for obstacle in self.obstacles:
                    if obstacle.pos_x == robot.pos_x and obstacle.pos_y == robot.pos_y:
                        # Si l'obstacle est infranchissable,
                        # on arrête le déplacement
                        if not obstacle.can_be_crossed:
                            robot.pos_x = robot_pos_x_save
                            robot.pos_y = robot_pos_y_save
                            deplacement_interdit = True
                        # Si on est sur la sortie
                        if type(obstacle) == Sortie:
                            fin_partie = True
                        # Autres retours utilisateurs
                        if type(obstacle) == Mur:
                            info = "Vous ne pouvez pas franchir un " \
                                "obstacle {} !\n".format(Mur.name)
                        if type(obstacle) == Porte:
                            info = "Vous franchissez un " \
                                "obstacle {}...\n".format(Porte.name)

            # Pour un déplacement interdit, on stoppe le déplacement
            # et on sort de la boucle while
            if deplacement_interdit:
                break
            else:
                i += 1
                # S'il y a eu au moins 1 déplacement,
                # le déplacement global est valide
                if i >= 1:
                    check = True

        return {
            "check": check,
            "info": info,
            "fin_partie": fin_partie
        }

    def robot_do(self, robot, sens, action):
        """
        Fonction permettant de murer une porte dans le labyrinthe,
        et renvoyant un dictionnaire :

        {
            "check" : check,
            "info" : info,
        }
        """

        check = False
        info = ""

        cible_x = robot.pos_x
        cible_y = robot.pos_y

        if sens == "N":
            cible_y = robot.pos_y - 1
        if sens == "E":
            cible_x = robot.pos_x + 1
        if sens == "S":
            cible_y = robot.pos_y + 1
        if sens == "O":
            cible_x = robot.pos_x - 1

        # On vérifie qu'on ne sort pas des limites du labyrinthe...
        if cible_x < 0 or cible_x >= self.largeur or cible_y < 0 or cible_y >= self.hauteur:
            if action == "wall_up":
                info = "Vous ne pouvez pas murer au-delà des limites du " \
                    "labyrinthe !"
            if action == "wall_down":
                info = "Vous ne pouvez pas percer au-delà des limites du " \
                    "labyrinthe !"
        # ... et qu'il y a bien un obstacle
        elif global_variables_server.carte.char_matrice[cible_y][cible_x] == " ":
            if action == "wall_up":
                info = "Il n'y a strictement rien à murer ici !"
            if action == "wall_down":
                info = "Il n'y a strictement rien à percer ici !"
        # Sinon, on vérifie le type d'obstacle que l'utilisateur
        # essaie de murer
        else:
            for indice, obstacle in enumerate(self.obstacles):
                if obstacle.pos_x == cible_x and obstacle.pos_y == cible_y:
                    if action == "wall_up":
                        # Si l'obstacle est une porte
                        if type(obstacle) == Porte:
                            info = "Vous murez une porte !"
                            check = True
                            # On sauvegarde l'indice de cette porte
                            indice_porte = indice
                        else:
                            if type(obstacle) == Mur:
                                info = "Vous ne pouvez pas murer un obstacle " \
                                    "de type {} !".format(Mur.name)
                            elif type(obstacle) == Sortie:
                                info = "Vous ne pouvez pas murer un obstacle " \
                                    "de type {} !".format(Sortie.name)
                            else:
                                info = "??? Cas pas testé ???"
                    if action == "wall_down":
                        # Si l'obstacle est un mur
                        if type(obstacle) == Mur:
                            info = "Vous percez un mur !"
                            check = True
                            # On sauvegarde l'indice de ce mur
                            indice_mur = indice
                        else:
                            if type(obstacle) == Porte:
                                info = "Vous ne pouvez pas percer un obstacle " \
                                    "de type {} !".format(Porte.name)
                            elif type(obstacle) == Sortie:
                                info = "Vous ne pouvez pas percer un obstacle " \
                                    "de type {} !".format(Sortie.name)
                            else:
                                info = "??? Cas pas testé ???"

        if check:
            if action == "wall_up":
                # Mise à jour de la carte
                global_variables_server.carte.char_matrice[cible_y][cible_x] = Mur.symbole
                # Mise à jour de la liste des obstacles
                del self.obstacles[indice_porte]
                self.obstacles.append(Mur(cible_x, cible_y, Mur.name))
            if action == "wall_down":
                # Mise à jour de la carte
                global_variables_server.carte.char_matrice[cible_y][cible_x] = Porte.symbole
                # Mise à jour de la liste des obstacles
                del self.obstacles[indice_mur]
                self.obstacles.append(Porte(cible_x, cible_y, Porte.name))
            global_variables_server.carte.update_carte_string(robot)
        return {
            "check": check,
            "info": info
        }

    def get_help(self):
        help_content = "\nRappel des règles du jeu :\n" \
            "  - Entrez N pour aller en haut\n" \
            "  - Entrez E pour aller à droite\n" \
            "  - Entrez S pour aller en bas\n" \
            "  - Entrez O pour aller à gauche\n" \
            "  - Chacune des directions ci-dessus suivies d'un nombre " \
            "permet d'avancer de \n" \
            "    plusieurs cases (par exemple E3 pour avancer " \
            "de trois cases vers la droite)\n" \
            "  - Entrez M + une direction pour murer une porte\n" \
            "  - Entrez Q pour quitter la partie\n" \
            "  - Entrez help pour obtenir de l'aide.\n" \
            "  - Entrez lab pour afficher le labyrinthe.\n"
        return help_content
