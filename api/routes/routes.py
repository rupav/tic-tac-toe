from flask import Blueprint, jsonify, request
from api.routes.helper import get_states, get_value_function, greedyMove

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
