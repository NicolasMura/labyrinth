# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 4
Classes.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 1.0
"""

import global_variables_server
import sys
from threading import Thread, RLock

from functions import *
from classes import *

verrou = RLock()


class ThreadClient(Thread):
    """Dérivation d'un objet thread pour gérer la connexion avec un client"""

    def __init__(self, conn):
        Thread.__init__(self)
        self.connection = conn
        self.active = False  # Passe à True une fois la partie commencée et que c'est au tour de ce Thread

    def run(self):
        """ L'utilité de ce thread est de réceptionner tous les messages provenant
        d'un client particulier. Il faut donc pour cela :
        - une 1ère boucle de
        répétition perpétuelle, qui ne s'interrompt qu'à la réception
        du message "C".
        - ... TBD
        """

        # Dialogue avec le client
        identifiant = self.getName()  # Chaque thread possède un nom
        while 1:
            # print("Thread {} actif ? {}".format(identifiant, self.active))
            msgClient = self.receive_message()
            message = "{}> {}".format(identifiant, msgClient)
            print(message)

            # Si la partie n'a pas encore commencé
            if not global_variables_server.play:
                # Un client entre la touche C
                nb_joueurs = len(global_variables_server.saved_connections)
                if msgClient.upper() == "C":
                    self.active = True
                    # Envoi de la carte à celui qui commence
                    if nb_joueurs > 1:
                        self.send_message_to_client("A vous l'honneur !")
                    else:
                        self.send_message_to_client("Vous jouez en solo !")
                    self.send_broadcast_message_to_other_clients("STOP")
                    self.send_message_to_client("PLAY")
                    if nb_joueurs > 1:
                        broadcast_message = "C'est à {} de commencer".format(identifiant)
                        self.send_broadcast_message_to_other_clients(broadcast_message)
                    # self.send_message_to_client("\n" + global_variables_server.carte.string + "\n")
                    self.send_message_to_client("\nEntrez votre commande :\n> ")
                    global_variables_server.play = True

                    # Début de la partie
                    print("Le joueur {} commence la partie.".format(identifiant))
                    global_variables_server.liste_joueurs = []  # Liste ordonnées des joueurs
                    # On place le joueur qui commence en première position
                    global_variables_server.liste_joueurs = [identifiant]
                    # Puis on place les autres joueurs à la suite
                    for joueur in global_variables_server.saved_connections:
                        if joueur != identifiant:
                            global_variables_server.liste_joueurs.append(joueur)
                    # print("Liste des joueurs :", global_variables_server.liste_joueurs)
                    global_variables_server.i = 0
                    continue
                else:
                    self.send_message_to_client("Commande incorrecte : vous devez entrer C pour commencer la partie.")

            # Si la partie a commencé
            if global_variables_server.play:
                if self.active:
                    deplacement = check_user_input(msgClient)
                    if msgClient == "help":
                        print("L'utilisateur demande de l'aide")
                        help_content = global_variables_server.labyrinth.get_help()
                        self.send_message_to_client(help_content)
                    elif msgClient == "lab":
                        print("L'utilisateur demande l'affichage de la carte")
                        self.send_message_to_client("\n" + global_variables_server.carte.string + "\n")
                    elif deplacement["check"]:
                        print("Commande acceptée")
                        # TO DO...
                        self.send_message_to_client("\n\n" + global_variables_server.carte.string + "\n")
                        # TO DO...

                        # Le thread actif passe au statut inactif
                        self.active = False
                        self.send_message_to_client("STOP")
                        global_variables_server.i += 1
                        # Si on arrive au bout de la liste des joueurs, on
                        # réinitisalise l'indice de parcours
                        if global_variables_server.i == len(global_variables_server.liste_joueurs):
                            global_variables_server.i = 0
                        print("Prochain joueur : ", global_variables_server.liste_joueurs[global_variables_server.i])
                        next_player = global_variables_server.liste_joueurs[global_variables_server.i]
                        if nb_joueurs > 1:
                            self.send_message_to_client("\nDéplacement OK, c'est au tour de {} .".format(next_player))
                        else:
                            self.send_message_to_client("\nDéplacement OK")
                        # Le prochain thread (actif) passe au statut actif
                        global_variables_server.saved_threads[next_player].active = True
                        self.send_message_to_other_client("PLAY", next_player)
                        if nb_joueurs > 1:
                            self.send_message_to_other_client("\nC'est à vous !\n\n" + global_variables_server.carte.string + "\n\nEntrez votre commande :\n> ", next_player)
                    else:
                        message = "{}> Commande incorrecte".format(identifiant)
                        print(message)
                        erreur = deplacement["erreur"]
                        self.send_message_to_client(erreur)

                else:
                    self.send_message_to_client("Attendez patiemment votre tour...")

            # S'il n'y a pas de message, c'est que le client s'est déconnecté
            if not msgClient:
                break

        # Fermeture des connexions
        # On fait suivre le message à tous les autres clients
        msgDeconnection = "\nUn client s'est déconnecté : la partie est bloquée, merci de la recommencer.\n"
        for cle in global_variables_server.saved_connections:
            self.send_broadcast_message_to_other_clients(msgDeconnection)
        self.connection.close()  # On coupe la connexion côté serveur
        del global_variables_server.saved_connections[identifiant]    # On supprime le client dans le dictionnaire
        print("Client '{}' déconnecté.".format(identifiant))
        # Le thread se termine ici

    def send_message_to_client(self, message):
        # Envoi du message au client
        identifiant = self.getName()  # Chaque thread possède un nom
        global_variables_server.saved_connections[identifiant].send(message.encode("utf-8"))

    def send_message_to_other_client(self, message, identifiant):
        # Envoi du message à un autre client
        global_variables_server.saved_connections[identifiant].send(message.encode("utf-8"))

    def send_broadcast_message(self, broadcast_message):
        # On fait suivre le message à tous les clients
        for cle in global_variables_server.saved_connections:
            global_variables_server.saved_connections[cle].send(broadcast_message.encode("utf-8"))

    def send_broadcast_message_to_other_clients(self, message_to_others):
        # On fait suivre le message à tous les autres clients
        identifiant = self.getName()  # Chaque thread possède un nom
        for cle in global_variables_server.saved_connections:
            if cle != identifiant:  # On ne le renvoie pas à l'émetteur
                global_variables_server.saved_connections[cle].send(message_to_others.encode("utf-8"))

    def receive_message(self):
        msgClient = self.connection.recv(1024).decode("utf-8")
        return msgClient

    def receive_message_from_other_client(self, identifiant):
        msgClient = global_variables_server[identifiant].recv(1024).decode("utf-8")
        return msgClient
