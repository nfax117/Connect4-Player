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

	#I still don't think that my player is being correctly detected. When I run, it seems that 
	#my AI is picking the minimum values. It puts a coin in the outermost columns rather than the middle.
	
	#it also doesnt see when there is a possible blocking of a 4 in a row. I think that this is still due
	#to it treating my function as the wrong player

	#what exactly does self.position do?

	#should i screenshot the gameboard output and put onto the submission doc?

	#playing against montecarlo, i do not block for some reason


	#Function to get the evaluation function value
	def getEval(self, env, GO_bool, player, last_col):

		# If i win, set the eval value very high, if i lose very low
		if GO_bool == True and player == self.position:
			return 100000

		if GO_bool == True and player == self.opponent.position:
			return -100000
		
		eval_function_val = 0
		player1_val = 0
		player2_val = 0
		board = env.getBoard()
		'''
		config1_1 = False
		config1_2 = False
		config2_1 = False
		config2_2 = False
		config3_1 = False
		config3_2 = False
		config4_1 = False
		config4_2 = False
		'''
		config5_1 = False
		config5_2 = False
		config6_1 = False
		config6_2 = False
		config7_1 = False
		config7_2 = False
		#config8_1 = False
		#config8_2 = False
		config9_1 = False
		config9_2 = False
		config10_1 = False
		config10_2 = False
		config11_1 = False
		config11_2 = False
		config12_1 = False
		config12_2 = False
		block_3row_1 = False
		block_3row_2 = False

		last_row = env.topPosition[last_col]
		#print("Last Col:", last_col, "Last Row:", last_row)

		#Need to implement blocking 4 in a rows with parameter of column that the move was played in.
		#use board[env.topPosition[move]][move] to see where the last coin placed lies.

		#check if three in a row below the placement
		if last_row < 3:
			if board[last_row][last_col] == 1 and board[last_row+1][last_col] == 2 and board[last_row+2][last_col] == 2 and board[last_row+3][last_col] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row+1][last_col] == 1 and board[last_row+2][last_col] == 1 and board[last_row+3][last_col] == 1:
				block_3row_2 = True

		#check if there is three in a row to the left
		if last_col > 2:
			if board[last_row][last_col] == 1 and board[last_row][last_col-1] == 2 and board[last_row][last_col-2] == 2 and board[last_row][last_col-3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row][last_col-1] == 1 and board[last_row][last_col-2] == 1 and board[last_row][last_col-3] == 1:
				block_3row_2 = True

		#check if there is three in a row to the right
		if last_col < 4:
			if board[last_row][last_col] == 1 and board[last_row][last_col+1] == 2 and board[last_row][last_col+2] == 2 and board[last_row][last_col+3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row][last_col+1] == 1 and board[last_row][last_col+2] == 1 and board[last_row][last_col+3] == 1:
				block_3row_2 = True
		#check if there is three in a row to northeast
		if last_col < 4 and last_row > 2:
			if board[last_row][last_col] == 1 and board[last_row-1][last_col+1] == 2 and board[last_row-2][last_col+2] == 2 and board[last_row-3][last_col+3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row-1][last_col+1] == 1 and board[last_row-2][last_col+2] == 1 and board[last_row-3][last_col+3] == 1:
				block_3row_2 = True

		#check if there is three in a row to southeast
		if last_col < 4 and last_row < 3:
			if board[last_row][last_col] == 1 and board[last_row+1][last_col+1] == 2 and board[last_row+2][last_col+2] == 2 and board[last_row+3][last_col+3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row+1][last_col+1] == 1 and board[last_row+2][last_col+2] == 1 and board[last_row+3][last_col+3] == 1:
				block_3row_2 = True

		#check if there is three in a row to northwest
		if last_col > 2 and last_row > 2:
			if board[last_row][last_col] == 1 and board[last_row-1][last_col-1] == 2 and board[last_row-2][last_col-2] == 2 and board[last_row-3][last_col-3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row-1][last_col-1] == 1 and board[last_row-2][last_col-2] == 1 and board[last_row-3][last_col-3] == 1:
				block_3row_2 = True

		#check if there is three in a row to southwest
		if last_col > 2 and last_row < 3:
			if board[last_row][last_col] == 1 and board[last_row+1][last_col-1] == 2 and board[last_row+2][last_col-2] == 2 and board[last_row+3][last_col-3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row+1][last_col-1] == 1 and board[last_row+2][last_col-2] == 1 and board[last_row+3][last_col-3] == 1:
				block_3row_2 = True

		#print("here", board)
		#Board is 2d array, (row, col) = (0,0) is the top left corner

		for col in range(7): #Iterate through the columns
			for row in range(6): #Iterate through the rows

				#Need to check if three in a row with blank space on either opposite ends.

				#Southeast
				if col < 4 and row < 3:
					#player one with open connect 4
					if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1 and board[row+3][col+3] == 0:
						config5_1 = True
					#player two with open connect 4
					if board[row][col] == 2 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2 and board[row+3][col+3] == 0:
						config5_2 = True

					if board[row][col] == 0 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1 and board[row+3][col+3] == 1:
						config9_1 = True
					if board[row][col] == 0 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2 and board[row+3][col+3] == 2:
						config9_2 = True

				#Northeast
				if col < 4 and row > 2:
					if board[row][col] == 1 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1 and board[row-3][col+3] == 0:
						config6_1 = True
					if board[row][col] == 2 and board[row-1][col+1] == 2 and board[row-2][col+2] == 2 and board[row-3][col+3] == 0:
						config6_2 = True

					if board[row][col] == 0 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1 and board[row-3][col+3] == 1:
						config10_1 = True
					if board[row][col] == 0 and board[row-1][col+1] == 2 and board[row-2][col+2] == 2 and board[row-3][col+3] == 2:
						config10_2 = True

				#Right
				if col < 4:
					if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+2] == 1 and board[row][col+3] == 0:
						config7_1 = True
					if board[row][col] == 2 and board[row][col+1] == 2 and board[row][col+2] == 2 and board[row][col+3] == 0:
						config7_2 = True

					if board[row][col] == 0 and board[row][col+1] == 1 and board[row][col+2] == 1 and board[row][col+3] == 1:
						config11_1 = True
					if board[row][col] == 0 and board[row][col+1] == 2 and board[row][col+2] == 2 and board[row][col+3] == 2:
						config11_2 = True

				#Down
				if row < 3:
					#This cannot happen
					#if board[row][col] == 2 and board[row+1][col] == 2 and board[row+2][col] == 2 and board[row+3][col] == 0:
					#	config8_2 = True
					#if board[row][col] == 1 and board[row+1][col] == 1 and board[row+2][col] == 1 and board[row+3][col] == 0:
					#	config8_1 = True

					if board[row][col] == 0 and board[row+1][col] == 2 and board[row+2][col] == 2 and board[row+3][col] == 2:
						config12_2 = True
					if board[row][col] == 0 and board[row+1][col] == 1 and board[row+2][col] == 1 and board[row+3][col] == 1:
						config12_1 = True

				'''
				#Need to check for resulting 3 in a row plays
				#Southeast
				if col < 5 and row < 4:
					if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1:
						config3_1 = True
					if board[row][col] == 2 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2:
						config3_2 = True
				#Northeast
				if col < 5 and row > 1:
					if board[row][col] == 1 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1:
						config4_1 = True
					if board[row][col] == 2 and board[row-1][col+1] == 2 and board[row-2][col+2] == 2:
						config4_2 = True
				#Right
				if col < 5:
					if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+2] == 1:
						config1_1 = True
					if board[row][col] == 2 and board[row][col+1] == 2 and board[row][col+2] == 2:
						config1_2 = True
				#Down
				if row < 4:
					if board[row][col] == 2 and board[row+1][col] == 2 and board[row+2][col] == 2:
						config2_2 = True
					if board[row][col] == 1 and board[row+1][col] == 1 and board[row+2][col] == 1:
						config2_1 = True
				'''

				#Assign weights based on column number
				if col==0 or col==6:
					if board[row][col] == 1: #player 1 (Max Player)

						player1_val = player1_val + 1
					
					elif board[row][col] == 2: #player 2 (Min Player)
					
						player2_val = player2_val + 1

				elif col==1 or col==5:
					if board[row][col] == 1:

						player1_val = player1_val + 2
					
					elif board[row][col] == 2:
					
						player2_val = player2_val + 2

				elif col==2 or col==4:
					if board[row][col] == 1:

						player1_val = player1_val + 5
					
					elif board[row][col] == 2:
					
						player2_val = player2_val + 5

				elif col==3:
					if board[row][col] == 1:

						player1_val = player1_val + 10
					
					elif board[row][col] == 2:
					
						player2_val = player2_val + 10

				else:
					print("Error")
					pass

		#Weighting for blocking an opponent potential 4 in a row
		if block_3row_1 == True:
			player1_val = player1_val + 100
		
		if block_3row_2 == True:
			player2_val = player2_val + 100

		'''
		#Weighting for 3 in rows
		if config1_1 or config2_1 or config3_1 or config4_1:
			player1_val = player1_val + 5

		if config1_2 or config2_2 or config3_2 or config4_2:
			player2_val = player2_val + 5
		'''

		#three in a row with open 4th slot
		if config5_1 or config6_1 or config7_1:
			player1_val = player1_val + 10
		if config5_2 or config6_2 or config7_2:
			player2_val = player2_val + 10

		#three in a row with open 1st slot
		if config9_1 or config10_1 or config11_1 or config12_1:
			player1_val = player1_val + 10
		if config9_2 or config10_2 or config11_2 or config12_2:
			player2_val = player2_val + 10


		#Determine who is player 1 and 2
		if player == self.position:
			eval_function_val = player1_val - player2_val
		elif player == self.opponent.position:
			eval_function_val = player2_val - player1_val

		
		return eval_function_val

		#print("Eval Value:", eval_function_val)


