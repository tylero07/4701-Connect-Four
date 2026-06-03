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
from AIandTurnLogic import *


def main():
    pygame.init()
    init_csv()
    screen = pygame.display.set_mode((WIN_W, HEIGHT))
    pygame.display.set_caption("Connect Four — CS470/570")
    clock = pygame.time.Clock()

    font_b = pygame.font.SysFont("Arial", 16, bold=True)
    font   = pygame.font.SysFont("Arial", 15)
    font_s = pygame.font.SysFont("Arial", 13)

    # Game state
    gs = {
        'board': new_board(),
        'current_player': P1,
        'game_over': False,
        'mode': 'hvai',       # 'hvai' or 'aivai'
        'human_first': True,
        'depth': 5,
        'use_ab': True,
        'thinking': False,
        'win_cells': set(),
        'end_msg': '',
        'stats': [],
        'hover_col': None,
        'total_states': {P1: 0, P2: 0},
        'move_times': {P1: [], P2: []},
    }
    # reset game state
    def reset():
        gs['board'] = new_board()
        gs['current_player'] = P1
        gs['game_over'] = False
        gs['thinking'] = False
        gs['win_cells'] = set()
        gs['end_msg'] = ''
        gs['hover_col'] = None
        gs['total_states'] = {P1: 0, P2: 0}
        gs['move_times'] = {P1: [], P2: []}
    
    # Define player AnD Moves
    def human_player():
        return P1 if gs['human_first'] else P2

    def is_ai_turn():
        if gs['mode'] == 'aivai':
            return True
        return gs['current_player'] != human_player()

    def do_ai_move():
        if gs['game_over']:
            return
        col, n_states, ms = ai_move(gs['board'], gs['current_player'], gs['depth'], gs['use_ab'])
        update_stats(gs['stats'], gs['depth'], gs['use_ab'], n_states, ms)

        p = gs['current_player']
        gs['total_states'][p] += n_states
        gs['move_times'][p].append(ms)

        row = drop(gs['board'], col, p)
        wins = check_win(gs['board'], p)
        if wins:
            gs['game_over'] = True
            gs['win_cells'] = set(pt for w in wins for pt in w)
            who = "Red" if p == P1 else "Yellow"
            gs['end_msg'] = f"{who} wins! (R to restart)"
            for player, label in [(P1, "Red"), (P2, "Yellow")]:
                avg_ms = sum(gs['move_times'][player]) / len(gs['move_times'][player]) if gs['move_times'][player] else 0
                log_move(gs['depth'], gs['use_ab'], gs['total_states'][player], avg_ms, outcome=f"{who} wins", player=label)
        elif is_draw(gs['board']):
            gs['game_over'] = True
            gs['end_msg'] = "Draw! (R to restart)"
            for player, label in [(P1, "Red"), (P2, "Yellow")]:
                avg_ms = sum(gs['move_times'][player]) / len(gs['move_times'][player]) if gs['move_times'][player] else 0
                log_move(gs['depth'], gs['use_ab'], gs['total_states'][player], avg_ms, outcome="Draw", player=label)
        else:
            gs['current_player'] = P2 if p == P1 else P1
        gs['thinking'] = False

    win_pulse = 0
    ai_delay_frames = 0
    # game logic sets frames and enum for keypress and click logic for 'buttons'
    while True:
        clock.tick(FPS)
        win_pulse = (win_pulse + 1) % 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_a:
                    gs['use_ab'] = not gs['use_ab']
                if event.key == pygame.K_UP:
                    gs['depth'] = min(9, gs['depth']+1)
                if event.key == pygame.K_DOWN:
                    gs['depth'] = max(1, gs['depth']-1)
                if event.key == pygame.K_m:
                    gs['mode'] = 'aivai' if gs['mode']=='hvai' else 'hvai'
                    reset()
                if event.key == pygame.K_f and gs['mode']=='hvai':
                    gs['human_first'] = not gs['human_first']
                    reset()

            if event.type == pygame.MOUSEMOTION:
                mx, _ = event.pos
                if mx < WIDTH:
                    gs['hover_col'] = mx // SQUARESIZE
                else:
                    gs['hover_col'] = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gs['game_over'] or gs['thinking']:
                    continue
                if gs['mode'] == 'hvai' and not is_ai_turn():
                    mx, my = event.pos
                    if mx < WIDTH and my > SQUARESIZE:
                        col = mx // SQUARESIZE
                        if col in valid_moves(gs['board']):
                            row = drop(gs['board'], col, gs['current_player'])
                            wins = check_win(gs['board'], gs['current_player'])
                            if wins:
                                gs['game_over'] = True
                                gs['win_cells'] = set(p for w in wins for p in w)
                                gs['end_msg'] = "You win! 🎉 (R to restart)"
                            elif is_draw(gs['board']):
                                gs['game_over'] = True
                                gs['end_msg'] = "Draw! (R to restart)"
                            else:
                                gs['current_player'] = P2 if gs['current_player']==P1 else P1
                                gs['thinking'] = True
                                ai_delay_frames = 8

        # Trigger AI move after a short delay
        if gs['thinking'] and not gs['game_over']:
            ai_delay_frames -= 1
            if ai_delay_frames <= 0:
                do_ai_move()

        # AI vs AI: schedule next move
        if gs['mode']=='aivai' and not gs['game_over'] and not gs['thinking']:
            gs['thinking'] = True
            ai_delay_frames = 20

        # Draw win pulse (toggle visibility)
        active_win_cells = gs['win_cells'] if win_pulse < 20 else set()

        draw_board(screen, gs['board'],
                   win_cells=active_win_cells,
                   hover_col=gs['hover_col'] if not is_ai_turn() else None,
                   current_player=gs['current_player'] if not gs['game_over'] else None)

        # Panel background
        pygame.draw.rect(screen, (18, 28, 48), (WIDTH, 0, PANEL_W, HEIGHT))
        pygame.draw.line(screen, (40,55,80), (WIDTH, 0), (WIDTH, HEIGHT), 2)

        draw_panel(screen, font_b, font, font_s, gs)
        pygame.display.flip()

if __name__ == '__main__':
    main()