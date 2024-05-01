# Description: Ce fichier contient la classe Game qui permet d'avoir des informations sur une game

# ------------------- Imports ------------------- #
import requests
import lxml
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import StaleElementReferenceException

# --------------- Game Class ------------------ #
class Game:

    # Constructeur
    def __init__(self, server, gameid):
        self.server = server.lower()
        self.gameid = gameid
        self.code_error = 0
        self.links = {
            "leagueofgraphs": f"https://www.leagueofgraphs.com/match/{self.server}/{self.gameid}",
            "tracker.gg": f"https://tracker.gg/lol/match/{self.server}/{self.gameid}",
        }
        self.players = self.get_players()


    # Méthode pour afficher le match
    def __str__(self):
        return f"Game {self.gameid} on {self.server}\nPlayers: {self.players}"

    # Méthode pour actualiser les codes d'erreurs
    def update_error_code(self, code):

        # serveur invalide
        if self.server not in v.possible_servers:
            self.code_error = 1

        # game invalide
        if not self.is_game_valid():
            self.code_error = 2


    # Méthode pour obtenir les joueurs de la game
    def get_players(self):

        # options pour le driver
        edge_options = Options()
        edge_options.add_argument("--headless")

        # on crée le driver
        driver = webdriver.Edge(options=edge_options)

        # on va sur la page
        driver.get(self.links["leagueofgraphs"])

        # on récupère les noms des joueurs
        all_players = []
        all_names = driver.find_elements(By.CLASS_NAME, "name")
        for player in all_names:
            if player.text != "":
                all_players.append(player.text)

        # on ferme le driver
        driver.quit()

        return all_players

    # Méthode pour vérifier si la game est valide
    def is_game_valid(self):

        # à compléter

        return True