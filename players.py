import random
import time
import pygame
import math
from copy import deepcopy

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	#Function to get the evaluation function value
	def getEval(self, env, depth, bool_val):

		#Get the evaluation function value
		eval_function_val = 0
		player1_val = 0
		player2_val = 0

		#need to access the diff columns or rows
		for i in env.board:

			#how do i find the number of tokens in each column
			if column1 or column7:
				player1_val = player1_val + num_player1_tokens
				player2_val = player2_val + num_player2_tokens

			elif column2 or column6:
				player1_val = player1_val + (1.25 * num_player1_tokens)
				player2_val = player2_val + (1.25 * num_player2_tokens)

			elif column3 or column5:
				player1_val = player1_val + (1.5 * num_player1_tokens)
				player2_val = player2_val + (1.5 * num_player2_tokens)

			elif column4:
				player1_val = player1_val + (2 * num_player1_tokens)
				player2_val = player2_val + (2 * num_player2_tokens)

		eval_function_val = player1_val - player2_val

		return eval_function_val




		# Two cases: 1) If depth is 0 and game is not over, return eval function
		# 2) If depth is 0 and game is over, just return node value (eval.gameOver() = Bool)
		
		if depth == 0 and bool_val == False:
			return eval_function_val
		
		if depth == 0 and bool_val == True:
			return bool_val

#Min/Max Player function
#Steps:
#1) generate all 7 different boards, each one with coin in diff column
#how do i generate a move, and then get a copy of the updated board
#2) check to see if the coin placement in column results in gameOver or at depth
#if it does, return the evaluation function of that board
#3) for each board, get the min or max value (which calls either Min or Max_Val)
#4) this restarts the process


	#Max Player function
	def Max_Val(self, env, depth):

		#check to see if set depth has been reached
		if depth == 0 or env.gameOver(self.position, 1):
			return self.getEval(env, depth, env.gameOver(self.position, 1))
		
		#set value
		value = math.inf

		#create list of columns that a move can be played in
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		#go through the successors, 7 envs with a different move in each one
		env = deepcopy(env)
		for i in indices:
			value = max(value, self.Min_Val(self.play(env, [i]), depth-1))

		return value


	def Min_Val(self, env, depth):

		#check to see if set depth has been reached
		if depth == 0 or env.gameOver(self.position, 2):
			return self.getEval(env, depth, env.gameOver(self.position, 2))
		
		#set value
		value = math.inf

		#create list of columns that a move can be played in
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		#go through the successors, 7 envs with a different move in each one
		env = deepcopy(env)
		for i in indices:
			value = min(value, self.Max_Val(self.play(env, [i]), depth-1))

		return value


	def minimax_dec(self, env, depth, MaxPlayer):

		#how to get a state from board, codewise
		state = self.position #???
		value = self.Max_Val(state)

		#Return action in the children state that has value v
		#how to do this?
		return 


	def play(self, env, move):
		env = deepcopy(env)
		self.minimax_dec(env, depth, MaxPlayer)
		move[:] = [np.argmax(vs)] #change the second brackets to determine column to drop in
		pass





class alphaBetaAI(connect4Player):

	def play(self, env, move):
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




