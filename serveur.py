# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 4
Mainfile côté serveur - Pour lancer le serveur, exécutez sur votre machine :
> python3 serveur.py (Mac OS X)
> py -3 serveur.py (Windows)

Note : le serveur doit être exécuté sur une seule machines connectée
au même réseau que le (ou les) client(s) - voir module setup.py.

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 1.0
"""

from threading import Thread
from os import system as os_system, name as os_name
import socket
import select

import setup
import global_variables_server
from functions import *
from classes import *
from serveur_threads import ThreadClient


if os_name == "nt":  # Cas Windows
    os_system("cls")
else:
    os_system("clear")

HOST = setup.HOST
PORT = setup.PORT
# Nombres de connexions simultanées que le serveur peut recevoir
# sans les accepter (en général 5)
NB_CONNECTIONS_MAX = setup.NB_CONNECTIONS_MAX

print("\nBienvenu(e) dans le jeu du labyrinthe !\n")

# Récupération et affichage du nom des cartes existantes,
# ou affichage d'un message approprié si aucune carte trouvée
maps = get_maps()
if maps is None:
    raise TypeError("Erreur : votre projet doit contenir un dossier 'cartes' avec au moins une carte valide.")

# Sélection et récupération d'une carte par l'utilisateur
map_selected = chose_map(maps)

# Récupération de la carte sélectionnée et d'une éventuelle sauvegarde
# sous forme de chaîne de caractères
string_map = get_string_map(
    map_selected)

# Création d'un objet carte
carte = Carte(
    map_selected["number"],
    map_selected["filename"],
    map_selected["name_to_print"],
    string_map
)

# Récupération du labyrinthe et du robot
labyrinth = carte.labyrinth
robot = carte.labyrinth.robot

# Affichage de la carte
print("\n" + carte.string + "\n")
global_variables_server.carte = carte
global_variables_server.labyrinth = labyrinth
global_variables_server.robot = robot

""" Initialisation du serveur - Mise en place du socket """

# Construction du socket
# - socket.AF_INET : la famille d'adresses, ici ce sont des adresses Internet
# - socket.SOCK_STREAM : le type du socket, SOCK_STREAM pour le protocole TCP.
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
liaisonOK = False
# print(PORT)
# Connexion du socket avec la méthode bind qui prend en paramètre le tuple (nom_hote, port)
# Si le port choisi est occupé, on tente avec le port suivant
try:
    mySocket.bind((HOST, PORT))
    liaisonOK = True
except socket.error:
    print("Erreur : la liaison du socket à l'adresse choisie a échoué.")
if liaisonOK is False:
    print("Nouvelle tentative en cours...")
    PORT += 1
    # print(PORT)
    try:
        mySocket.bind((HOST, PORT))
    except socket.error:
        print("Erreur : la liaison du socket à l'adresse choisie a échoué.")
        exit()
print("Serveur prêt, en attente de requêtes de connexions clientes...")
# On fait écouter le socket sur le port précédemment spécifié
mySocket.listen(NB_CONNECTIONS_MAX)


""" Lancement du serveur et récupération des connexions clientes """

# Attente et prise en charge des connexions demandées par les clientes
# global saved_connections
global_variables_server.saved_connections = {}  # Dictionnaire des connexions clients
global_variables_server.saved_threads = {}  # Dictionnaire des connexions clients
# saved_connections_objets = []  # Dictionnaire des objets connexions clients
# conn_threads_objets = []  # Dictionnaire des objets connexions clients
"""
Note : on place les connexions clients dans un dictionnaire plutôt que dans une
liste car on doit pouvoir ajouter ou enlever des références dans n'importe quel
ordre, de plus on dispose ainsi d'un identifiant unique pour chaque connexion
(fourni par la classe Thread(), lequel servira de clé d'accès dans le
dictionnaire.
"""
# La boucle de répétition attend constamment l'arrivée de nouvelles connexions.
# Pour chacune d'entre elles, un nouvel objet ThreadClient() est créé, lequel
# pourra s'occuper d'elle indépendamment de toutes les autres.
connected_clients = []
global_variables_server.play = False
global_variables_server.accept_new_client = True
# serveur_lance = th_serveur_E.serveur_lance

while 1:

    connection, adresse = mySocket.accept()

    if not global_variables_server.play:
        # saved_connections_objets.append(connection)
        # Création d'un nouvel objet thread pour gérer la connexion
        th_client = ThreadClient(connection)
        # conn_threads_objets.append(th_client)
        th_client.start()
        # On mémorise la connexion dans le Dictionnaire
        identifiant = th_client.getName()  # Identifiant du thread
        global_variables_server.saved_connections[identifiant] = connection
        global_variables_server.saved_threads[identifiant] = th_client
        print("Connexion acceptée, client {} connecté, adresse IP {}, port {}.".format(identifiant, adresse[0], adresse[1]))

        # Dialogue avec le client
        msgServeur_bienvenue = "Bienvenue, joueur " + identifiant + ".\n\n" + global_variables_server.carte.string + "\n\nEntrez C pour commencer la partie.\n"
        msgServeurBroadcast_bienvenue = "'{} a rejoint le jeu du labyrinthe.'".format(identifiant)
        # On informe les autres clients
        for cle in global_variables_server.saved_connections:
            if cle == identifiant:  # On ne le renvoie pas à l'émetteur
                connection.send(msgServeur_bienvenue.encode("utf-8"))
            else:
                global_variables_server.saved_connections[cle].send(msgServeurBroadcast_bienvenue.encode("utf-8"))
    else:
        # La partie est déjà commencée, on refuse le nouveau client
        print("Connection refusée.")
        msgServeur = "FULL"
        connection.send(msgServeur.encode("utf-8"))
    # print("Connexions enregistrées : ", global_variables_server.saved_connections)