#Min/Max Player function
#Steps:
#1) generate all 7 different boards, each one with coin in diff column
#how do i generate a move, and then get a copy of the updated board
#2) check to see if the coin placement in column results in gameOver or at depth
#if it does, return the evaluation function of that board
#3) for each board, get the min or max value (which calls either Min or Max_Val)
#4) this restarts the process


	#Max Player function
	def Max_Val(self, env, depth, player, last_col):

		#check to see if set depth has been reached
		#if first recursion
		if depth != 3:
			if depth == 0 or env.gameOver(env.history[0][-1], player):
				return self.getEval(env, env.gameOver(env.history[0][-1], player), player, last_col), None
		
		#set value
		best_value = -math.inf
		best_move = -1

		#create list of columns that a move can be played in
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		#go through the successors, 7 envs with a different move in each one
		#switch = {1:2,2:1}
		#player = switch[player]
		player = self.position

		for i in indices:
			env = deepcopy(env)
			env.visualize = False
			self.simulateMove(env, i, player)

			value = self.Min_Val(env, depth-1, player, i)[0]

			if value > best_value:
				best_value = value
				best_move = i

		#print("Best Value:", best_value)
		return best_value, best_move


	#Min Player Function
	def Min_Val(self, env, depth, player, last_col):

		#check to see if set depth has been reached
		if depth != 3:
			if depth == 0 or env.gameOver(env.history[0][-1], player):
				return self.getEval(env, env.gameOver(env.history[0][-1], player), player, last_col), None
		
		#set value
		best_value = math.inf
		best_move = -1

		#create list of columns that a move can be played in
		possible = env.topPosition >= 0 #makes array: [True, False, ..., True]
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		#go through the successors, 7 envs with a different move in each one
		#switch = {1:2,2:1}
		#player = switch[player]

		player = self.opponent.position
		for i in indices:
			env = deepcopy(env)
			env.visualize = False
			self.simulateMove(env, i, player)

			value = self.Max_Val(env, depth-1, player, i)[0]

			if value < best_value:
				best_value = value
				best_move = i

		return best_value, best_move


	def minimax_dec(self, env, depth, player):

		env = deepcopy(env)
		value, action = self.Max_Val(env, depth, player, None)

		return value, action


	def play(self, env, move):

		env = deepcopy(env)
		player = self.position
		depth = 3 #Can change this to any depth that doesn't go over time limit (MAX = 3)
		
		action = [self.minimax_dec(env, depth, player)[1]]
		print("No Time out, play in column:", action)
		move[:] = action
			

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)



