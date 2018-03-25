import pickle

with open('States.pickle',"rb") as fo:
	states = pickle.load(fo)

print(len(states))
