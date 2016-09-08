# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Fonctions utilisées dans le jeu du labyrinthe.

Auteur  : Nicolas MURA
Date    : 02/09/2016
Version : 1.0
"""
import os
import glob
import pickle
import copy
import re


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
                # Si on détecte qu'une partie est en cours (ie qu'un fichier
                # <carte>_save existe), on le spécifie
                if os.path.isfile("cartes/sauvegardes/" + filename):
                    en_cours = True
                    name_to_print += " (en cours)"
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
        "name": 'facile',
        "en_cours": True
    }
    """

    map_selected = {}
    number_selected = input(
        "\nEntrez un numéro de labyrinthe pour commencer à jouer : ")
    try:
        number_selected = int(number_selected)
    except ValueError:
        print("Erreur : vous devez entrer un entier !\n")
        # On réaffiche les maps et on demande à nouveau
        # à l'utilisateur d'entrer un numéro de labyrinthe
        maps = get_maps()
        return chose_map(maps)

    if number_selected > len(maps) or number_selected <= 0:
        print("Saisie incorrecte : veuillez choisir une carte existante.\n")
        # On réaffiche les maps et on demande à nouveau
        # à l'utilisateur d'entrer un numéro de labyrinthe
        maps = get_maps()
        return chose_map(maps)

    map_selected["number"] = number_selected
    map_selected["filename"] = maps[number_selected-1]["filename"]
    map_selected["name_to_print"] = maps[number_selected-1]["name_to_print"]
    map_selected["en_cours"] = maps[number_selected-1]["en_cours"]

    print("Vous avez sélectionné la carte : {} - {}".format(
        map_selected["number"], map_selected["name_to_print"]))
    return map_selected


def get_string_map(map_selected, reprendre_partie):
    """
    Fonction qui retourne 2 chaînes de caractères correspondant
    à une carte en récupérant le contenu d'un fichier.
    A la demande de l'utilisateur, on récupère :

    - Soit une partie sauvegardée :
      -> string_map_initiale = contenu du fichier <carte_filename>.txt
      -> string_map_saved    = contenu du fichier sauvegardes/<carte_filename>_save

    - Soit une partie à jouer depuis le début
      -> string_map_initiale = contenu du fichier <carte_filename>.txt
      -> string_map_saved    = copie de la chaine string_map_initiale
    """

    if reprendre_partie is True:
        print("OK, reprise de la partie sauvegardée !")
        with open("cartes/" + map_selected["filename"], "r") as fichier:
            string_map_initiale = fichier.read()
        with open("cartes/sauvegardes/" + map_selected["filename"], "rb") as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            string_map_saved = mon_depickler.load()
    else:
        print("OK, reprise de la partie depuis le début !")
        with open("cartes/" + map_selected["filename"], "r") as fichier:
            string_map_initiale = fichier.read()
        string_map_saved = copy.deepcopy(string_map_initiale)

    return string_map_saved, string_map_initiale


def check_user_input(input_user):
    """
    Fonction qui vérifie le déplacement demandé par l'utilisateur.
    On regarde d'abord la première lettre (qui désigne la direction), puis
    si celle-ci est reconnue on regarde si celle-ci est suivie d'un nombre.

    La fonction retourne le dictionnaire suivant :
    {
        "check": check,
        "sens": sens,
        "nb_cases": nb_cases
    }
    """

    check = False
    sens = ""
    nb_cases = 0

    if len(input_user) == 0:
        print("Erreur : merci d'entrer une direction :)\n")

    else:
        sens = input_user[0]
        if sens not in ["N", "E", "S", "O", "n", "e", "s", "o"]:
            print("Saisie de la direction incorrecte (N, E, S ou O obligatoire).\n")
        else:
            # S'il n'y aucun caractère derrière la direction, le joueur
            # souhaite se déplacer d'une seule case
            if len(input_user) == 1:
                nb_cases = 1
                check = True
            # Sinon on regarde si ce ou ces caractères sont bien des entiers
            else:
                nb_cases = input_user[1:]
                try:
                    nb_cases = int(nb_cases)
                except ValueError:
                    print("Erreur : vous devez entrer un nombre " \
                        "entier derrière votre direction !\n")

            if type(nb_cases) is int:
                # On vérifie que l'utilisateur n'a pas entré un nombre
                # inférieur ou égal à 0
                if nb_cases <= 0:
                    print("Erreur : vous devez entrer un nombre entier " \
                        "strictement positif derrière votre direction !\n")
                else:
                    check = True

    return {"check": check, "sens": sens, "nb_cases": nb_cases}
