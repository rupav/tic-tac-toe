import pickle
import os

states = []
V = []
totalStates = 0

board = [0]*9

tiles = [0,1,2]

def abspath(fname):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    return dir_ + fname

def create_all_states(board,player):
	won = hasWinner(board)
	if won == 1 or won == -1:
		return
	for i in range(0,9):
		if board[i] == 0:
			board[i] = player
			if board[:] not in states:
				states.append(board[:])
				V.append(determineValue(board,player))
			create_all_states(board,switchPlayer(player))
			board[i] = 0

def switchPlayer(player):
	if player == 1:
		return 2
	else:
		return 1

def determineValue(_board, player):
  won = hasWinner(_board)
  
  # win
  if 1 == won:
    if 1 == player:
      return 1.0
    else:
      return 0.0
  # draw
  elif -1 == won:
    return 0.0
  else:
    return 0.5

def hasWinner(board):

	for player in range(1,3):
		tile = tiles[player]

		#check Horizontal
		for i in range(0,3):
			i = i*3
			if (board[i] == tile) and \
			   (board[i+1] == tile) and \
			   (board[i+2] == tile):
				return 1
		# check Vertical
		for i in range(0,3):
			if (board[i] == tile) and \
				(board[i+3] == tile) and \
				 (board[i+6] ==tile):
					return 1
		if(board[0] == tile) and \
			(board[4] == tile ) and \
			(board[8] == tile):
			return 1
		if (board[6] == tile) and \
			(board[4] == tile) and \
			(board[2] == tile):
			return 1

	for i in range(0,9):
		if board[i] == 0:
			return 0
		#Draw match
	return -1

def updateBoard(_board, player, index):
  if _board[index] == 0:
    _board[index] = player
    return True
  
  return False

def updateEstimateValueOfS(sPrime, s, alpha):
  V[s] = V[s] + alpha*(V[sPrime] - V[s])       #RJ problem --- why not chosen gamma?// since we know next state, gamma = 1, also no reward 

def getListOfBlankTiles(board):
	blanks = []
	for i in range(0,9):
		if board[i] == 0:
			blanks.append(i)
	return blanks

if __name__ == "__main__":
    print("Initializing!")
    print("Creating states")
    create_all_states(board, 1)
    create_all_states(board, 2)
    print("States are created")

    print("Dumping States!")
    fname = "/temp/States.pickle"
    file_ = abspath(fname)
    with open(file_, "wb") as f:
        pickle.dump(states, f)
    print(file_)
    print("Dumped!")
    print(os.path.exists(file_))
    
    print("Dumping Value Function!")
    fname = "/temp/InitialValueFunction.pickle"
    file_ = abspath(fname)
    with open(file_, "wb") as f:
        pickle.dump(V, f)
    print(file_)
    print("Dumped!")

    print(os.path.isdir("/temp"))
    print(os.path.exists("/temp/States.pickle"))

    print("Initialization Complete!")