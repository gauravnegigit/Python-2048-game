import pygame
import random
pygame.font.init()

#screen variables 
WIDTH , HEIGHT = 500,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2048 GAME USING PYGAME MODULE !")
FPS = 60

#font variables
NUMBER_FONT = pygame.font.SysFont("ARIAL BLACK", 40)
SCORE_FONT = pygame.font.SysFont("ARIAL BLACK",30)

def add_2(mat):
	r = random.randint(0,3)
	c = random.randint(0,3)
	board = [y for x in mat for y in x]
	while mat[r][c] != 0 :
		r = random.randint(0,3)
		c = random.randint(0,3)
		if board.count(0) <= 0:
			break
	if board.count(0) >0:
		mat[r][c] = 2
	return mat

def init():
	# method for designing board in the starting of the game 
	global score , high_scores
	mat = [[0 for x in range(4)] for x in range(4)]
	mat = add_2(mat)
	mat = add_2(mat)
	score , high_score = 0,0
	return mat

def game_status(mat):
	for i in range(len(mat)):
		for j in range(len(mat)):
			if mat[i][j] == 2048:
				return 'YOU WON !'
	for i in range(len(mat)):
		for j in range(len(mat)):
			if mat[i][j] == 0:
				return 'GAME NOT OVER!'

	#checking for the possibility of cell being full but can be merged
	for i in range(3):
		for j in range(3):
			if mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1] :
				return 'GAME NOT OVER!'
	return 'YOU LOST !'

def compress(mat):
	change = False
	new_mat = [[0 for x in range(4)] for x in range(4)]
	for i in range(4):
		pos = 0 
		for j in range(4):
			if mat[i][j] != 0 :
				new_mat[i][pos] = mat[i][j]
				if j != pos :
					change = True
				pos += 1
	return new_mat , change

def merge(mat):
	global score
	change = False
	for i in range(4):
		for j in range(3):
			if mat[i][j] == mat[i][j+1] and mat[i][j] != 0 :
				mat[i][j] = mat[i][j] *2
				mat[i][j+1] = 0 
				score += 10
				change = True
	return mat , change

def reverse(mat): 
	new_mat = [[mat[i][3-j] for j in range(4)] for i in range(4)]
	return new_mat 

def transpose(mat):
	new_mat = [[mat[j][i] for j in range(4)] for i in range(4)]
	return new_mat 

def move_left(mat):
	mat , change1 = compress(mat)
	mat , change2 = merge(mat)
	mat , temp = compress(mat)
	change = change1 or change2
	return mat , change

def move_right(mat):
	mat = reverse(mat)
	mat , change = move_left(mat)
	mat = reverse(mat)
	return mat , change

def move_up(mat):
	mat = transpose(mat)
	mat , change = move_left(mat)
	mat = transpose(mat)
	return mat , change

def move_down(mat):
	mat = transpose(mat)
	mat , change = move_right(mat)
	mat = transpose(mat)
	return mat , change

def display(text , y):
	text = SCORE_FONT.render(text , 1, (255,255,255))
	WIN.blit(text , (WIDTH //2 - text.get_width()//2 , y))

def draw(board, score ,high_score):
	global mat
	WIN.fill((0,0,0))
	x,y = 0,0
	gap = WIDTH//4
	game_check = game_status(mat)
	if game_status(mat) == "GAME NOT OVER!":
		for i in range(4):
			x += gap
			y += gap
			pygame.draw.line(WIN , (0,255,0), (x,0) , (x,WIDTH))
			pygame.draw.line(WIN , (0,255,0), (0,y) , (WIDTH ,y))
		for i,c in enumerate(board):
			text = NUMBER_FONT.render(c , 1, (255,255,255))
			WIN.blit(text , ((i%4+0.5)*gap - text.get_width()//2 , (i//4+0.5)*gap - text.get_height()//2))
	else:
		display(game_check , HEIGHT//2 - 50)
		display(f"SCORE : {score}" , HEIGHT//2)
		display(f"HIGH SCORE : {high_score}" , HEIGHT//2 + 50)

		pygame.display.update()
		pygame.time.delay(1500)
		mat = init()
	pygame.display.update()

#main loop for the game
def main():
	global score , mat
	run = True 
	clock = pygame.time.Clock()
	board = ['' for x in range(16)]
	mat = init()
	score = 0 
	high_score = 0

	while run :
		clock.tick(FPS)
		ind = 0
		for i in mat:
			for j in i:
				if j != 0 :
					board[ind] = str(j)
				else:
					board[ind] = "" 
				ind += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
				if event.key == pygame.K_UP:
					mat , flag = move_up(mat)
				elif event.key == pygame.K_DOWN:
					mat , flag = move_down(mat)
				elif event.key == pygame.K_LEFT:
					mat , flag = move_left(mat)
				elif event.key == pygame.K_RIGHT:
					mat , flag = move_right(mat)
				
				if flag :
					mat = add_2(mat)
				if high_score<score :
					high_score = score
		draw(board , score ,high_score)

	pygame.quit()
if __name__ == '__main__':
	main()