class alphaBetaAI(connect4Player):

	def play(self, env, move):
		env = deepcopy(env)
		player = self.position

		alpha = -math.inf
		beta = math.inf

		action = [self.Alpha_Beta_Seach(self, alpha, beta, player)[1]]
		print("No Time out, play in column:", action)
		move[:] = action


	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)


	def Alpha_Beta_Seach(self, env, alpha, beta, player):
		env = deepcopy(env)
		depth = 5
		value, action = self.Max_Val_AB(env, alpha, beta, player, depth, None)

		return value, action

	def rearrange(self, array):
		temp = []
		if 3 in array: temp.append(3)
		if 2 in array: temp.append(2)
		if 4 in array: temp.append(4)
		if 1 in array: temp.append(1)
		if 5 in array: temp.append(5)
		if 0 in array: temp.append(0)
		if 6 in array: temp.append(6)
		return temp


	def Max_Val_AB(self, env, alpha, beta, player, depth, last_col):
		#check to see if terminal state reached, no plays left to make
		#count is used to make sure it is not the first recursion
		if depth != 5:
			if depth == 0 or env.gameOver(env.history[0][-1], player):
				return self.getEval(env, env.gameOver(env.history[0][-1], player), player, last_col), None
	
		#possible = env.topPosition >= 0
		#if all(possible) == False or env.gameOver(env.history[0][-1], player):
		#	return self.getEval(env, env.gameOver(env.history[0][-1], player), player, last_col), None
		
		#set value
		best_value = -math.inf
		best_move = -1

		#create list of columns that a move can be played in
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		#go through the successors, 7 envs with a different move in each one
		player = self.opponent.position

		#order the moves to go from middle column play first, outwards
		indices = self.rearrange(indices)

		for i in indices:
			env = deepcopy(env)
			env.visualize = False

			#Need successor function to order children boards from greatest to least, then call Min_Val_AB
			#order based on which column a move is played in (middle to side columns)

			self.simulateMove(env, i, player)

			value = self.Min_Val_AB(env, alpha, beta, player, depth-1, i)[0]

			if value > beta:
				best_value = value
				best_move = i
				return best_value, best_move
			
			alpha = max(alpha, value)

		return best_value, best_move


	def Min_Val_AB(self, env, alpha, beta, player, depth, last_col):

		if depth != 5:
			if depth == 0 or env.gameOver(env.history[0][-1], player):
				return self.getEval(env, env.gameOver(env.history[0][-1], player), player, last_col), None

		#set value
		best_value = math.inf
		best_move = -1

		#create list of columns that a move can be played in
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		#go through the successors, 7 envs with a different move in each one
		player = self.opponent.position

		#order the moves to go from middle column play first, outwards
		indices = self.rearrange(indices)

		for i in indices:
			env = deepcopy(env)
			env.visualize = False

			#Need successor function to order children boards from greatest to least, then call Max_Val_AB

			self.simulateMove(env, i, player)

			value = self.Max_Val_AB(env, alpha, beta, player, depth-1, i)[0]

			if value < alpha:
				best_value = value
				best_move = i
				return best_value, best_move
			
			beta = min(beta, value)

		return best_value, best_move


	#Function to get the evaluation function value
	def getEval(self, env, GO_bool, player, last_col):

		# If i win, set the eval value very high, if i lose very low
		if GO_bool == True and player == self.position:
			return 100000

		if GO_bool == True and player == self.opponent.position:
			return -100000
		
		eval_function_val = 0
		player1_val = 0
		player2_val = 0
		board = env.getBoard()
		config1_1 = False
		config1_2 = False
		config2_1 = False
		config2_2 = False
		config3_1 = False
		config3_2 = False
		config4_1 = False
		config4_2 = False
		config5_1 = False
		config5_2 = False
		config6_1 = False
		config6_2 = False
		config7_1 = False
		config7_2 = False
		#config8_1 = False
		#config8_2 = False
		config9_1 = False
		config9_2 = False
		config10_1 = False
		config10_2 = False
		config11_1 = False
		config11_2 = False
		config12_1 = False
		config12_2 = False
		block_3row_1 = False
		block_3row_2 = False

		last_row = env.topPosition[last_col]
		#print("Last Col:", last_col, "Last Row:", last_row)

		#Need to implement blocking 4 in a rows with parameter of column that the move was played in.
		#use board[env.topPosition[move]][move] to see where the last coin placed lies.

		#check if three in a row below the placement
		if last_row < 3:
			if board[last_row][last_col] == 1 and board[last_row+1][last_col] == 2 and board[last_row+2][last_col] == 2 and board[last_row+3][last_col] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row+1][last_col] == 1 and board[last_row+2][last_col] == 1 and board[last_row+3][last_col] == 1:
				block_3row_2 = True

		#check if there is three in a row to the left
		if last_col > 2:
			if board[last_row][last_col] == 1 and board[last_row][last_col-1] == 2 and board[last_row][last_col-2] == 2 and board[last_row][last_col-3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row][last_col-1] == 1 and board[last_row][last_col-2] == 1 and board[last_row][last_col-3] == 1:
				block_3row_2 = True

		#check if there is three in a row to the right
		if last_col < 4:
			if board[last_row][last_col] == 1 and board[last_row][last_col+1] == 2 and board[last_row][last_col+2] == 2 and board[last_row][last_col+3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row][last_col+1] == 1 and board[last_row][last_col+2] == 1 and board[last_row][last_col+3] == 1:
				block_3row_2 = True
		#check if there is three in a row to northeast
		if last_col < 4 and last_row > 2:
			if board[last_row][last_col] == 1 and board[last_row-1][last_col+1] == 2 and board[last_row-2][last_col+2] == 2 and board[last_row-3][last_col+3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row-1][last_col+1] == 1 and board[last_row-2][last_col+2] == 1 and board[last_row-3][last_col+3] == 1:
				block_3row_2 = True

		#check if there is three in a row to southeast
		if last_col < 4 and last_row < 3:
			if board[last_row][last_col] == 1 and board[last_row+1][last_col+1] == 2 and board[last_row+2][last_col+2] == 2 and board[last_row+3][last_col+3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row+1][last_col+1] == 1 and board[last_row+2][last_col+2] == 1 and board[last_row+3][last_col+3] == 1:
				block_3row_2 = True

		#check if there is three in a row to northwest
		if last_col > 2 and last_row > 2:
			if board[last_row][last_col] == 1 and board[last_row-1][last_col-1] == 2 and board[last_row-2][last_col-2] == 2 and board[last_row-3][last_col-3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row-1][last_col-1] == 1 and board[last_row-2][last_col-2] == 1 and board[last_row-3][last_col-3] == 1:
				block_3row_2 = True

		#check if there is three in a row to southwest
		if last_col > 2 and last_row < 3:
			if board[last_row][last_col] == 1 and board[last_row+1][last_col-1] == 2 and board[last_row+2][last_col-2] == 2 and board[last_row+3][last_col-3] == 2:
				block_3row_1 = True
			if board[last_row][last_col] == 2 and board[last_row+1][last_col-1] == 1 and board[last_row+2][last_col-2] == 1 and board[last_row+3][last_col-3] == 1:
				block_3row_2 = True

		#print("here", board)
		#Board is 2d array, (row, col) = (0,0) is the top left corner

		for col in range(7): #Iterate through the columns
			for row in range(6): #Iterate through the rows

				#Need to check if three in a row with blank space on either opposite ends.

				#Southeast
				if col < 4 and row < 3:
					#player one with open connect 4
					if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1 and board[row+3][col+3] == 0:
						config5_1 = True
					#player two with open connect 4
					if board[row][col] == 2 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2 and board[row+3][col+3] == 0:
						config5_2 = True

					if board[row][col] == 0 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1 and board[row+3][col+3] == 1:
						config9_1 = True
					if board[row][col] == 0 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2 and board[row+3][col+3] == 2:
						config9_2 = True

				#Northeast
				if col < 4 and row > 2:
					if board[row][col] == 1 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1 and board[row-3][col+3] == 0:
						config6_1 = True
					if board[row][col] == 2 and board[row-1][col+1] == 2 and board[row-2][col+2] == 2 and board[row-3][col+3] == 0:
						config6_2 = True

					if board[row][col] == 0 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1 and board[row-3][col+3] == 1:
						config10_1 = True
					if board[row][col] == 0 and board[row-1][col+1] == 2 and board[row-2][col+2] == 2 and board[row-3][col+3] == 2:
						config10_2 = True

				#Right
				if col < 4:
					if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+2] == 1 and board[row][col+3] == 0:
						config7_1 = True
					if board[row][col] == 2 and board[row][col+1] == 2 and board[row][col+2] == 2 and board[row][col+3] == 0:
						config7_2 = True

					if board[row][col] == 0 and board[row][col+1] == 1 and board[row][col+2] == 1 and board[row][col+3] == 1:
						config11_1 = True
					if board[row][col] == 0 and board[row][col+1] == 2 and board[row][col+2] == 2 and board[row][col+3] == 2:
						config11_2 = True

				#Down
				if row < 3:
					#This cannot happen
					#if board[row][col] == 2 and board[row+1][col] == 2 and board[row+2][col] == 2 and board[row+3][col] == 0:
					#	config8_2 = True
					#if board[row][col] == 1 and board[row+1][col] == 1 and board[row+2][col] == 1 and board[row+3][col] == 0:
					#	config8_1 = True

					if board[row][col] == 0 and board[row+1][col] == 2 and board[row+2][col] == 2 and board[row+3][col] == 2:
						config12_2 = True
					if board[row][col] == 0 and board[row+1][col] == 1 and board[row+2][col] == 1 and board[row+3][col] == 1:
						config12_1 = True


				#Need to check for resulting 3 in a row plays

				#Southeast
				if col < 5 and row < 4:
					if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1:
						config3_1 = True
					if board[row][col] == 2 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2:
						config3_2 = True
				#Northeast
				if col < 5 and row > 1:
					if board[row][col] == 1 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1:
						config4_1 = True
					if board[row][col] == 2 and board[row-1][col+1] == 2 and board[row-2][col+2] == 2:
						config4_2 = True
				#Right
				if col < 5:
					if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+2] == 1:
						config1_1 = True
					if board[row][col] == 2 and board[row][col+1] == 2 and board[row][col+2] == 2:
						config1_2 = True
				#Down
				if row < 4:
					if board[row][col] == 2 and board[row+1][col] == 2 and board[row+2][col] == 2:
						config2_2 = True
					if board[row][col] == 1 and board[row+1][col] == 1 and board[row+2][col] == 1:
						config2_1 = True


				#Assign weights based on column number
				if col==0 or col==6:
					if board[row][col] == 1: #player 1 (Max Player)

						player1_val = player1_val + 1
					
					elif board[row][col] == 2: #player 2 (Min Player)
					
						player2_val = player2_val + 1

				elif col==1 or col==5:
					if board[row][col] == 1:

						player1_val = player1_val + 1.25
					
					elif board[row][col] == 2:
					
						player2_val = player2_val + 1.25

				elif col==2 or col==4:
					if board[row][col] == 1:

						player1_val = player1_val + 1.5
					
					elif board[row][col] == 2:
					
						player2_val = player2_val + 1.5

				elif col==3:
					if board[row][col] == 1:

						player1_val = player1_val + 2
					
					elif board[row][col] == 2:
					
						player2_val = player2_val + 2

				else:
					print("Error")
					pass

		#Weighting for blocking opponent 3 in a rows
		if block_3row_1 == True:
			player1_val = player1_val + 30
		
		if block_3row_2 == True:
			player2_val = player2_val + 30

		#Weighting for 3 in rows
		if config1_1 or config2_1 or config3_1 or config4_1:
			player1_val = player1_val + 5

		if config1_2 or config2_2 or config3_2 or config4_2:
			player2_val = player2_val + 5

		#three in a row with open 4th slot
		if config5_1 or config6_1 or config7_1:
			player1_val = player1_val + 10
		if config5_2 or config6_2 or config7_2:
			player2_val = player2_val + 10

		#three in a row with open 1st slot
		if config9_1 or config10_1 or config11_1 or config12_1:
			player1_val = player1_val + 10
		if config9_2 or config10_2 or config11_2 or config12_2:
			player2_val = player2_val + 10


		#Determine who is player 1 and 2
		if player == self.position:
			eval_function_val = player1_val - player2_val
		elif player == self.opponent.position:
			eval_function_val = player2_val - player1_val

		
		return eval_function_val

		#print("Eval Value:", eval_function_val)



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




