import pygame as pygame
import numpy as np
import random 
import math  
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Display:
    def __init__(self):
        self.size = 30
        self.pix = 20
        self.width = self.size*self.pix
        self.height = self.size*self.pix
        self.grid = np.zeros((self.size,self.size, 3))
        self.xoffset = 0
        self.yoffset = 0

    def update_grid(self, snake, apple):
        for x in range(self.width//self.pix):
            for y in range(self.height//self.pix):
                if snake.x == x and snake.y == y:
                    self.grid[x][y] = red
                elif apple.x == x and apple.y == y:
                    self.grid[x][y] = green
                else:
                    self.grid[x][y] = black

        for i in range(len(snake.tail)):
            self.grid[snake.tail[i][0]][snake.tail[i][1]] = red
    
    def render(self, win):
        win.fill(grey)
        for x in range(self.width//self.pix):
            for y in range(self.height//self.pix):
                pygame.draw.rect(win, self.grid[x][y], (self.xoffset+x*self.pix, y*self.pix, self.pix, self.pix))

class Snake:
    def __init__(self, disp):
        self.x = disp.size//2
        self.y = disp.size//2
        self.tail = []
        self.length = 3
        self.direction = 'none'
        self.vel = 100
        self.acc = 1.2
    
    def move(self):
        if self.direction == 'none':
            return
            
        self.tail.append([self.x, self.y])
        if len(self.tail) > self.length:
            self.tail = self.tail[1:]

        if self.direction == 'up':
            self.y -= 1
        if self.direction == 'down':
            self.y += 1
        if self.direction == 'right':
            self.x += 1
        if self.direction == 'left':
            self.x -= 1
    
    def get_status(self, apple, disp):
        if self.x == disp.size or self.x < 0 or self.y == disp.size or self.y < 0:
            return -1
        
        for item in self.tail:
            if self.x == item[0] and self.y == item[1]:
                return -1
        
        if self.x == apple.x and self.y == apple.y:
            self.length += 1
            return 1

        return 0


class Apple:
    def __init__(self, disp):
        self.move(disp)

    def move(self, disp):
        self.x = int(random.random()*disp.size)
        self.y = int(random.random()*disp.size)
        while not np.array_equal(disp.grid[self.x][self.y], black):
            self.x = int(random.random()*disp.size)
            self.y = int(random.random()*disp.size)
    
def main():
    disp = Display()
    snake = Snake(disp)
    apple = Apple(disp)

    font = pygame.font.Font('freesansbold.ttf', 28) 

    winWidth = disp.size*disp.pix + disp.xoffset
    winHeight = disp.size*disp.pix + disp.yoffset

    win = pygame.display.set_mode((winWidth, winHeight))

    pygame.display.set_caption("Snake")

    points = 0

    run = True
    while run:
        pygame.time.delay(snake.vel)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake.direction != 'right':
            snake.direction = 'left'
        if keys[pygame.K_RIGHT] and snake.direction != 'left':
            snake.direction = 'right'
        if keys[pygame.K_UP] and snake.direction != 'down':
            snake.direction = 'up'
        if keys[pygame.K_DOWN] and snake.direction != 'up':
            snake.direction = 'down'

        snake.move()

        status = snake.get_status(apple, disp)

        if status == 1:
            apple.move(disp)
            points += 1
            if points%5 == 0:
                snake.vel = int(snake.vel//snake.acc)
        if status == -1:
            run = False
            break

        disp.update_grid(snake, apple)
        disp.render(win)

        text = font.render('Points: ' + str(points), True, white, black) 
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