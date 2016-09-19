# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Fonctions utilisées dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 02/09/2016
Version : 1.0
"""

import os
import pickle


def get_maps():
    """
    Fonction qui permet de récupérer l'ensemble des informations
    des cartes situées dans un répertoire 'cartes', sous la forme
    d'un dictionnaire de dictionnaires, par ex. :

    maps = {
        {
            "number": '0',
            "filename": 'cartes/facile.txt',
            "name_to_print": 'Facile',
            "en_cours": False,
        },
        {
            ...
        }
    }
    """

    maps_names_list = []
    maps = {}
    en_cours = False
    if os.path.isdir("cartes"):
        for filename in os.listdir("cartes"):
            if filename.endswith(".txt"):
                maps_names_list.append(filename)

        if len(maps_names_list) > 0:
            print("Labyrinthes existants :")
            i = 0
            for key, filename in enumerate(maps_names_list):
                # Nettoyage des noms des fichiers
                name_to_print = filename.replace(".txt", "").lower().capitalize()
                # Si on détecte qu'une partie est en cours
                # on l'enregistre
                if os.path.isfile("cartes/sauvegardes/" + filename):
                    en_cours = True
                    name_to_print += " (partie en cours)"
                maps[key] = {
                    "number": key,
                    "filename": filename,
                    "name_to_print": name_to_print,
                    "en_cours": en_cours
                }
                print("{0} - {1}".format(key+1, name_to_print))
                en_cours = False
                i += 1
            return maps
        else:
            print(
                "\nAucune carte trouvée : veuillez ajouter une carte au " \
                "format .txt dans votre dossier 'cartes'.\n"
                )

    else:
        print("\nErreur : votre projet doit contenir un dossier 'cartes'.\n")


def chose_map(maps):
    """
    Fonction qui retourne les informations de la carte
    sélectionnée par l'utilisateur sous la forme d'un dictionnaire
    map_selected, par ex. :

    map_selected = {
        "number": 1,
        "filename": 'facile',
        "name_to_print": 'Facile (partie en cours)',
        "en_cours": True
    }
    """

    map_selected = {}
    user_input = input(
        "\nEntrez un numéro de labyrinthe pour commencer à jouer (ou Q pour quitter) : ")

    if user_input in ["Q", "q"]:
        print("Vous nous quittez déjà ? A bientôt...\n")
        exit()

    try:
        user_input = int(user_input)
    except ValueError:
        print("Erreur : vous devez entrer un entier !\n")
        # On réaffiche les maps et on demande à nouveau
        # à l'utilisateur d'entrer un numéro de labyrinthe
        maps = get_maps()
        return chose_map(maps)

    if user_input > len(maps) or user_input <= 0:
        print("Saisie incorrecte : veuillez choisir une carte existante.\n")
        # On réaffiche les maps et on demande à nouveau
        # à l'utilisateur d'entrer un numéro de labyrinthe
        maps = get_maps()
        return chose_map(maps)

    map_selected["number"] = user_input
    map_selected["filename"] = maps[user_input-1]["filename"]
    map_selected["name_to_print"] = maps[user_input-1]["name_to_print"]
    map_selected["en_cours"] = maps[user_input-1]["en_cours"]

    print("Vous avez sélectionné la carte : {} - {}".format(
        map_selected["number"], map_selected["name_to_print"]))
    return map_selected


def get_string_map(map_selected):
    """
    Fonction qui retourne la chaîne de caractères correspondant
    à une carte en récupérant le contenu d'un fichier.
    """

    with open("cartes/" + map_selected["filename"], "r") as fichier:
        string_map = fichier.read()

    return string_map


def check_user_input(input_user):
    """
    Fonction qui vérifie la commande entrée par l'utilisateur.
    On regarde d'abord la première lettre (qui désigne la commande), puis
    si celle-ci est reconnue on regarde si celle-ci est suivie d'un nombre
    ou d'une lettre.

    La fonction retourne le dictionnaire suivant :
    {
        "check": check,
        "nature": nature,
        "sens": sens,
        "nb_cases": nb_cases,
        "erreur": erreur
    }
    """

    check = False
    nature = ""
    sens = ""
    nb_cases = 0
    erreur = ""
    erreur_help = "(Tapez help pour afficher l'aide, ou lab pour " \
        "afficher le labyrinthe)\n"

    if len(input_user) == 0:
        erreur = "Erreur : merci d'entrer une commande " \
            "valide :)\n" + erreur_help
    else:
        nature = input_user[0].upper()
        # Commande "M" (murer une porte)
        if nature == "M":
            # Il faut une seule lettre de direction derrière une commande
            # de type "M"
            if len(input_user) != 2:
                erreur = "Erreur : vous devez préciser une " \
                    "direction pour murer une porte !\n" + erreur_help
            else:
                if input_user[1].upper() not in ["N", "E", "S", "O"]:
                    erreur = "Erreur : saisie de la direction incorrecte " \
                        "(N, E, S ou O obligatoire) !\n" + erreur_help
                else:
                    sens = input_user[1].upper()
                    check = True
        # Commande "P" (percer un mur)
        if nature == "P":
            # Il faut une seule lettre de direction derrière une commande
            # de type "P"
            if len(input_user) != 2:
                erreur = "Erreur : vous devez préciser une " \
                    "direction pour percer un mur !\n" + erreur_help
            else:
                if input_user[1].upper() not in ["N", "E", "S", "O"]:
                    erreur = "Erreur : saisie de la direction incorrecte " \
                        "(N, E, S ou O obligatoire) !\n" + erreur_help
                else:
                    sens = input_user[1].upper()
                    check = True
        # Commande "NESO" (déplacement)
        elif nature in ["N", "E", "S", "O"]:
            # S'il n'y aucun caractère derrière la direction, le joueur
            # souhaite se déplacer d'une seule case
            if len(input_user) == 1:
                sens = nature
                nb_cases = 1
                check = True
            # Sinon on regarde si ce ou ces caractères sont bien des entiers
            else:
                nb_cases = input_user[1:]
                try:
                    nb_cases = int(nb_cases)
                except ValueError:
                    erreur = "Erreur : vous devez entrer un nombre " \
                        "entier derrière votre direction !\n" + erreur_help

            if type(nb_cases) is int:
                # On vérifie que l'utilisateur n'a pas entré un nombre
                # inférieur ou égal à 0
                if nb_cases <= 0:
                    erreur = "Erreur : vous devez entrer un " \
                        "nombre entier strictement positif derrière " \
                        "votre direction !\n" + erreur_help
                else:
                    sens = nature
                    check = True
        else:
            erreur = "Erreur : saisie de la commande " \
                "incorrecte.\n" + erreur_help

    return {
        "check": check,
        "nature": nature,
        "sens": sens,
        "nb_cases": nb_cases,
        "erreur": erreur}
