# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Mainfile - Pour lancer le jeu, exécutez :
> python3 roboc.py sous OS X
> py -3 roboc.py sous Windows

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 2.0
"""

import os
from functions import *
from classes import *


if os.name == "nt":  # Cas Windows
    os.system('cls')
else:
    os.system("clear")

print("\nBienvenu(e) dans le jeu du labyrinthe !\n")
# Récupération et affichage du nom des cartes existantes,
# ou affichage d'un message approprié si aucune carte trouvée
maps = get_maps()
if maps is None:
    raise TypeError("Erreur : votre projet doit contenir un dossier 'cartes' avec au moins une carte valide.")

# Sélection et récupération d'une carte par l'utilisateur
map_selected = chose_map(maps)

# Si une partie est déjà en cours sur le labyrinthe sélectionné,
# on demande à l'utilisateur s'il veut la poursuivre
reprendre_partie = False
if map_selected["en_cours"] is True:
    user_input = False
    while(user_input not in ["Y", "y", "N", "n"]):
        user_input = input("Une partie est en cours sur ce labyrinthe : souhaitez-vous la reprendre ? (Y/n) ")
        if user_input in ["Y", "y"]:
            reprendre_partie = True
        elif user_input in ["N", "n"]:
            reprendre_partie = False
            # On efface la partie sauvegardée
            os.remove("cartes/sauvegardes/" + map_selected["filename"])

# Récupération de la carte sélectionnée et d'une éventuelle sauvegarde
# sous forme de chaîne de caractères
(string_map_saved, string_map_initiale) = get_string_map(
    map_selected, reprendre_partie)

# Création d'un objet carte
carte = Carte(
    map_selected["number"],
    map_selected["filename"],
    map_selected["name_to_print"],
    string_map_saved, string_map_initiale)

# Récupération du labyrinthe et du robot
labyrinth = carte.labyrinth
robot = carte.labyrinth.robot

# On lance le jeu avec un petit rappel des règles
labyrinth.get_help()

continue_partie = True

nb_deplacements = 0
while(continue_partie):
    # Affichage de la carte
    print(carte.string, "\n")

    user_input = input("> ")

    # Si l'utilisateur quitte le jeu, on enregistre la chaîne
    # représentant l'état de la carte dans sa dernière version
    # (à condition qu'il y ait eu au moins 1 déplacement)
    if user_input in ["Q", "q"]:
        continue_partie = False
        if nb_deplacements > 0:
            carte.save()
            print("La partie en cours a été sauvegardée. A bientôt...\n")
        else:
            print("A bientôt... (PS : comme vous n'avez pas déplacé le robot, la partie reste en l'état)\n")
    elif user_input == "help":
        labyrinth.get_help()
    else:
        deplacement = check_user_input(user_input)
        # Si la saisie utilisateur est correcte, on essaie de déplacer le robot
        if deplacement["check"] is True:
            fin_partie = labyrinth.robot_move(
                robot,
                deplacement["sens"],
                deplacement["nb_cases"]
            )
            # if robot_move is True:
            carte.update_carte_string(robot)
            nb_deplacements += 1
            if fin_partie is True:
                print(carte.string, "\n")
                print("Félicitations ! Vous avez gagné !\n")
                continue_partie = False
                # On efface une éventuelle partie sauvegardée
                carte.destroy()
