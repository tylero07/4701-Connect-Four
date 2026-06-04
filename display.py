"""Holds All The Data And Settings For Drawing/Rendering Pygame Needs"""
import pygame

ROWS, COLS = 6, 7
SQUARESIZE = 90
RADIUS     = SQUARESIZE // 2 - 6
WIDTH      = COLS * SQUARESIZE
HEIGHT     = (ROWS + 1) * SQUARESIZE   # +1 row for the drop-preview area
PANEL_W    = 280
WIN_W      = WIDTH + PANEL_W
EMPTY, P1, P2 = 0, 1, 2

FPS = 60

"""Color Palate Definition Contstants"""
BOARD_BG   = (26,  58, 107)
BOARD_EDGE = (18,  45,  84)
EMPTY_C    = (10,  32,  68)
P1_C       = (230, 57,  70)
P1_LIGHT   = (255, 107, 122)
P2_C       = (244, 208, 63)
P2_LIGHT   = (249, 232, 127)
BG         = (15,  25,  45)
TEXT_C     = (220, 220, 220)
MUTED_C    = (140, 140, 160)
WHITE      = (255, 255, 255)
GREEN      = (50,  200, 100)
DARK_GREEN = (30,  140,  60)
WIN_GLOW   = (255, 255, 100)

"""This is critical for making the heuristic work
    The columns are ordered by their values 3 (middle) being the best play and alternating out
    to the ends (0 and 6) being the least valuable"""
CENTER_ORDER = [3, 2, 4, 1, 5, 0, 6]

