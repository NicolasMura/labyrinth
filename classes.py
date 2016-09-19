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
from robot import Robot
from obstacles import Obstacle, Mur, Porte, Sortie


class Carte:
    """
    Objet de transition entre un fichier et un labyrinthe.
    """

    def __init__(self, number, filename, name_to_print, string, string_initiale):
        """
        Initialisation d'une carte.

        Soit on reprend une partie sauvegardée, la carte et son labyrinthe
        associé sont créés avec :
        - string_saved issue du fichier cartes/sauvegardes/<carte_filename>.txt
        - string_initiale issue du fichier <carte_filename>.txt (fichier original)

        Soit on reprend une partie du début, et dans ce cas
        string_saved = string_initiale
        """

        self.number = number
        self.filename = filename
        self.name_to_print = name_to_print
        self.string = string
        self.string_initiale = string_initiale
        self.char_matrice = []
        self.char_matrice_initiale = []
        self.labyrinth = self.create_labyrinth_from_string(string, string_initiale)
        self.largeur = self.labyrinth.largeur
        self.hauteur = self.labyrinth.hauteur

    def __repr__(self):
        return "<Carte {} - {}>".format(self.number, self.name_to_print)

    def create_labyrinth_from_string(self, string, string_initiale):
        """
        Création de 2 matrices : matrices char_matrice et
        char_matrice_initiale.

        * char_matrice_initiale contiendra tous les caractères de la carte
        initiale, par ex. :
        char_matrice_initiale = [
            ['O', 'X', 'O', ' ', 'U'],
            ['O', ' ', 'O', ' ', 'O'],
            ['O', ' ', '.', ' ', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]

        * char_matrice contiendra tous les caractères de la carte
        sauvegardée (si on reprend un partie sauvegardée), par ex. :
        char_matrice_initiale = [
            ['O', ' ', 'O', ' ', 'U'],
            ['O', ' ', 'O', ' ', 'O'],
            ['O', ' ', '.', 'X', 'O'],
            ['O', 'O', 'O', 'O', 'O']
        ]

        Si on reprend la partie depuis le début, les deux matrices
        sont identiques car dans ce cas string = string_initiale.

        On génère ensuite le labyrinthe associé.
        """

        char_line = []           # Liste contenant tous les caractères d'une ligne
        char_line_initiale = []  # idem pour la carte initiale
        obstacles = []           # Liste des obstacles

        ligne = 0
        colonne = 0
        robot = None
        # Parcours des chaînes string et string_initiale
        for i in range(0, len(string)):

            # Si le caractère est un retour à la ligne on ajoute la ligne
            # créée aux matrices char_matrice / char_matrice_initiale et on
            # réinitialise char_line /char_line_initiale pour la ligne suivante
            if string[i] == "\n":
                self.char_matrice.append(char_line)
                self.char_matrice_initiale.append(char_line_initiale)
                char_line, char_line_initiale = [], []
                colonne = 0
                ligne += 1
            # Sinon, on l'ajoute aux listes char_line / char_line_initiale
            else:
                char_line.append(string[i])
                char_line_initiale.append(string_initiale[i])
                if string[i] == Robot.symbole:
                    if robot is not None:
                        raise ValueError("Erreur lors de la génération du labyrinthe : il ne peut y avoir qu'un seul robot.")
                    robot = Robot(colonne, ligne)  # Création du robot
                elif string[i] == Mur.symbole:
                    obstacles.append(Mur(colonne, ligne, Mur.name))  # Création d'un obstacle
                elif string[i] == Porte.symbole:
                    obstacles.append(Porte(colonne, ligne, Porte.name))  # Création d'un obstacle
                elif string[i] == Sortie.symbole:
                    obstacles.append(Sortie(colonne, ligne, Sortie.name))  # Création d'un obstacle
                elif string[i] == " ":
                    pass
                else:
                    raise ValueError("Erreur lors de la génération du labyrinthe : symbole '{}' inconnu.".format(string[i]))
                # Si c'est le dernier caractère
                if i == len(string)-1:
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
        Fonction permettant de déplacer le robot dans le labyrinthe,
        et renvoyant un bouléen :

        - fin_partie : True si on rencontre une obstacle de type Sortie,
        False sinon
        """

        robot_move = False
        deplacement_interdit = False
        fin_partie = False

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
                print("Vous ne pouvez pas sortir des limites du labyrinthe !\n")
                robot.pos_x = robot_pos_x_save
                robot.pos_y = robot_pos_y_save
                deplacement_interdit = True
            # Sinon, on regarde si on est sur un obstacle
            else:
                for obstacle in self.obstacles:
                    if obstacle.pos_x == robot.pos_x and obstacle.pos_y == robot.pos_y:
                        # Si l'obstacle est infranchissable, on arrête le déplacement
                        if not obstacle.can_be_crossed:
                            robot.pos_x = robot_pos_x_save
                            robot.pos_y = robot_pos_y_save
                            deplacement_interdit = True
                        # Si on est sur la sortie
                        if type(obstacle) == Sortie:
                            fin_partie = True
                        # Autres retours utilisateurs
                        if type(obstacle) == Mur:
                            print("Vous ne pouvez pas franchir un obstacle {} !\n".format(Mur.name))
                        if type(obstacle) == Porte:
                            print("Vous franchissez un obstacle {}...\n".format(Porte.name))

            # Pour un déplacement interdit, on stoppe le déplacement
            # et on sort de la boucle while
            if deplacement_interdit:
                break
            else:
                i += 1

        return fin_partie

    def get_help(self):
        help_content = "\nRappel des règles du jeu :\n" \
        "  - Entrez N pour aller en haut\n" \
        "  - Entrez E pour aller à droite\n" \
        "  - Entrez S pour aller en bas\n" \
        "  - Entrez O pour aller à gauche\n" \
        "  - Chacune des directions ci-dessus suivies d'un nombre permet d'avancer de \n" \
            "    plusieurs cases (par exemple E3 pour avancer de trois cases vers la droite)\n" \
        "  - Entrez Q pour quitter la partie\n" \
        "  - Entrez help pour obtenir de l'aide.\n" \
        "  - Entrez lab pour afficher le labyrinthe.\n"
        return help_content
