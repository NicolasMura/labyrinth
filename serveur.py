# -*- coding: utf-8 -*-

"""
Jeu du Labyrinthe / Exercice tutoriel Python OC, partie 3
Mainfile côté serveur - Pour lancer le serveur, exécutez :
> python3 serveur.py sous OS X
> py -3 serveur.py sous Windows

Auteur  : Nicolas MURA
Date    : 08/09/2016
Version : 2.0
"""

import setup
import os
import socket
import select


if os.name == "nt":  # Cas Windows
    os.system('cls')
else:
    os.system("clear")

hote = ''
port = setup.PORT
# Nombres de connexions simultanées que le serveur peut recevoir
# sans les accepter (en général 5)
nb_connexions_max = setup.NB_CLIENTS_MAX

print("\nBienvenu(e) dans le jeu du labyrinthe !\n")
# Construction du socket
# - socket.AF_INET : la famille d'adresses, ici ce sont des adresses Internet
# - socket.SOCK_STREAM : le type du socket, SOCK_STREAM pour le protocole TCP.
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connexion du socket avec la méthode bind qui prend en paramètre le tuple (nom_hote, port)
connexion_principale.bind((hote, port))
# On fait écouter le socket sur le port précédemment spécifié
connexion_principale.listen(nb_connexions_max)

serveur_lance = True
clients_connectes = []
numero_clients_list = []
print("En attente de la connexion d'un client...")

i = 0
while serveur_lance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    connexions_demandees, wlist, xlist = select.select(
        [connexion_principale], [], [], 0.05)
    if connexions_demandees:
        i += 1

    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(connexion_avec_client)
        # Affichage du dernier client connecté
        print("Client n° {} connecté".format(i))
        # On envoie un message de bienvenue au client
        msg_a_envoyer = "Bienvenue, joueur " + str(i) + "."
        msg_a_envoyer = msg_a_envoyer.encode()
        connexion_avec_client.send(msg_a_envoyer)

    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(
            clients_connectes, [], [], 0.05)
    except select.error:
        print("Aucun client connecté !")
    else:
        # On parcourt la liste des clients à lire
        for client in clients_a_lire:
            # Client est de type socket
            msg_recu = client.recv(1024)
            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode()
            print("Reçu {}".format(msg_recu))
            client.send(b"5 / 5")
            if msg_recu == "fin":
                serveur_lance = False

print("Fermeture des connexions")
for client in clients_connectes:
    client.close()

connexion_principale.close()
