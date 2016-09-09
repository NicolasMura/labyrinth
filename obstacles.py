# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Ce module contient la classe Obstacle générique et ses classes
dérivées Mur, Porte et Sortie utilisées dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 1.0
"""


class Obstacle:
    """
    Classe représentant un obstacle générique.
    """

    def __init__(self, pos_x, pos_y, name):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = (pos_x, pos_y)
        self.name = name

    def __repr__(self):
        return "Obstacle {} @ {}".format(self.name, self.position)


class Mur(Obstacle):
    """Classe représentant un mur, un obstacle non franchissable."""

    can_be_crossed = False
    name = "mur"
    symbole = "O"


class Porte(Obstacle):
    """Classe représentant une porte, un obstacle franchissable."""

    can_be_crossed = True
    name = "porte"
    symbole = "."


class Sortie(Obstacle):
    """Classe représentant une sortie du labyrinthe."""

    can_be_crossed = True
    name = "sortie"
    symbole = "U"
