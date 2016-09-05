# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Mainfile - Exécutez-le avec Python 3 pour lancer le jeu.

Auteur  : Nicolas MURA
Date    : 02/09/2016
Version : 1.0
"""
from os import path, remove
from functions import *
import pickle
from classes import *

print("\nBienvenu(e) dans le jeu du labyrinthe !\n")
# Récupération et affichage du nom des cartes existantes,
# ou affichage d'un message approprié si aucune carte trouvée
maps = get_maps()

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
            remove("cartes/" + map_selected["filename"] + "_save")

# Récupération de la carte sélectionnée
# sous forme de chaîne de caractères
(string_map, string_map_initiale) = get_string_map(
    map_selected, reprendre_partie)

# Création d'un objet carte avec la chaîne de caractères récupérée string_map
carte = Carte(
    map_selected["number"],
    map_selected["name"],
    string_map, string_map_initiale)

# Récupération du labyrinthe et du robot
labyrinth = carte.labyrinth
robot = carte.labyrinth.robot

# On lance le jeu avec un petit rappel des règles
print("""\nRappel des règles du jeu :
- Entrer N pour aller en haut
- Entrer E pour aller à droite
- Entrer S pour aller en bas
- Entrer O pour aller à gauche
- Chacune des directions ci-dessus suivies d'un nombre permet d'avancer de
  plusieurs cases (par exemple E3 pour avancer de trois cases vers la droite)
- Entrer q ou Q pour quitter la partie\n""")

continue_partie = True

nb_deplacements = 0
while(continue_partie):
    # Affichage de la carte
    print(carte.string, "\n")

    user_input = input("> ")

    # Si l'utilisateur quitte le jeu, on enregistre la chaîne
    # représentant l'état de la carte dans sa dernière version
    # (à condition qu'il y ait eu au moins 1 déplacement)
    if user_input == "q" or user_input == "Q":
        continue_partie = False
        if nb_deplacements > 0:
            with open("cartes/" + map_selected["filename"] + "_save", "wb") as data:
                mypickler = pickle.Pickler(data)
                mypickler.dump(carte.string)
            print("La partie en cours a été sauvegardée. A bientôt...\n")
    else:
        deplacement = check_user_input(user_input)
        # Si la saisie utilisateur est correcte, on essaie de déplacer le robot
        if deplacement["check"] is True:
            [robot_move, fin_partie] = labyrinth.robot_move(
                robot,
                deplacement["sens"],
                deplacement["nb_cases"]
            )
            if robot_move is True:
                carte.update_carte_string(robot)
                nb_deplacements += 1
                if fin_partie is True:
                    print(carte.string, "\n")
                    print("Félicitations ! Vous avez gagné !\n")
                    continue_partie = False
                    # On efface une éventuelle partie sauvegardée
                    if path.isfile("cartes/" + map_selected["filename"] + "_save"):
                        remove("cartes/" + map_selected["filename"] + "_save")
