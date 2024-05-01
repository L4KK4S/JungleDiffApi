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

    # On renvoie les erreurs
    match player.code_error:
        case 1:
            return jsonify({'error': 'Invalid server. Please use one of the following: euw, na, eune, br, kr, lan, las, oce, ru, tr'})
        case 2:
            return jsonify({'error': 'Invalid player. Please check the name and the gametag.'})
        case _:
            pass

    # Résultat
    result = {
        'name': player.name,
        'gametag': player.gametag,
        'server': player.server,
        'links': player.links
    }

    # Renvoyer le résultat
    return jsonify({'result': result})

if __name__ == '__main__':
   app.run(debug=False, host="0.0.0.0")
