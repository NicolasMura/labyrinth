# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 4
Classes.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 1.0
"""

import global_variables_client
import sys
from threading import Thread, RLock

verrou = RLock()


class ThreadReception(Thread):
    """Objet Thread gérant la réception des messages"""

    def __init__(self, conn):
        Thread.__init__(self)
        self.connection = conn  # Référence du socket de connexion
        self.active = False

    def run(self):
        # Boucle de réception des messages : à chaque itération, le flux
        # d'instructions s'interrompt sur self.connection.recv, dans l'attente
        # d'un nouveau message - mais le reste du programme n'est pas figé
        # (les autres threads continuent leur travail indépendamment)

        identifiant = self.getName()  # Chaque thread possède un nom
        i = 0
        while 1:
            # print("Actif ? ", self.active)
            message_recu = self.connection.recv(1024).decode("utf-8")
            # On met un verrou car sinon on peut recevoir en même temps
            # les messages "C" et "PLAY" / "STOP"
            with verrou:
                # print("Message reçu n°{} :".format(i+1))
                print(message_recu)
                # print("*" + message_recu + "*")
                i += 1
                if message_recu == "PLAY":
                    self.active = True
                else:
                    self.active = False

        # print("Un joueur a entré la commande C.")

        # while 1:
            # message_recu = self.connection.recv(1024).decode("utf-8")
            # print("*" + message_recu + "*")
            # print("type(message_reçu) : ", type(message_recu))

            # if message_recu == identifiant:
            #     print("OK")
            # else:
            #     print("NOK")

        # Le thread <réception> se termine ici.
        # print("Le thread réception s'est terminé correctement.")
        print("Taper Enter pour quitter.")
        # On force la fermeture du thread <émission>
        global_variables_client.th_E.stop()
        self.connection.close()


class ThreadEmission(Thread):
    """Objet Thread gérant l'émission des messages"""

    def __init__(self, conn):
        Thread.__init__(self)
        self.connection = conn  # Référence du socket de connexion
        self.terminated = False

    def run(self):
        # Boucle d'envoi des messages : à chaque itération, le flux
        # d'instructions s'interrompt sur input("C> "), dans l'attente
        # d'une entrée clavier - mais le reste du programme n'est pas figé
        # (les autres threads continuent leur travail indépendamment)
        while 1:
            message_emis = input("C> ")
            if self.terminated:
                break
            self.connection.send(message_emis.encode("utf-8"))

        # Le thread <émission> se termine ici.
        # print("Le thread émission s'est terminé correctement.")
        # print("Client arrêté (Thread Emission). Connexion interrompue.")
        # sys.exit()

    def stop(self):
        self.terminated = True
