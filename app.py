from flask import Flask, request, jsonify
from player import Player

app = Flask(__name__)

# Créer un joueur
def create_player(server, name, gametag=None):
    if gametag is None:
        gametag = server
    return Player(name, gametag, server)

@app.route('/api', methods=['GET'])
def api():

    # Créer un joueur
    server = request.args.get('server')
    name = request.args.get('name')
    gametag = request.args.get('gametag')
    player = create_player(server, name, gametag)

    # On actualise le code d'erreur
    player.update_error_code(player)

    # Si le serveur n'est pas valide
    if player.code_error == 1:
        return jsonify({'error': 'Invalid server. Please use one of the following: euw, na, eune, br, kr, lan, las, oce, ru, tr'})

    # Si le joueur n'est pas valide
    if player.code_error == 2:
        return jsonify({'error': 'Invalid player. Please check the name and the gametag.'})

    # Résultat
    result = {
        'name': player.name,
        'gametag': player.gametag,
        'server': player.server,
        'opgg_link': player.opgg_link
    }

    # Renvoyer le résultat
    return jsonify({'result': result})

if __name__ == '__main__':
   app.run(debug=False, host="0.0.0.0")
