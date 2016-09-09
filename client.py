# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Mainfile côté client - Pour lancer le client, exécutez :
> python3 client.py sous OS X
> py -3 client.py sous Windows

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 2.0
"""

import setup
import socket
import os
import setup

if os.name == "nt":  # Cas Windows
    os.system('cls')
else:
    os.system("clear")


hote = setup.CLIENT_HOST
port = setup.PORT

print("Tentative de connexion avec le serveur du jeu Labyrinthe en cours...\n")
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion_avec_serveur.connect((hote, port))
except:
    raise ConnectionRefusedError("Vous devez d'abord lancer le serveur !")

print("Connexion établie avec le serveur du jeu Labyrinthe !")

# A ce stade, le serveur doit normalement envoyer un message de bienvenue
msg_recu = connexion_avec_serveur.recv(1024)
print(msg_recu.decode())

msg_a_envoyer = b""
while msg_a_envoyer != b"fin":
    msg_a_envoyer = input("> ")
    # Peut planter si vous tapez des caractères spéciaux
    msg_a_envoyer = msg_a_envoyer.encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)
    msg_recu = connexion_avec_serveur.recv(1024)
    print(msg_recu.decode())  # Là encore, peut planter s'il y a des accents

print("Fermeture de la connexion")
connexion_avec_serveur.close()
