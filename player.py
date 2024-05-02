# Description: Ce fichier contient la classe Player qui permet de créer un joueur

# ------------------- Imports ------------------- #
import _variables as v
import requests
import lxml
from bs4 import BeautifulSoup
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import StaleElementReferenceException


# --------------- Player Class ------------------ #
class Player:

    # Constructeur
    def __init__(self, name, gametag, server):
        self.name = name
        self.gametag = gametag
        self.server = server.lower()
        self.code_error = 0
        self.links = {
            "op.gg": f"https://op.gg/summoners/{self.server}/{self.name}-{self.gametag}",
            "blitz": f"https://blitz.gg/lol/profile/{self.server}1/{self.name}-{self.gametag}",
            "tracker.gg": f"https://tracker.gg/lol/profile/riot/{self.server}/{self.name}%23{self.gametag}",
            "leagueofgraphs": f"https://www.leagueofgraphs.com/summoner/{self.server}/{self.name}-{self.gametag}"
        }
        self.matches = []

    # Méthode pour afficher le joueur
    def __str__(self):
        return f"{self.name}#{self.gametag}"


    # Méthode pour actualiser les codes d'erreurs
    def update_error_code(self, code):

        # serveur invalide
        if self.server not in v.possible_servers:
            self.code_error = 1

        # joueur invalide
        if not self.is_player_valid():
            self.code_error = 2

    # Méthode pour vérifier si le joueur est valide
    def is_player_valid(self):

        # url de la page
        source = requests.get(self.links["op.gg"]).text
        page = BeautifulSoup(source, "lxml")

        # on cherche dans tous les h2 si on trouve "not registered"
        all_h2 = page.find_all("h2")
        for h2 in all_h2:
            if "not registered" in h2.text:
                return False

        return True

    # Méthode pour récupérer un match id
    def get_match_id(self, nb_games=5, wait_delay=1, debug=False):

        """
        Dans cette méthode une erreur courante est l'erreur de type StaleElementReferenceException
        qui se produit lorsque l'élément que vous essayez d'interagir n'est plus attaché à la page.
        Pour éviter cette erreur, on utilise un cache pour stocker les éléments et on les rafraîchit
        si l'exception est levée.
        """

        print(nb_games)

        # options pour le driver
        edge_options = Options()
        edge_options.add_argument("--headless")

        # on crée le driver
        driver = webdriver.Edge(options=edge_options)

        # on va sur la page et on attend le chargement
        driver.get(self.links["blitz"])
        driver.implicitly_wait(wait_delay)

        # initialisation du cache
        cached_elements = {}

        # tentatives pour récupérer les ID des matchs
        match_ids = []
        try:
            # on récupère tous les liens
            all_a = driver.find_elements(By.TAG_NAME, "a")
            cpt = 0
            for a in all_a:
                href = a.get_attribute("href")
                if href and f"https://blitz.gg/lol/match/{self.server}1/" in href:
                    match_id = href[len(f"https://blitz.gg/lol/match/{self.server}1/{self.name}-{self.gametag}/"):]
                    match_ids.append(match_id)
                    cpt += 1
                    if cpt == nb_games:
                        break
        except StaleElementReferenceException:
            # Gestion de l'exception de référence d'élément obsolète
            # Rafraîchissement des éléments du cache
            all_a = driver.find_elements(By.TAG_NAME, "a")
            cached_elements["all_a"] = all_a
            for a in all_a:
                href = a.get_attribute("href")
                if href and f"https://blitz.gg/lol/match/{self.server}1/" in href:
                    match_id = href[len(f"https://blitz.gg/lol/match/{self.server}1/{self.name}-{self.gametag}/"):]
                    match_ids.append(match_id)
                    cpt += 1
                    if cpt == nb_games:
                        break

        if debug:
            print(match_ids)

        # on stocke les matchs
        self.matches = match_ids

        # on ferme le driver
        driver.quit()

        return match_ids