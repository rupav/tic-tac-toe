import pickle, os

players = [1, 2]
tiles = [0, 1, 2]

def abspath(fname):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    return dir_ + fname

def get_states(fname):
    file_ = abspath(fname)
    print("Inside get_states")
    print(file_)
    print(os.path.exists(file_))
    with open(file_, "rb") as f:
        states = pickle.load(f)
        return states
    
def get_value_function(fname):
    file_ = abspath(fname)
    try:
        with open(file_, "rb") as f:
            V = pickle.load(f)
            return V
    except:
        print(fname, "not found")
        return False

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


def greedyMove(board, states, V):
    maxValue = 0
    maxIndex = 0
    possibleMoves = getListOfBlankTiles(board)    
    nextMove = possibleMoves.pop()      #here we assumed any 1 move from all possible moves!
    board[nextMove] = 1
    if isWinner(board) == 1:
        return nextMove, -1
    maxIndex = states.index(board)      #for current board setting
    maxValue = V[maxIndex]
    board[nextMove] = 0                 #setting again to zero until we find the real one!

    for i in possibleMoves:
        board[i] = 1
        if isWinner(board) == 1:
            return i, -1
        idx = states.index(board)
        val = V[idx]

        if(val > maxValue):
            maxValue = val
            maxIndex = idx
            nextMove = i
        board[i] = 0                    #so that for next iteration, this remains a un-filled place 

    return nextMove, maxIndex
