import copy
import sys
import pygame
import random
import numpy as np

from consts import *

# --- KONFIGURACJA PYGAME ---

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('KÓŁKO I KRZYŻYK AI')
screen.fill( BG_COLOUR )

# --- KLASY ---

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [kwadraty]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 jeśli jeszcze nie ma wygranej
            @return 1 jeśli gracz 1 wygrywa
            @return 2 jeśli gracz 2 wygrywa
        '''

        # wygrane pionowe
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    colour = CIRC_COLOUR if self.squares[0][col] == 2 else CROSS_COLOUR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, colour, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # wygrane poziome
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    colour = CIRC_COLOUR if self.squares[row][0] == 2 else CROSS_COLOUR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, colour, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # przekątna malejąca
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                colour = CIRC_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # przekątna rosnąca
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                colour = CIRC_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # jeszcze nie ma wygranej
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- LOSOWANIE ---

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (wiersz, kolumna)

    # --- MINIMAX ---

    def minimax(self, board, maximizing):
        
        # przypadek końcowy
        case = board.final_state()

        # gracz 1 wygrywa
        if case == 1:
            return 1, None # ocena, ruch

        # gracz 2 wygrywa
        if case == 2:
            return -1, None

        # remis
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- GŁÓWNA OCENA ---

    def eval(self, main_board):
        if self.level == 0:
            # losowy wybór
            eval = 'losowy'
            move = self.rnd(main_board)
        else:
            # wybór algorytmu minimax
            eval, move = self.minimax(main_board, False)

        print(f'AI wybrało pole w pozycji {move} z oceną: {eval}')

        return move # wiersz, kolumna

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1-krzyżyk  #2-kółko
        self.gamemode = 'ai' # pvp lub ai
        self.running = True
        self.show_lines()

    # --- METODY RYSOWANIA ---

    def show_lines(self):
        # tło
        screen.fill( BG_COLOUR )

        # pionowe
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # poziome
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # rysuj krzyżyk
            # linia malejąca
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_desc, end_desc, CROSS_WIDTH)
            # linia rosnąca
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.player == 2:
            # rysuj kółko
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOUR, center, RADIUS, CIRC_WIDTH)

    # --- INNE METODY ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # --- OBIEKTY ---

    game = Game()
    board = game.board
    ai = game.ai
    # --- GŁÓWNA PĘTLA ---

    while True:
        
        # zdarzenia pygame
        for event in pygame.event.get():

            # zdarzenie wyjścia
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # zdarzenie naciśnięcia klawisza
            if event.type == pygame.KEYDOWN:

                # g-zmiana trybu gry
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-losowy AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-minimax AI
                if event.key == pygame.K_1:
                    ai.level = 1

            # zdarzenie kliknięcia myszą
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                # ludzkie oznaczenie kwadratu
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    # sprawdzenie czy gra się skończyła
                    if game.isover():
                        game.running = False


        # początkowe wywołanie AI
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # aktualizacja ekranu
            pygame.display.update()

            # ocena
            row, col = ai.eval(board)
            game.make_move(row, col)

            # sprawdzenie czy gra się skończyła
            if game.isover():
                game.running = False
            
        pygame.display.update()

main()
