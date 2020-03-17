import numpy as np
from numpy import random
import pickle


V = []
states = []
totalStates = 0
alpha = 0.2

board = [0]*9
tiles = [0,1,2]
players = [1,2]

def initBoard():
	for i in range(0,9):
		board[i] = 0

def printBoard(board):
	for i in range(len(board)):
		
		if (i%3==0):
			print('\n')

		if board[i] == 1:
			print('X ',end='')
		elif board[i] == 2:
			print('O ',end = '')
		else:
			print('- ',end='')


	return 

def printStates(States):
	for state in States:
		
		printBoard(state)
		print("\n")

	return 

def printValueFunction(values):
	for val in values:
		print(val,"\n")

def updateEstimateValueOfS(s, sPrime):
	V[s] = V[s] + alpha*(V[sPrime] - V[s])       #why not chosen gamma?

def switch_player(player):
	if player == 1:
		return 2
	else:
		return 1

def getListOfBlankTiles():
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
	if getListOfBlankTiles() is not []:
		return 0

	return -1                #for draw!... np more move is possible

def updateBoard(_board, player, index):
  if _board[index] == 0:
    _board[index] = player           # RJ: should be tiles[player]
    return True
  
  return False

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


def create_all_states(board,player):

	#base condition:
	result = isWinner(board) 
	if result == 1 or result == -1:     #either won or draw!
		return 

	for i in range(len(board)):
		if board[i] == 0:
			board[i] = player         #either 1 or 2
			if board[:] not in states:
				states.append(board[:])
				V.append(determineValue(board,player))
			create_all_states(board,switch_player(player))
			board[i] = 0              #so that for next i it will be zero


def greedyMove():
	maxValue = 0
	maxIndex = 0
	possibleMoves = getListOfBlankTiles()
	nextMove = possibleMoves.pop()      #here we assumed any 1 move from all possible moves!
	board[nextMove] = 1
	maxIndex = states.index(board)      #for current board setting
	maxValue = V[maxIndex]
	board[nextMove] = 0                 #setting again to zero until we find the real one!

	for i in possibleMoves:
		board[i] = 1
		idx = states.index(board)
		val = V[idx]

		if(val>maxValue):
			maxValue = val
			maxIndex = idx
			nextMove = i
		board[i] = 0                    #so that for next iteration, this remains a un-filled place 
		                                

	return nextMove, maxIndex



initBoard()

for player in players:
	create_all_states(board,player)



totalStates += len(states)                    #

print("Total Possible States in TicTacToe game are: {} !".format(totalStates))

#loading states using pickle and initialized value function!
with open('States.pickle',"wb") as fo:
	pickle.dump(states,fo)
with open('ValueFunction.pickle',"wb") as fo:
	pickle.dump(V,fo)



'''
print("first 100 states are : and corresponding values are  :")
for i in range(100):
	#print("state {}".format(i))
	printStates(states[i:i+1])
	print("val for state {}: ".format(i))
	printValueFunction(V[i:i+1])
'''



player1won = 0
player2won = 0
draws = 0
prevIndex = 0
maxIndex = 0
'''
while(True):

	initBoard()
	player = random.randint(1,3)
	print("player 1: {}".format("Computer"))
	print("player 2: {}".format("User"))
	print("Game Begins!")

	while(True):
		exploring = False
		possibleMoves = getListOfBlankTiles()
		num_possibleMoves = len(possibleMoves)

		if player == 2:
			userPlay = int(raw_input("Enter your move(1-9"))
			if userPlay not in range(1,10):
				print("Next Time enter number within the range!")
				print("U lost")



'''