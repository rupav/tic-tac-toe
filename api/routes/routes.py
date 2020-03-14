from flask import Blueprint, jsonify, request


mod = Blueprint('main', __name__)

@mod.route('/', methods=['GET'])
def index():
    return 'Done', 201
