from flask import Blueprint, jsonify, request
from api.routes.helper import get_states, get_value_function, greedyMove
from api.routes.trainRL import trainRL

mod = Blueprint('main', __name__)

@mod.route('/', methods=['GET'])
def index():
    return 'Done', 201

@mod.route('/next_move', methods=['POST'])
def next_move():
    req = request.get_json()
    states = get_states("/temp/States.pickle")
    V = get_value_function("/temp/ValueFunction.pickle")
    board = req['board']
    nm, _ = greedyMove(board, states, V)
    return jsonify({'next_move': nm}), 200

@mod.route('/train', methods=['POST'])
def train():
    req = request.get_json()
    trainRL(req['alpha'], req['episodes'])
    return 'Done', 201