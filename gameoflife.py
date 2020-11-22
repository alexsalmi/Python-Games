import pygame as pygame
import numpy as np
import random 
import math  
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
green = (0, 255, 0)

class Display:
    def __init__(self):
        self.size = 45
        self.pix = 20
        self.width = self.size*self.pix
        self.height = self.size*self.pix
        self.grid = np.zeros((self.size,self.size))
        self.xoffset = 0
        self.yoffset = 100

    def randomize(self):
        for x in range(1, self.width//self.pix-1):
            for y in range(1, self.height//self.pix-1):
                if random.randint(1,4) == 1:
                    self.grid[x][y] = 1
                else:
                    self.grid[x][y] = 0


    def update_grid(self):
        grid_cpy = np.zeros((self.size,self.size))

        for x in range(1, (self.width//self.pix)-1):
            for y in range(1, (self.height//self.pix)-1):
                alive_nbrs = 0
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if (x != i or y != j) and (self.grid[i][j] == 1):
                            alive_nbrs += 1
                
                if self.grid[x][y] == 1:
                    if alive_nbrs < 2 or alive_nbrs > 3:
                        grid_cpy[x][y] = 0
                    else:
                        grid_cpy[x][y] = 1
                elif self.grid[x][y] == 0 and alive_nbrs == 3:
                    grid_cpy[x][y] = 1
        self.grid = grid_cpy

    
    def render(self, win):
        win.fill(grey)
        for x in range(self.width//self.pix):
            for y in range(self.height//self.pix):
                color = black
                if self.grid[x][y] == 1:
                    color = green
                pygame.draw.rect(win, color, (self.xoffset+x*self.pix, self.yoffset+y*self.pix, self.pix, self.pix))

class Game:
    def __init__(self):
        self.speed = 100
  
def main():
    disp = Display()
    game = Game()
    disp.randomize()

    font = pygame.font.Font('freesansbold.ttf', 28) 

    winWidth = disp.size*disp.pix + disp.xoffset
    winHeight = disp.size*disp.pix + disp.yoffset

    win = pygame.display.set_mode((winWidth, winHeight))

    pygame.display.set_caption("Game of Life")

    gen = 0

    run = True
    evolving = False
    while run:
        pygame.time.delay(game.speed)

        keys = pygame.key.get_pressed()
        if evolving == False and keys[pygame.K_r]:
            disp.randomize()
            gen = 0
        elif evolving == False and keys[pygame.K_RETURN]:
            evolving = True
        elif evolving == True and keys[pygame.K_RETURN]:
            evolving = False
        elif evolving == True:
            disp.update_grid()
            gen += 1

        disp.render(win)

        text = font.render('Generation ' + str(gen), True, white, grey) 
        textRect = text.get_rect()  
        textRect.center = (disp.size*disp.pix//2+disp.xoffset, disp.size) 
        win.blit(text, textRect) 

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


    gameOverFont = pygame.font.Font('freesansbold.ttf', 64) 
    text = gameOverFont.render('GAME OVER', True, white, black) 
    textRect = text.get_rect()  
    textRect.center = (disp.size*disp.pix//2+disp.xoffset, disp.size*disp.pix//2) 
    win.blit(text, textRect) 
    pygame.display.update()  
    pygame.time.delay(2000)

    pygame.quit()

main()