from display import *

def new_board():
    return [[EMPTY]*COLS for _ in range(ROWS)]

def valid_moves(board):
    return [c for c in CENTER_ORDER if board[0][c] == EMPTY]

def drop(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = player
            return r
    return -1

def undrop(board, col, row):
    board[row][col] = EMPTY

def check_win(board, player):
    wins = []
    for r in range(ROWS):
        for c in range(COLS):
            if c+3 < COLS and all(board[r][c+i]==player for i in range(4)):
                wins.append([(r,c+i) for i in range(4)])
            if r+3 < ROWS and all(board[r+i][c]==player for i in range(4)):
                wins.append([(r+i,c) for i in range(4)])
            if r+3 < ROWS and c+3 < COLS and all(board[r+i][c+i]==player for i in range(4)):
                wins.append([(r+i,c+i) for i in range(4)])
            if r+3 < ROWS and c-3 >= 0 and all(board[r+i][c-i]==player for i in range(4)):
                wins.append([(r+i,c-i) for i in range(4)])
    return wins

def is_draw(board):
    return all(board[0][c] != EMPTY for c in range(COLS))