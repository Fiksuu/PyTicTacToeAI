import sys #umożliwia zamknięcie aplikacji za pomocą klawisza
import pygame #zewnętrzna biblioteka ułatwiajaca tworzenie gier

from consts import *
#Ustawienie Pygame
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Tic Tac Toe')
screen.fill( BG_COLOUR )

#Kod Pygame
def main():
    
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()    

main()