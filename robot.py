# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Ce module contient la classe Robot utilisée dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 09/09/2016
Version : 2.0
"""


class Robot:
    """
    Classe représentant notre robot.
    """

    symbole = "X"

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.last_pos_x = pos_x
        self.last_pos_y = pos_y

    def __str__(self):
        return "<Objet Robot {x, y} @ ({}, {})>".format(self.pos_x, self.pos_y)

    def move(self, sens):
        """
        Fonction permettant un déplacement élémentaire du robot.
        """

        # On enregistre la nouvelle position
        if sens in ["N", "n"]:
            self.pos_y -= 1
        if sens in ["E", "e"]:
            self.pos_x += 1
        if sens in ["S", "s"]:
            self.pos_y += 1
        if sens in ["O", "o"]:
            self.pos_x -= 1
        return [self.pos_x, self.pos_y]
