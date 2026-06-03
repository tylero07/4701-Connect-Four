"""All Meaningful AI Logic For The Game"""
import sys
import time
import math
import random
import pygame
from display import *
from GameControlLogic import *

def score_window(window, player):
    """Display Logic For the Score Window"""
    opponent = P2 if player == P1 else P1
    pc = window.count(player)
    ec = window.count(EMPTY)
    oc = window.count(opponent)
    if oc > 0:
        return 0
    if pc == 4: return 100
    if pc == 3 and ec == 1: return 5
    if pc == 2 and ec == 2: return 2
    return 0


def evaluate(board, player):
    """Win Condition Evaluations"""
    opponent = P2 if player == P1 else P1
    score = 0
    # Center column bonus
    center = [board[r][3] for r in range(ROWS)]
    score += center.count(player) * 3
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            w = [board[r][c+i] for i in range(4)]
            score += score_window(w, player) - score_window(w, opponent)
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            w = [board[r+i][c] for i in range(4)]
            score += score_window(w, player) - score_window(w, opponent)
    # Diagonal /
    for r in range(ROWS-3):
        for c in range(COLS-3):
            w = [board[r+i][c+i] for i in range(4)]
            score += score_window(w, player) - score_window(w, opponent)
    # Diagonal \
    for r in range(3, ROWS):
        for c in range(COLS-3):
            w = [board[r-i][c+i] for i in range(4)]
            score += score_window(w, player) - score_window(w, opponent)
    return score

# initialize sates explored to 0
states_explored = 0

def minimax(board, depth, alpha, beta, maximizing, ai_player, use_alpha_beta_prune):
    """Minimax Algorithm. Check the states and choose the least bad option avoiding the worse loss conditions"""
    global states_explored
    # internal tracker for the total states explored for the chart
    states_explored += 1
    # defines who is the opposition and who is the "mini" of the minimax
    opponent = P2 if ai_player == P1 else P1

    # sets the win/loss condition to overwhelming values
    # depth - 1 to help choose/avoid the shallowest win/loss <- good reccomandation by claude
    if check_win(board, ai_player):
        return 100000 + depth, -1
    if check_win(board, opponent):
        return -100000 - depth, -1

    moves = valid_moves(board)
    # board is full or hit search depth
    if not moves or depth == 0:
        return evaluate(board, ai_player), -1
    # resets best column to prevent locking or returning -1 when ties are found
    best_col = moves[0]
    # boolean recursively set Flag (True = "AIs" Turn | False = Opponents Turn) for logic in search
    if maximizing:
        # Starting with -infinity so any value will be greater than it setting the a start point
        best = -math.inf
        # Loops through columns to assess legal moves
        for col in moves:
            # board status, col, ai passed 
            row = drop(board, col, ai_player)
            # Recursive Search/Eval
            val, _ = minimax(board, depth-1, alpha, beta, False, ai_player, use_alpha_beta_prune)
            undrop(board, col, row) # I was locking the game with clunky logic this claude recommendation helped speed/clean things up
            if val > best:
                # Choosing the best option for your turn, if its better replace with col postition
                best, best_col = val, col
            if use_alpha_beta_prune:
                # alpha side logic involves only keeping the best path 
                # in practice significantly reduces explored states and increases game speed
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best, best_col
    else:
        # search the worst scenarios 
        # set best as infinity so any move initializes to a worst value
        best = math.inf
        for col in moves:
            row = drop(board, col, opponent)
            # Recursive Search/Evaluation
            val, _ = minimax(board, depth-1, alpha, beta, True, ai_player, use_alpha_beta_prune)
            # same as above work your way back
            undrop(board, col, row)
            # if the move is worse
            if val < best:
                # reset values, location
                best, best_col = val, col
            if use_alpha_beta_prune:
                # only search the values that give the least bad result
                beta = min(beta, best)
                if alpha >= beta:
                    break
        return best, best_col

"""Logic to Make AI/Opponent Move"""
def ai_move(board, player, depth, use_alpha_beta_prune):
    global states_explored
    states_explored = 0
    t0 = time.perf_counter()
    _, col = minimax(board, depth, -math.inf, math.inf, True, player, use_alpha_beta_prune)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    if col == -1:
        col = valid_moves(board)[0]
    return col, states_explored, elapsed_ms


"""Added on the backend from claude to create a csv to grab game data for the writeup"""
import csv
import os

CSV_FILE = "game_log.csv"

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Algorithm", "Depth", "Alpha-Beta", "Player", "States Explored", "Avg Time (ms)", "Outcome"])
            
def log_move(depth, use_ab, states, ms, outcome=None, player=""):
    label = f"Minimax {'w/ Alpha-Beta' if use_ab else 'no pruning'} depth {depth}"
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([label, depth, use_ab, player, states, f"{ms:.2f}", outcome or "in progress"])