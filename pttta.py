import sys #umożliwia zamknięcie aplikacji za pomocą klawisza
import pygame #zewnętrzna biblioteka ułatwiajaca tworzenie gier

from consts import *
#Ustawienia Pygame
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toe')
screen.fill( BG_COLOUR )

#Kod Pygame
class Game: 
    def __init__(self):
        self.show_lines()
        
    def show_lines(self):
        #pionowe
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)

        #poziome

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