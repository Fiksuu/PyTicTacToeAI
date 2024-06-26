import sys #umożliwia zamknięcie aplikacji za pomocą klawisza
import pygame #zewnętrzna biblioteka ułatwiajaca tworzenie gier
import numpy as np #zewnętrzna biblioteka do tworzenia tablic

from consts import *
#Ustawienia Pygame
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toe')
screen.fill( BG_COLOUR )

#Kod Pygame
class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

class Game: 
    def __init__(self):
        self.board = Board()
        self.player = 1 #gracz 1 - krzyżyk || gracz 2 - kółko
        self.show_lines()
        
    def show_lines(self):
        #pionowe linie
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        #poziome linie
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            #krzyżyk
            pass

        elif self.player == 2:
            #kółko
            center = ()
            pygame.draw.circle(screen, CIRC_COLOUR, center, RADIUS, CIRC_WIDTH)
        
        #zmiana gracza
    def next_player(self):
        self.player = self.player % 2 + 1


def main():

    #objekt
    game = Game()
    board = game.board


    #główna pętla
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #wykrywanie kliknięć na planszy
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_player()
                    
                

        pygame.display.update()    

main()