def draw_board(screen, board, win_cells=None, hover_col=None, current_player=None):
    """Draw Game Setting the size borders Color Game Space/Shapes/visuals Palate Etc (All Non Alpha Numerics For the Display)"""
    # Background
    screen.fill(BG)

    # Board body
    pygame.draw.rect(screen, BOARD_BG, (0, SQUARESIZE, WIDTH, ROWS*SQUARESIZE), border_radius=12)
    pygame.draw.rect(screen, BOARD_EDGE, (0, SQUARESIZE, WIDTH, ROWS*SQUARESIZE), 3, border_radius=12)

    # Column hover highlight
    if hover_col is not None and 0 <= hover_col < COLS:
        hover_rect = pygame.Rect(hover_col*SQUARESIZE, SQUARESIZE, SQUARESIZE, ROWS*SQUARESIZE)
        pygame.draw.rect(screen, (255,255,255,25), hover_rect)

    # Cells
    for r in range(ROWS):
        for c in range(COLS):
            cx = c*SQUARESIZE + SQUARESIZE//2
            cy = (r+1)*SQUARESIZE + SQUARESIZE//2
            # Shadow hole
            pygame.draw.circle(screen, EMPTY_C, (cx, cy), RADIUS)
            pygame.draw.circle(screen, (0,0,0), (cx, cy+3), RADIUS, 3)

            p = board[r][c]
            if p == P1:
                color = P1_C
                light = P1_LIGHT
            elif p == P2:
                color = P2_C
                light = P2_LIGHT
            else:
                continue

            if win_cells and (r,c) in win_cells:
                # Pulsing highlight — alternate each frame via a glow ring
                pygame.draw.circle(screen, WIN_GLOW, (cx, cy), RADIUS+4)
            pygame.draw.circle(screen, color, (cx, cy), RADIUS)
            pygame.draw.circle(screen, light, (cx-RADIUS//4, cy-RADIUS//4), RADIUS//4)

    # Drop-preview row
    if hover_col is not None and current_player is not None:
        cx = hover_col*SQUARESIZE + SQUARESIZE//2
        cy = SQUARESIZE//2
        color = P1_C if current_player == P1 else P2_C
        pygame.draw.circle(screen, color, (cx, cy), RADIUS, 3)

def draw_panel(screen, font_b, font, font_s, game_state):
    """Initialize and Set all Text And Descriptors For The Game"""
    px = WIDTH + 14
    y = 18

    def txt(text, f, color, x=None, center=False):
        nonlocal y
        surf = f.render(text, True, color)
        rx = x if x else px
        if center:
            rx = WIDTH + (PANEL_W - surf.get_width()) // 2
        screen.blit(surf, (rx, y))
        y += surf.get_height() + 5

    txt("CONNECT FOUR", font_b, WHITE, center=True)
    y += 4

    # Mode
    mode_label = "Human vs AI" if game_state['mode']=='hvai' else "AI vs AI"
    txt(f"Mode: {mode_label}", font_s, MUTED_C, center=True)
    y += 6

    # Current player indicator
    p = game_state['current_player']
    p_color = P1_C if p == P1 else P2_C
    p_name = ("Red" if p==P1 else "Yellow")
    who = ""
    if game_state['mode'] == 'hvai':
        who = " (You)" if p == (P1 if game_state['human_first'] else P2) else " (AI)"
    label = f"{p_name}{who}'s turn"
    if game_state.get('game_over'):
        label = game_state.get('end_msg','Game over')

    surf = font_b.render(label, True, p_color if not game_state.get('game_over') else WHITE)
    screen.blit(surf, (WIDTH + (PANEL_W - surf.get_width())//2, y))
    y += surf.get_height() + 12

    if game_state.get('thinking'):
        txt("AI thinking...", font_s, P2_C, center=True)

    y += 6
    # Settings
    sep_y = y
    pygame.draw.line(screen, (50,60,80), (px-4, sep_y), (px+PANEL_W-20, sep_y))
    y += 8
    txt("SETTINGS", font_s, MUTED_C, center=True)
    y += 4

    depth = game_state['depth']
    ab = game_state['use_ab']
    txt(f"Depth: {depth}   (Arrow UP/DOWN to change)", font_s, TEXT_C, center=True)
    ab_color = GREEN if ab else (200,80,80)
    txt(f"Alpha-Beta: {'ON' if ab else 'OFF'}   (A to toggle)", font_s, ab_color, center=True)
    y += 4

    mode_c = GREEN if game_state['mode']=='hvai' else P2_C
    txt("M: toggle mode    R: restart", font_s, MUTED_C, center=True)
    y += 4
    if game_state['mode']=='hvai':
        txt("F: toggle first/second", font_s, MUTED_C, center=True)

    # Stats table
    y += 8
    pygame.draw.line(screen, (50,60,80), (px-4, y), (px+PANEL_W-20, y))
    y += 8
    txt("STATS (avg per move)", font_s, MUTED_C, center=True)
    y += 2

    stats = game_state.get('stats', [])
    if not stats:
        txt("No moves yet", font_s, (80,90,110), center=True)
    else:
        headers = ["Algorithm", "States", "ms"]
        col_w = [110, 70, 50]
        xs = [px, px+col_w[0], px+col_w[0]+col_w[1]]
        for i,h in enumerate(headers):
            s = font_s.render(h, True, MUTED_C)
            screen.blit(s, (xs[i], y))
        y += 18
        pygame.draw.line(screen, (50,60,80), (px-4, y), (px+PANEL_W-20, y))
        y += 4
        for row in stats[-6:]:  # last 6 rows
            cells = [row['label'], f"{row['avg_states']:,}", f"{row['avg_ms']:.0f}"]
            for i,c in enumerate(cells):
                s = font_s.render(c, True, TEXT_C)
                screen.blit(s, (xs[i], y))
            y += 17

    # Controls reminder at bottom
    ctrl_y = HEIGHT - 26
    ctrl = font_s.render("Q: quit", True, (60,70,90))
    screen.blit(ctrl, (WIDTH + (PANEL_W - ctrl.get_width())//2, ctrl_y))

def update_stats(stats, depth, use_ab, n_states, ms):
    label = f"MM {'αβ' if use_ab else '  '} d={depth}"
    row = next((r for r in stats if r['label']==label), None)
    if row is None:
        row = {'label': label, 'states': [], 'ms_list': [], 'avg_states': 0, 'avg_ms': 0}
        stats.append(row)
    row['states'].append(n_states)
    row['ms_list'].append(ms)
    row['avg_states'] = sum(row['states']) // len(row['states'])
    row['avg_ms'] = sum(row['ms_list']) / len(row['ms_list'])