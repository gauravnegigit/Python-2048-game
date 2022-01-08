import random

def print_board(board):
    print("------------------------------")
    print("|      |      |      |      |")
    print("| "+board[0]+" | "+board[1]+" | "+board[2]+" | "+board[3]+" |")
    print("|      |      |      |      |")
    print("-------------------------------")
    print("| "+board[4]+" | "+board[5]+" | "+board[6]+" | "+board[7]+" |")
    print("|      |      |      |      |")
    print("-------------------------------")
    print("| "+board[8]+" | "+board[9]+" | "+board[10]+" | "+board[11]+" |")
    print("|      |      |      |      |")
    print("--------------------------------")
    print("| "+board[12]+" | "+board[13]+" | "+board[14]+" | "+board[15]+" |")
    print("|      |      |      |      |")
    print("------------------------------")

def display_board(mat , board):
        #compensating the number to be in between of a particular block in the board
        ind = 0
        for i in mat:
            for j in i :
                if len(str(j)) == 1:
                    board[ind] = "  "+str(j)+" "
                elif len(str(j))== 2:
                    board[ind] = " "+str(j)+" "
                elif len(str(j)) == 3:
                    board[ind] = " " +str(j)
                elif len(str(j)) == 4:
                    board[ind] = str(j)
                ind +=1

        print_board(board)

def add_2(mat):
    r = random.randint(0,3)
    c = random.randint(0,3)
    while mat[r][c] !=0:
        r = random.randint(0,3)
        c = random.randint(0,3)
    mat[r][c] = 2
    return mat

def get_current_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == 2048:
                return 'WON'
    for i in range(len(mat)):
        for j in range(len(mat)):  
            if mat[i][j] == 0:
                return 'GAME NOT OVER!'
    for i in range(3):
        for j in range(3):
            if mat[i][j] == mat[i+1][j] or mat[i][j] == mat[i][j+1] :
                return 'GAME NOT OVER!'
    return 'LOST'

# the functions named compress and merged are used for the left key move
# then we may change the moves to up by tranversing the matrix and performing the left move 
# then we may change the moves to right by reversing the matrix and performing the left move 
# then we may change the moves to down by tranversing the matrix and performing the right move 

def compress(mat):
    change = False
    #creating copy of the matrix 
    new_mat = []
    for i in range(4):
        new_mat.append([0]*4)
    for i in range(4):
        pos = 0  
        for j in range(4):
            if mat[i][j] !=0:
                #we will compress the matrix when the cell is not empty 
                new_mat[i][pos] = mat[i][j]
                if j !=pos :
                    change = True
                pos +=1 

    return new_mat , change

def merge(mat):
    change = False
    for i in range(4):
        for j in range(3):

            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0 :
                mat[i][j] = mat[i][j] *2
                mat[i][j+1] = 0 
                change = True
    return mat, change


def reverse(mat):
    new_mat = [[mat[i][3-j] for j in range(4)] for i in range(4)]
    return new_mat

def transpose(mat):
    new_mat = [[mat[j][i] for j in range(4)] for i in range(4)]
    return new_mat

def move_left(grid):
    new_grid , change1 = compress(grid)
    new_grid,  change2 = merge(new_grid)
    change = change1 or change2
    new_grid, temp = compress(new_grid)
    return new_grid , change 

def move_right(grid):
    new_grid = reverse(grid)
    new_grid , change = move_left(new_grid)
    new_grid = reverse(new_grid)
    return new_grid , change 

def move_up(grid):
    new_grid = transpose(grid)
    new_grid , change = move_left(new_grid)
    new_grid = transpose(new_grid)
    return new_grid , change

def move_down(grid):
    new_grid = transpose(grid)
    new_grid, change = move_right(new_grid)
    new_grid = transpose(new_grid)
    return new_grid , change

def main():
    board = ['' for x in range(16)]
    mat = [[0 for x in range(4)] for x in range(4)]
    mat = add_2(mat)
    mat = add_2(mat)
    status = None

    name = input("HI TRAVELLER ! WHAT IS YOUR NAME ? ")
    wanna_play = input("HI {} , WELCOME TO 2048 GAME ! DO YOU WANNA PLAY THIS GAME ? (ENTER YES OR NO) ".format(name.lower().title()))
    print("\n\n\nCommands are as follows : ")
    print("'W' or 'w' : Move Up")
    print("'S' or 's' : Move Down")
    print("'A' or 'a' : Move Left")
    print("'D' or 'd' : Move Right\n\n\n")

    play_again_flag = 0
    while wanna_play.lower() == 'yes':
        
        display_board(mat , board)
        x = input("Press the command : ")
        if x.lower() == 'a':
            mat , flag = move_left(mat)
            status = get_current_state(mat) 
            print(status)
            if status == 'GAME NOT OVER!' and flag :
                mat = add_2(mat)
            elif status == "WON" or status == "LOST" :
                play_again_flag  = 1

        elif x.lower() == 'd':
            mat , flag = move_right(mat)
            status = get_current_state(mat) 
            print(status)
            if status == 'GAME NOT OVER!' and flag :
                mat = add_2(mat)
            elif status == "WON" or status == "LOST" :
                play_again_flag  = 1
                   
        elif x.lower() == 'w':
            mat , flag = move_up(mat)
            status = get_current_state(mat) 
            if status == 'GAME NOT OVER!' and flag :
                mat  = add_2(mat)
            elif status == "WON" or status == "LOST" :
                print(status)
                play_again_flag  = 1 

        elif x.lower() == 's':
            mat , flag = move_down(mat)
            status = get_current_state(mat) 
            print(status)
            if status == 'GAME NOT OVER!' and flag :
                mat = add_2(mat)
            elif status == "WON" or status == "LOST" :
                play_again_flag  = 1

        if status == 'WON':
            print("Great job ! You have won !")
        elif status == "LOST" :
            print("Oh no ! You have lost")

        if play_again_flag == 1:
            display_board(mat ,board)
            play_again= input ("DO YOU WANNA PLAY THIS GAME AGAIN ? (ENTER YES OR NO ) ")
            if play_again.lower().strip() == 'yes':
                status , mat , play_again_flag = None , [[0 for x in range(4)] for x in range(4)] , 0
                mat = add_2(mat)
                mat = add_2(mat)
                continue
            else :
                print("THAT'S COOL HAVE A GOOD ONE............")
                break

    else :
        print("THAT'S COOL HAVE A GOOD ONE............")
if __name__ == '__main__':
    main()