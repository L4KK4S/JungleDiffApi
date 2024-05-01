# Description: Ce fichier contient les scripts de test du projet

import player
import game

if __name__ == "__main__" :

    # player = player.Player("L4KK4S", "EFREI", "euw")
    # player.get_match_id(debug=True)

    game = game.Game("euw", "6681846948")
    print(game)