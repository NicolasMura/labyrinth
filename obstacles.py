# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Ce module contient la classe Obstacle générique et les classes
dérivées Mur, Porte et Sortie utilisées dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 1.0
"""


class Obstacle:
    """
    Classe représentant un obstacle.
    """

    def __init__(self, pos_x, pos_y, nature):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = (pos_x, pos_y)
        self.nature = nature

    def __repr__(self):
        return "Obstacle {} @ {}".format(self.nature, self.position)


class Mur(Obstacle):

    """Classe représentant un mur, un obstacle impassable."""

    est_franchissable = False
    nom = "mur"
    symbole = "O"


class Porte(Obstacle):

    """Classe représentant une porte, un obstacle passable."""

    est_franchissable = True
    nom = "porte"
    symbole = "."


class Sortie(Obstacle):

    """Classe représentant une sortie du labyrinthe.

    Quand le robot arrive sur cette case, la partie est considérée comme
    terminée.

    """

    est_franchissable = True
    nom = "sortie"
    symbole = "U"

    def arriver(self, labyrinthe, robot):
        """Le robot arrive sur la sortie.

        La partie est gagnée !

        """
        labyrinthe.gagnee = True
