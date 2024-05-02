from flask import Flask, request, jsonify
from player import Player

app = Flask(__name__)

@app.route('/player/links', methods=['GET'])
def player_links():

    # Récupérer les paramètres
    server = request.args.get('server')
    name = request.args.get('name')
    gametag = request.args.get('gametag')

    # Créer le joueur
    if gametag is None:
        gametag = server
    player = Player(name, gametag, server)

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

@app.route('/game/id', methods=['GET'])
def game_id():

    # Récupérer les paramètres
    server = request.args.get('server')
    name = request.args.get('name')
    gametag = request.args.get('gametag')
    nb_games = int(request.args.get('nb_games'))


    # Créer le joueur
    if gametag is None:
        gametag = server
    player = Player(name, gametag, server)

    # Actualiser le code d'erreur
    player.update_error_code(player)

    # Renvoyer les erreurs
    match player.code_error:
        case 1:
            return jsonify({'error': 'Invalid server. Please use one of the following: euw, na, eune, br, kr, lan, las, oce, ru, tr'})
        case 2:
            return jsonify({'error': 'Invalid player. Please check the name and the gametag.'})
        case _:
            pass

    # Résultat
    result = {
        f'last {nb_games} games id': player.get_match_id(nb_games=nb_games)
    }

    # Renvoyer le résultat
    return jsonify({'result': result})


if __name__ == '__main__':
   app.run(debug=False, host="0.0.0.0")
