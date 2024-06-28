import copy
import sys
import pygame
import random
import numpy as np

from consts import *

# --- KONFIGURACJA PYGAME ---

# Inicjalizacja biblioteki Pygame
pygame.init()
# Ustawienie rozmiaru okna gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Ustawienie tytułu okna gry
pygame.display.set_caption('KÓŁKO I KRZYŻYK AI')
# Wypełnienie tła okna gry kolorem
screen.fill( BG_COLOUR )

# --- KLASY ---

# Klasa reprezentująca planszę gry
class Board:
    # Konstruktor klasy
    def __init__(self):
        # Inicjalizacja planszy jako macierzy zer
        self.squares = np.zeros((ROWS, COLS))
        # Lista pustych kwadratów (na początku wszystkie)
        self.empty_sqrs = self.squares
        # Licznik zaznaczonych kwadratów
        self.marked_sqrs = 0

    # Metoda sprawdzająca stan końcowy gry
    def final_state(self, show=False):
        # Sprawdzenie warunków wygranej dla obu graczy oraz remisu
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

# Metoda zaznaczająca kwadrat przez gracza
    def mark_sqr(self, row, col, player):
        # Zaznaczenie kwadratu w macierzy planszy
        self.squares[row][col] = player
        # Inkrementacja licznika zaznaczonych kwadratów
        self.marked_sqrs += 1

    # Metoda sprawdzająca czy kwadrat jest pusty
    def empty_sqr(self, row, col):
        # Zwraca True jeśli kwadrat jest pusty
        return self.squares[row][col] == 0

    # Metoda zwracająca listę pustych kwadratów
    def get_empty_sqrs(self):
        # Zwraca listę pustych kwadratów
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    # Metoda sprawdzająca czy plansza jest pełna
    def isfull(self):
        # Zwraca True jeśli wszystkie kwadraty są zaznaczone
        return self.marked_sqrs == 9

    # Metoda sprawdzająca czy plansza jest pusta
    def isempty(self):
        # Zwraca True jeśli żaden kwadrat nie jest zaznaczony
        return self.marked_sqrs == 0

# Klasa reprezentująca sztuczną inteligencję
class AI:
    # Konstruktor klasy
    def __init__(self, level=1, player=2):
        # Poziom trudności AI
        self.level = level
        # Numer gracza AI
        self.player = player

    # --- LOSOWANIE ---

    # Metoda losowego wyboru ruchu przez AI
    def rnd(self, board):
        # Losowy wybór pustego kwadratu
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (wiersz, kolumna)

    # --- MINIMAX ---

    # Metoda algorytmu minimax
    def minimax(self, board, maximizing):
        # Implementacja algorytmu minimax
        
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

    # Metoda oceny ruchu przez AI
    def eval(self, main_board):
        # Wybór ruchu na podstawie poziomu trudności
        if self.level == 0:
            # losowy wybór
            eval = 'losowy'
            move = self.rnd(main_board)
        else:
            # wybór algorytmu minimax
            eval, move = self.minimax(main_board, False)

        print(f'AI wybrało pole w pozycji {move} z oceną: {eval}')

        return move # wiersz, kolumna

# Klasa reprezentująca grę
class Game:
    # Konstruktor klasy
    def __init__(self):
        # Inicjalizacja planszy i AI
        self.board = Board()
        self.ai = AI()
        # Ustawienie gracza rozpoczynającego grę
        self.player = 1   # 1-krzyżyk  # 2-kółko
        # Tryb gry: przeciwko AI lub gracz przeciwko graczowi
        self.gamemode = 'ai'
        # Stan gry: trwa lub zakończona
        self.running = True
        # Wyświetlenie linii podziału planszy
        self.show_lines()

    # --- METODY RYSOWANIA ELEMENTÓW NA PLANSZY---

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

    # Metoda wykonująca ruch
    def make_move(self, row, col):
        # Zaznaczenie kwadratu i narysowanie figury
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    # Metoda zmieniająca tury graczy
    def next_turn(self):
        # Przełączenie tury na drugiego gracza
        self.player = self.player % 2 + 1

    # Metoda zmieniająca tryb gry
    def change_gamemode(self):
        # Przełączenie między trybem AI a PvP
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    # Metoda sprawdzająca czy gra się zakończyła
    def isover(self):
        # Sprawdzenie czy jest stan końcowy lub plansza pełna
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    # Metoda resetująca grę
    def reset(self):
        # Reset gry do stanu początkowego
        self.__init__()

    # --- OBIEKTY ---

    # Główna funkcja gry
def main():
    # Inicjalizacja gry i jej komponentów
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
