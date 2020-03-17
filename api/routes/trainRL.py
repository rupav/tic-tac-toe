from numpy import random
import pickle
import os

states = []
V = []
totalStates = 0

board = [0,0,0,0,0,0,0,0,0]

tiles = [0,1,2]

def abspath(fname):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    return dir_ + fname

def initBoard():
	for i in range(0,9):
		board[i] = 0

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

def printBoard(board):
	size = len(board)
	rows = []
	row = []
	for index in range(0, size):
		if board[index] == 1:
			row.append('X ')
		elif board[index] == 2:
			row.append('O ')
		else:
			row.append('_ ')

		if ((index+1)%3) == 0:
			rows.append(row)
			row = []
	for row in rows:
		print(row)
	
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

def greedyMove():
	maxValue = 0
	maxIndex = 0
	nextMoves = getListOfBlankTiles(board)
	boardIndex = nextMoves.pop()
	board[boardIndex] = 1
	maxIndex = states.index(board)
	maxValue = V[maxIndex]
	board[boardIndex] = 0

	for i in nextMoves:
		board[i] = 1
		idx = states.index(board)
		if V[idx] > maxValue:
			boardIndex = i
			maxIndex = idx
			maxValue = V[idx]
		board[i] = 0
	return boardIndex,maxIndex

def trainRL(alpha, episodes):

    global states
    states = []
    global V
    V = []
    print("Initializing states and Value function!")
    create_all_states(board,1)
    create_all_states(board,2)
    totalStates = len(states)
    print ("Total States: ", totalStates)
    return totalStates

    numPlayer1Won = 0
    numPlayer2Won = 0
    numDraws = 0
    prevIndex = 0          # previous state index
    maxIndex = 0 

    player = 1
    last_loss_episode = 1
    print("Let the game begins!")
    total = episodes
    while(episodes != 0):
        episodes -= 1
        initBoard()
        # player = random.randint(1,3)
        player = 1

        print ("Player 1 = Compuer")
        print ("Player 2 = You!")

        printBoard(board)

        while(True):

            nextMoves = getListOfBlankTiles(board)
            countNextMoves = len(nextMoves)
            exploring = False

            print("Player ", player, "'s move: ")

            if player == 2:

                # userPlay = int(input("Enter move [1-9]: "))
                # userPlay = userPlay -1
                userPlay = nextMoves[random.randint(0, countNextMoves)]

            else:
                ex = random.randint(1,100)/(100.0)
                if ex<= 0.1:
                    userPlay = nextMoves[random.randint(0, countNextMoves)]
                    exploring = True
                    print ("exploring")
                else:
                    userPlay, maxIndex = greedyMove()      #we have not updated the board yet!
                    print ("greedy")
                    print("V(s) = ", V[prevIndex], " changed to ")
                    updateEstimateValueOfS(maxIndex, prevIndex, alpha)
                    print("V(s) = ", V[prevIndex])
                    prevIndex = maxIndex                          
            if True == updateBoard(board, player, userPlay):      #board has been updated finally!
                if exploring:
                    prevIndex = states.index(board)
                
        
            printBoard(board)
            
            won = hasWinner(board)
            if 1 == won:
                if 1 == player:                           ##if computer won
                    numPlayer1Won = numPlayer1Won + 1
                else:                                     #if user won (player = 2)
                    last_loss_episode = total - episodes
                    maxIndex = states.index(board)
                    updateEstimateValueOfS(maxIndex, prevIndex, alpha)
                    numPlayer2Won = numPlayer2Won + 1
                print ("Player has won! ", player )
                break
            
            if -1 == won:
                numDraws = numDraws + 1
                if player == 2:
                    maxIndex = states.index(board)
                    updateEstimateValueOfS(maxIndex, prevIndex, alpha)
                print ("It's a draw!")
                break
            
            player = switchPlayer(player)

    print ("-----")
    print ("Game Stats: ")
    print ("Player 1 # of Wins  : ", numPlayer1Won)
    print ("Player 2 # of Wins  : ", numPlayer2Won)
    print ("         # of Draws : ", numDraws)
    print ("last_loss_episode: ", last_loss_episode)

    # dumping states using pickle and initialized value function!
    print(totalStates)
    fname = "/temp/States.pickle"
    file_ = abspath(fname)
    with open(file_, "wb") as f:
        pickle.dump(states, f)
    fname = "/temp/ValueFunction.pickle"
    file_ = abspath(fname)
    with open(file_,"wb") as f:
        pickle.dump(V, f)
    print("Dumped!!!!!!!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    trainRL(0.1, 100)
