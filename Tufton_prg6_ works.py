from simplegraphics import *
import random

NUM_MINES= 10

def main ():
    board= []
    for i in range (8):
        board.append ([])
        for j in range (8):
            board[i].append(0)

    clicks= []
    for i in range (8):
        clicks.append ([])
        for j in range (8):
            clicks[i].append(0)


    open_canvas(400, 400)   
    set_background_color("gray")

       
    for i in range (0, 400, 50):
        draw_line (0,i, 400, i)
        draw_line (i,0,i,400)

    createMines(board, NUM_MINES)
    board = computeNumbers(board)

    
    print()

    for r in range(len(board)):
        for c in range(len(board[r])):
            print(format(board[r][c],"4d"), end='')
        print ()

    display_board(board,clicks)

    

    while noMines(board, clicks) and moreMoves(board, clicks):

        wait_for_click ()
        
        x= get_last_click_x ()
        y= get_last_click_y ()

        row= int (y//50)
        col= int(x//50)
        
        do_move(board,clicks,row,col)
        
        display_board(board,clicks)

        
    if not moreMoves(board, clicks):
        draw_string( "Winner!", 150,95,22)
            
    else:
        display_all_mines (board,clicks)

        
    wait_for_click()
    close_canvas()

  

def createMines(board, NUM_MINES):
    count= 0
    while count < NUM_MINES:
        row= random.randint(0,7)
        col= random.randint(0,7)
        if board [row][col] != -1:
            board [row][col] = -1
            count += 1


def display_board(board,clicks):
    for i in range (0, 400, 50):
        draw_line (0,i, 400, i)
        draw_line (i,0,i,400)

    for row in range(len(clicks)):
        for col in range(0,len(clicks[row])):
            if clicks[row][col] == 1:
                if board [row][col]== -1:
                    draw_image ("mine.gif", col*50+25, row*50+25)
                    
                elif board [row][col] == 0:
                    set_color("white")
                    draw_filled_rect(col*50,row*50,50, 50)
                    set_color("black")
                    draw_rect(col*50,row*50,50, 50)
  
                else:
                    text = str(board[row][col])
                    draw_string(text, col*50+25,row*50+25, 18)
    
                            

def display_all_mines(board, clicks):

    for row in range (len(board)):
        for col in range (len(board [row])):
            if board [row][col] == -1:
                draw_image ("mine.gif",col*50+25, row*50+25)
                
            elif clicks [row][col] == 1:
                if board [row][col] == 0:
                    set_color("white")
                    draw_filled_rect(col*50,row*50,50, 50)
                    set_color("black")
                    draw_rect(col*50,row*50,50, 50)
  
                else:
                    text = str(board[row][col])
                    draw_string(text, col*50+25,row*50+25, 18)
                
            

def moreMoves (board,clicks):
    for row in range (0, len(clicks)):
        for col in range(0,len(clicks [row])):
            if clicks [row][col] == 0 and board [row][col] != -1:
                return True
            
    return False


def noMines(board, clicks):
    for row in range (len(clicks)):
        for col in range (len(clicks [row])):

            if clicks [row][col] == 1 and board [row][col]== -1:
                return False

    return True 
                
 
#This function computes the correct number of mines that surround each square.
#If a mine is in the square, it remains a -1.
#This function expects that you pass in a 2-D list that has a -1 everywhere a mine is
#and a 0 otherwise. - DON'T CHANGE THIS FUNCTION
#parameters: board, a 2-D list with 0s and -1s
#returns: a 2-D list with either a -1, or the number of adjacent mines to that square
def computeNumbers(board):
    BOARD_SIZE = len(board)
    numBoard = []
    for i in range(len(board)):
        numBoard.append([])
        for j in range(len(board[i])):
            numBoard[i].append(0)
    for r in range(len(board)):
        for c in range(len(board[r])):
            if(board[r][c] == -1):
                numBoard[r][c] = -1
                continue
            if 0 < r < BOARD_SIZE-1 and 0 < c < BOARD_SIZE-1:
                totalMines = board[r-1][c-1] + board[r-1][c] + board[r-1][c+1] +\
                             board[r][c-1] + board[r][c+1] + board[r+1][c-1] + \
                             board[r+1][c] + board[r+1][c+1]
            elif 0 < r < BOARD_SIZE-1:
                if c-1 < 0:
                    totalMines =  board[r-1][c] + board[r-1][c+1] + \
                                 board[r][c+1] + board[r+1][c] + board[r+1][c+1]
                elif c+1 >= BOARD_SIZE:
                    totalMines =  board[r-1][c-1] + board[r-1][c] + \
                                 board[r][c-1] + board[r+1][c-1] + board[r+1][c]                    
            elif 0 < c < BOARD_SIZE-1:
                if r-1 < 0:
                    totalMines = board[r][c-1] + board[r][c+1] + board[r+1][c-1] + \
                                board[r+1][c] + board[r+1][c+1]
                elif r+1 >= BOARD_SIZE:
                    totalMines = board[r-1][c-1] + board[r-1][c] + board[r-1][c+1] + \
                                board[r][c-1] + board[r][c+1]
            elif r <= 0 and c <= 0:
                totalMines = board[r][c+1] + board[r+1][c] + board[r+1][c+1]
            elif r+1 == BOARD_SIZE and c <= 0:
                totalMines = board[r-1][c] + board[r-1][c+1] + board[r][c+1]
            elif r+1 == BOARD_SIZE and c+1 == BOARD_SIZE:
                totalMines = board[r-1][c-1] + board[r-1][c] + board[r][c-1]
            elif r <= 0 and c+1 == BOARD_SIZE:
                totalMines = board[r][c-1]+ board[r+1][c-1] + board[r+1][c]
            numBoard[r][c] = totalMines * -1
                  
    return numBoard

#This function will update the clicks list to show that a square has been clicked
#It will also call its helper function fill_in_move, so that surrounding blocks
#can be uncovered as well if they should be - DON'T CHANGE THIS CODE
#An uncovered square will be marked with a 1, otherwise, it will remain a 0
def do_move(board, clicks, r, c):
    if board[r][c] == 0:
        fill_in_move(board, clicks, r, c)
    else:
        clicks[r][c] = 1

#Helper function for do_move - DON'T CHANGE THIS CODE    
def fill_in_move(board, clicks, r, c):
    if r < 0 or r >= len(board) or c < 0 or c >= len(board):
        return
    if clicks[r][c] == 1:
        return
    if 0 <= r < len(board) and 0 <= c < len(board):
        if board[r][c] != -1:
            clicks[r][c] = 1
            if board[r][c] == 0:
                fill_in_move(board, clicks, r-1, c-1)
                fill_in_move(board, clicks, r-1, c)
                fill_in_move(board, clicks, r-1, c+1)
                fill_in_move(board, clicks, r, c-1)
                fill_in_move(board, clicks, r, c+1)
                fill_in_move(board, clicks, r+1, c-1)
                fill_in_move(board, clicks, r+1, c)
                fill_in_move(board, clicks, r+1, c+1)

main ()





