# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 4
Mainfile côté client - Pour lancer le client, exécutez :
> python3 client.py (Mac OS X)
> py -3 client.py (Windows)

Note : le client doit être exécuté sur une (ou plusieurs) machines connectée(s)
au même réseau que le serveur - voir module setup.py.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 1.0
"""

from os import system as os_system, name as os_name
import socket
from sys import exit

import setup
import global_variables_client
from client_threads import ThreadReception, ThreadEmission

if os_name == "nt":  # Cas Windows
    os_system('cls')
else:
    os_system("clear")


HOST = setup.HOST
PORT = setup.PORT

print("Tentative de connexion avec le serveur du jeu Labyrinthe en cours...\n")
connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexionOK = False
# print(PORT)
try:
    connection_with_server.connect((HOST, PORT))
    connexionOK = True
except socket.error:
    print("La connexion a échoué.")
if not connexionOK:
    connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Nouvelle tentative en cours...")
    PORT += 1
    # print(PORT)
    try:
        connection_with_server.connect((HOST, PORT))
    except socket.error:
        print("La connexion a échoué.")
        exit()
print("Connexion établie avec le serveur du jeu Labyrinthe !\n")

# A ce stade, le serveur doit normalement envoyer un message de bienvenue...
msg_recu = connection_with_server.recv(1024).decode("utf-8")
if msg_recu == "FULL":
    print("Désolé, la partie a déjà commencé...")
    print("Veuillez fermer les connexions clientes et redémarrer le serveur.")
    exit()
print(msg_recu)

# # Dialogue avec le serveur : on instancie deux threads enfants pour gérer
# # indépendamment l'émission et la réception des messages
global_variables_client.th_E = ThreadEmission(connection_with_server)
th_R = ThreadReception(connection_with_server)
global_variables_client.th_E.start()
th_R.start()
# global_variables_client.th_E.join()
# global_variables_client.th_R.join()
# exit()
