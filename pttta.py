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
    
        

class Game: 
    def __init__(self):
        self.board
        self.show_lines()
        
    def show_lines(self):
        #pionowe
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        #poziome
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)


def main():

    #objekt
    game = Game()
    
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()    

main()