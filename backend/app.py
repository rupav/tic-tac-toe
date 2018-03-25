#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import pickle
from numpy import random
from firebase import firebase               #stored value function on firebase

def firebase_helper(indices):
    firebase = firebase.FirebaseApplication('https://rupav-firebase-data.firebaseio.com', None)
    result = firebase.get('rupav-firebase-data', None)
    value_functions_list = []
    for idx in range(indices):
        value_functions_list.append(result['-L0_e_TKRgJhxq4PVmbo'][idx])

    return value_functions_list #return all new possible states' value function


V = []
states = []
totalStates = 0
alpha = 0.9

board = [0]*9
tiles = [0,1,2]
players = [1,2]

# load the data which contains the states of the game.
with open('States.pickle',"rb") as fo:
	states = pickle.load(fo)

def updateEstimateValueOfS(s,sPrime):
	V[s] = V[s] + alpha*(V[sPrime] - V[s])

def getListOfBlankTiles(board):
	blankTiles = []
	for i in range(len(board)):
		if board[i] == 0:
			blankTiles.append(i)
	return blankTiles

def isWinner(board):
	for player in players:
		tile = tiles[player]

		for i in range(3):
			i *= 3
			#horizontal
			if (board[i] == tile) and\
			   (board[i+1] == tile) and\
			   (board[i+2] == tile) :
				return 1

		for i in range(3):
			#vertical
			if (board[i] == tile) and\
			   (board[i+3] == tile) and\
			   (board[i+6] == tile) :
			   return 1

        #major/principal diagonal
		if (board[0]==tile) and\
		   (board[4] == tile) and\
		   (board[8] == tile) :
		   return 1
        #minor/secondary diagonal
		if (board[2]==tile) and\
		   (board[4] == tile) and\
		   (board[6] == tile) :
		   return 1

	#no winner found if we are here!
	#check if there is atleast 1 blank tile for nextMove!
	if getListOfBlankTiles(board) is not []:
		return 0

	return -1                #for draw!... np more move is possible

def determineValue(board, player):
	result = isWinner(board)

	if result == 1:                   # someone won the game:
		if player == 1:
			return 1.0
		else:
			return 0.0
	if result == -1:                  # draw case
		return 0.0
	else:
		return 0.5

def greedyMove(board):
	maxValue = 0
	maxIndex = 0
	possibleTiles = getListOfBlankTiles()  # returns a list, max length = 9 (all are empty)
    #put 1 in those possible tiles to find possible states
    possibleStates = []
    for tile in possibleTiles:
        board[tile] = 1
        possibleStates.append(board)
        board[tile] = 0

    valueFunctions_possibleStates = firebase_helper(possibleStates)

    #find max value in the valueFunction list for greedy move!
    maxV = max(valueFunctions_possibleStates)
    maxIndex = index(maxV)

    nextMove = possibleTiles[maxIndex]
    return nextMove, maxIndex

    '''

    nextMove = possibleMoves.pop()      #here we assumed any 1 move from all possible moves!
	board[nextMove] = 1
	maxIndex = states.index(board)      #for current board setting
	maxValue = V[maxIndex]
	board[nextMove] = 0                 #setting again to zero until we find the real one!

	for i in range(len(possibleMoves)):
		board[i] = 1
		idx = states.index(board)
		val = V[idx]

		if(val>maxValue):
			maxValue = val
			maxIndex = idx
			nextMove = i
		board[i] = 0                    #so that for next iteration, this remains a un-filled place


	return nextMove, maxIndex
    '''


@app.route('tic-tac-toe-api/v1.0/state', methods=['GET'])
def post_state():


# called from client when computer can play the next move
@app.route('tic-tac-toe-api/v1.0/state', methods=['POST'])
def fetch_state():
    # we receive state/board and computer has to play the next move
    current_state = request.json['state']
    if random.randint(1,11) in [1,2]:
        tiles = getListOfBlankTiles(current_state)
        randomTile = tiles[random.randint(0,len(tiles))]

    else:
        nextMove, maxIndex = greedyMove(current_state)



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug = True)
