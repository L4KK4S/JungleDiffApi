# Description: This file contains the Player class which is used to store the player's information.

# ------------------- Imports ------------------- #
import requests
import lxml
from bs4 import BeautifulSoup


# --------------- Variables --------------------- #
possible_servers = ['euw', 'na', 'eune', 'br', 'kr', 'lan', 'las', 'oce', 'ru', 'tr']


# --------------- Player Class ------------------ #
class Player:

    # Constructeur
    def __init__(self, name, gametag, server):
        self.name = name
        self.gametag = gametag
        self.server = server.lower()
        self.code_error = 0
        self.opgg_link = f"https://op.gg/summoners/{self.server}/{self.name}-{self.gametag}"

    # Méthode pour afficher le joueur
    def __str__(self):
        return f"{self.name}#{self.gametag}"

    # Méthode pour actualiser les codes d'erreurs
    def update_error_code(self, code):

        # serveur invalide
        if self.server not in possible_servers:
            self.code_error = 1

        # joueur invalide
        if not self.is_player_valid():
            self.code_error = 2

    # Méthode pour vérifier si le joueur est valide
    def is_player_valid(self):

        source = requests.get(self.opgg_link).text
        page = BeautifulSoup(source, "lxml")

        all_h2 = page.find_all("h2")
        for h2 in all_h2:
            print(h2.text)
            if "not registered" in h2.text:
                return False

        return True

