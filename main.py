"""
Connect Four — CS470/570 Project #2
Minimax with Alpha-Beta Pruning, pygame graphics
Controls: click a column to drop a piece, or watch AI vs AI
"""

import sys
import time
import math
import random
import pygame
from display import *
from GameControlLogic import *
from ai_logic_algos import *


# ─── Evaluation heuristic ────────────────────────────────────────────────────
def score_window(window, player):
    opp = P2 if player == P1 else P1
    pc = window.count(player)
    ec = window.count(EMPTY)
    oc = window.count(opp)
    if oc > 0:
        return 0
    if pc == 4: return 100
    if pc == 3 and ec == 1: return 5
    if pc == 2 and ec == 2: return 2
    return 0

def evaluate(board, player):
    opp = P2 if player == P1 else P1
    score = 0
    # Center column bonus
    center = [board[r][3] for r in range(ROWS)]
    score += center.count(player) * 3
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            w = [board[r][c+i] for i in range(4)]
            score += score_window(w, player) - score_window(w, opp)
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            w = [board[r+i][c] for i in range(4)]
            score += score_window(w, player) - score_window(w, opp)
    # Diagonal /
    for r in range(ROWS-3):
        for c in range(COLS-3):
            w = [board[r+i][c+i] for i in range(4)]
            score += score_window(w, player) - score_window(w, opp)
    # Diagonal \
    for r in range(3, ROWS):
        for c in range(COLS-3):
            w = [board[r-i][c+i] for i in range(4)]
            score += score_window(w, player) - score_window(w, opp)
    return score

# ─── Minimax with optional alpha-beta ────────────────────────────────────────
states_explored = 0

def minimax(board, depth, alpha, beta, maximizing, ai_player, use_ab):
    global states_explored
    states_explored += 1
    opp = P2 if ai_player == P1 else P1

    if check_win(board, ai_player):
        return 100000 + depth, -1
    if check_win(board, opp):
        return -100000 - depth, -1
    moves = valid_moves(board)
    if not moves or depth == 0:
        return evaluate(board, ai_player), -1

    best_col = moves[0]
    if maximizing:
        best = -math.inf
        for col in moves:
            row = drop(board, col, ai_player)
            val, _ = minimax(board, depth-1, alpha, beta, False, ai_player, use_ab)
            undrop(board, col, row)
            if val > best:
                best, best_col = val, col
            if use_ab:
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best, best_col
    else:
        best = math.inf
        for col in moves:
            row = drop(board, col, opp)
            val, _ = minimax(board, depth-1, alpha, beta, True, ai_player, use_ab)
            undrop(board, col, row)
            if val < best:
                best, best_col = val, col
            if use_ab:
                beta = min(beta, best)
                if alpha >= beta:
                    break
        return best, best_col

def ai_move(board, player, depth, use_ab):
    global states_explored
    states_explored = 0
    t0 = time.perf_counter()
    _, col = minimax(board, depth, -math.inf, math.inf, True, player, use_ab)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    if col == -1:
        col = valid_moves(board)[0]
    return col, states_explored, elapsed_ms


if __name__ == '__main__':
    main()