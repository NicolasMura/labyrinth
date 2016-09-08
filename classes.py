# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Ce module contient les classes Carte et Labyrinthe utilisées
dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 2.0
"""

import os
import pickle
import copy
from robot import Robot
from obstacles import Obstacle, Mur, Porte, Sortie


class Carte:
    """
    Objet de transition entre un fichier et un labyrinthe.
    """

    def __init__(self, number, filename, name_to_print, string, string_initiale):
        """
        Si on reprend une partie sauvegardée, la carte et son labyrinthe
        associé sont créés avec :
        - string issue du fichier <carte_filename>_save
        - string_initiale issue du fichier <carte_filename>.txt (fichier original)

        Si on reprend une partie du début, les chaînes string et
        string_initiale données en argument sont identiques.
        """

        self.number = number
        self.filename = filename
        self.name_to_print = name_to_print
        self.string = string
        self.string_initiale = string_initiale
        self.char_matrice = []
        self.char_matrice_initiale = []
        self.largeur = 0
        self.hauteur = 0
        self.labyrinth = self.create_labyrinth_from_string(string, string_initiale)

    def __repr__(self):
        return "<Carte {} - {}>".format(self.number, self.name_to_print)

    def create_labyrinth_from_string(self, string, string_initiale):
        """
        Création de 2 listes de listes (matrices char_matrice et
        char_matrice_initiale).

        char_matrice_initiale contient tous les caractères de la carte
        initiale, par ex. :
        char_matrice_initiale = [
            ['O', 'X', 'O', ' ', 'U'],
            ['O', ' ', 'O', ' ', 'O'],
            ['O', ' ', '.', ' ', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]
        pour la carte Ultrafacile.

        char_matrice contient tous les caractères de la carte
        sauvegardée, par ex. :
        char_matrice_initiale = [
            ['O', ' ', 'O', ' ', 'U'],
            ['O', ' ', 'O', ' ', 'O'],
            ['O', ' ', '.', 'X', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]
        pour la carte Ultrafacile.

        On génère ensuite le labryinthe associé.
        """

        char_line = []  # Liste contenant tous les caractères d'une ligne
        char_line_initiale = []  # idem pour la carte initiale
        obstacles = []  # Liste des obstacles (murs O et sortie U)

        # Parcours des caractères des chaînes string et string_initiale
        ligne = 0
        colonne = 0
        for i in range(0, len(string)):
            # Si on n'a pas atteint la fin de la chaîne
            if i < len(string)-1:
                # Si le caractère n'est pas un retour à la ligne
                # on l'ajoute aux listes char_line / char_line_initiale
                if string[i] != "\n":
                    char_line.append(string[i])
                    char_line_initiale.append(string_initiale[i])
                    # Si le caractère est un X,
                    # on en profite pour créer notre robot
                    if string[i] == "X":
                        robot = Robot(colonne, ligne)
                    # Si le caractère est un 'O', un '.'' un 'U', on créé un
                    # obstacle et on enrichit notre collection d'obstacles
                    if string[i] in ["O", ".", "U"]:
                        obstacles.append(Obstacle(colonne, ligne, string[i]))
                    colonne += 1
                # Sinon on ajoute la ligne créée aux matrices char_matrice /
                # char_matrice et on réinitialise char_line /
                # char_line_initiale pour la ligne suivante
                else:
                    self.char_matrice.append(char_line)
                    self.char_matrice_initiale.append(char_line_initiale)
                    char_line = []
                    char_line_initiale = []
                    colonne = 0
                    ligne += 1
            # Sinon, on est sur le dernier caractère de la chaîne
            else:
                # Si c'est un X, on en profite pour créer notre robot
                if string[i] == "X":
                    robot = Robot(colonne, ligne)
                # Si c'est un 'O', un '.'' un 'U', on créé un obstacle
                # et on enrichit notre collection d'obstacles
                if string[i] in ["O", ".", "U"]:
                    obstacles.append(Obstacle(colonne, ligne, string[i]))
                # On ajoute le dernier caractère aux listes char_line /
                # char_line_initiale
                char_line.append(string[i])
                char_line_initiale.append(string_initiale[i])
                # On ajoute la dernière ligne créée aux matrices char_matrice /
                # char_line_initiale
                self.char_matrice.append(char_line)
                self.char_matrice_initiale.append(char_line_initiale)

        # On récupère les largeur / hauteur de la carte
        # self.char_matrice = char_matrice
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
        if self.char_matrice_initiale[robot.last_pos_y][robot.last_pos_x] == ".":
            self.char_matrice[robot.last_pos_y][robot.last_pos_x] = "."
        else:
            self.char_matrice[robot.last_pos_y][robot.last_pos_x] = " "

        # Affectation de la nouvelle position du robot
        self.char_matrice[robot.pos_y][robot.pos_x] = "X"

        self.string = ""
        nb_lignes = 0
        for ligne in self.char_matrice:
            for char in ligne:
                self.string += char
            if nb_lignes < len(self.char_matrice)-1:
                self.string += "\n"
            nb_lignes += 1

    def save(self):
        """
        Fonction permettant d'enregistrer la partie en cours.
        """
        if not os.path.isdir("cartes/sauvegardes/"):
            os.makedirs("cartes/sauvegardes/")
        with open("cartes/sauvegardes/" + self.filename, "wb") as data:
                mypickler = pickle.Pickler(data)
                mypickler.dump(self.string)

    def destroy(self):
        """
        Fonction permettant d'effacer la partie en cours.
        """
        if os.path.isfile("cartes/sauvegardes/" + self.filename):
            os.remove("cartes/sauvegardes/" + self.filename)


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
        Fonction permettant de valider ou non le déplacement du
        robot dans le labyrinthe, et renvoyant deux bouléens :

        - robot_move : True si le déplacement global est valide, False sinon
        - fin_partie : True si on rencontre l'obstacle "U", False sinon
        """

        # On sauvegarde la position du robot avant le déplacement
        robot_pos_x_init = robot.pos_x
        robot_pos_y_init = robot.pos_y

        obstacle_interdit = False
        deplacement_interdit = False
        robot_move = False
        fin_partie = False
        i = 1
        while(i <= nb_cases):
            # On déplace le robot d'une case
            robot.move(sens)

            # On vérifie qu'on ne sort pas des limites du labyrinthe
            if robot.pos_x < 0 or robot.pos_x >= self.largeur or robot.pos_y < 0 or robot.pos_y >= self.hauteur:
                print("Vous ne pouvez pas sortir des limites du labyrinthe !\n")
                deplacement_interdit = True
                robot.pos_x = robot_pos_x_init
                robot.pos_y = robot_pos_y_init
                robot.last_pos_x = robot_pos_x_init
                robot.last_pos_y = robot_pos_y_init
            # Sinon, on vérifie qu'on n'essaie pas de franchir
            # un obstacle interdit
            else:
                for obstacle in self.obstacles:
                    if obstacle.pos_x == robot.pos_x and obstacle.pos_y == robot.pos_y:
                        # Si on est sur un mur, on avertit l'utilisateur
                        # et on annule le déplacement
                        if obstacle.nature == "O":
                            print("Vous ne pouvez pas franchir un mur !\n")
                            robot.pos_x = robot_pos_x_init
                            robot.pos_y = robot_pos_y_init
                            robot.last_pos_x = robot_pos_x_init
                            robot.last_pos_y = robot_pos_y_init
                            obstacle_interdit = True
                        # Si on est sur une porte, on avertit l'utilisateur
                        if obstacle.nature == ".":
                            print("Vous franchissez une porte...\n")
                        # Si on est sur la sortie, on regarde si
                        # l'utilisateur s'est arrêté dessus ou pas
                        if obstacle.nature == "U":
                            if i == nb_cases:
                                fin_partie = True

            # Dès qu'on rencontre un obstacle ou qu'on sort des limites du
            # labyrinthe, on interrompt la boucle
            if obstacle_interdit or deplacement_interdit:
                robot_move = False
                break
            # Sinon le déplacement est OK : on autorise le déplacement
            # et on sauvegarde la précédente position du robot
            else:
                robot_move = True
                robot.last_pos_x = robot_pos_x_init
                robot.last_pos_y = robot_pos_y_init

            i += 1
        return [robot_move, fin_partie]

    def get_help(self):
        print("\nRappel des règles du jeu :")
        print("  - Entrez N pour aller en haut")
        print("  - Entrez E pour aller à droite")
        print("  - Entrez S pour aller en bas")
        print("  - Entrez O pour aller à gauche")
        print("  - Chacune des directions ci-dessus suivies d'un nombre permet d'avancer de \n" \
            "    plusieurs cases (par exemple E3 pour avancer de trois cases vers la droite)")
        print("  - Entrez Q pour quitter la partie")
        print("  - Entrez help pour obtenir de l'aide.\n")
