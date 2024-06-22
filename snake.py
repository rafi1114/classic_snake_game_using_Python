import pygame
from pygame.locals import *
import time #creating a time delay for the snake's movement
import random  #To generate random locations for the apple 

SIZE = 40

class blockade:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load("resources/blockade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.n = random.randint(1,4) #Number of blockades
        print("Number of blockades: ", self.n)
        self.lengths = [] #Initializing the length array
        self.x = []
        self.y = []
        for i in range(self.n):
            self.lengths.append(random.randint(2,4))
            self.x.append(random.randint(4,8)*SIZE)
            self.y.append(random.randint(4,8)*SIZE)

        # print("The Lengths of the blockades are ", self.lengths)

        # for i in range(len(self.x)):
        #     print("The starting position of x are: ", self.x[i])
        #     print("The starting position of y are: ", self.y[i])

        for i in range(self.n):
            self.case = random.randint(1, 3)
            for j in range(self.lengths[i]+1):
                if self.case == 1:
                    self.x.append(self.x[0] + j*SIZE)
                    self.y.append(self.y[0] + j*SIZE)
                if self.case == 2:
                    self.x.append(self.x[0] + j*SIZE)
                    self.y.append(self.y[0])
                if self.case == 3:
                    self.x.append(self.x[0])
                    self.y.append(self.y[0] + j*SIZE)
        # print(f"The x positions of blockade  are: ", self.x)
        # print(f"The y positions of blockade are: ", self.y)

    def blockade_length(self):
        for i in range(0, len(self.x)):
            self.surface.blit(self.image, (self.x[i], self.y[i])) #typical function for displaying the blockade

    def draw(self):
        self.blockade_length()
        pygame.display.flip() #Updates the display

                                            
                                        

class apple:
    def __init__(self, surface): #initiates the apple
        self.surface = surface #gets surface from the Game Class as input
        self.image = pygame.image.load("resources/apple.png").convert_alpha() #imports own image here
        self.image = pygame.transform.scale(self.image, (SIZE, 35)) #reshapes the image
        self.x = 40 #the x position of the first apple
        self.y = 40 #the y position of the first apple


    def draw(self): #displays the apple
        self.surface.blit(self.image, (self.x, self.y)) #typical function for displaying the apple
        pygame.display.flip() #Updates the display

    def move(self): #randomly moves the apple in the game
        self.x = random.randint(1,19)*SIZE 
        self.y = random.randint(1,14)*SIZE

class snake:
    def __init__(self, surface, block, background, length): #gets the surface, snake block, background, and length from Game Class

        #initiating all properties received from Game class

        self.surface = surface
        self.block = block
        self.background = background
        self.direction = 'down'
        self.length = length
        self.x = [40]*length
        self.y = [40]*length

    # Setting the directions 

    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'


    # Setting the snake motion where next block gets the previous block's coordinates

    def walk(self):
        for i in range(self.length-1, 0, -1): #We go backward from last block towards the head
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE       #Coordinates are of the top corners of the blocks 
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE    
        self.draw()

    def draw(self):    #to display the snake on the screen
        # Load the background image
        self.surface.blit(self.background, (0,0))
        for i in range(self.length):
            self.surface.blit(self.block, (self.x[i],self.y[i])) #show all the blocks via loop
        pygame.display.flip()

    def increase_length(self):  #increase the length and this length is used in the walk function
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def wall_crossing(self): 
        if self.x[0]< 0:
            self.x[0] = 800
        if self.y[0]< 0:
            self.y[0] = 600
        if self.x[0]> 800:
            self.x[0] = 0
        if self.y[0]> 600:
            self.y[0] = 0 


class Game: #most important
    def __init__(self): 
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake Game by Rafi Bin Dastagir")

        self.play_bg_music()

        self.surface = pygame.display.set_mode((800,600)) #this surface is used by snake and apple too

        block = pygame.image.load("resources/block2.png").convert_alpha() #imports block for snake, apple
        block = pygame.transform.scale(block, (SIZE,SIZE))

        self.background = pygame.image.load("resources/bg2.jpg").convert() #imports background, used by snake too
        self.background = pygame.transform.scale(self.background, (800, 600))

        self.length = 1
        self.block = block
        self.snake = snake(self.surface, self.block, self.background, self.length) #This is how we pass the details through Snake
        self.snake.draw() #Draw the snake
        self.apple = apple(self.surface) #passing details to apple
        self.apple.draw() #Draw the apple
        self.blockade = blockade(self.surface)
        self.blockade.draw() 



    def is_collision(self, x1, y1, x2, y2): #Any collision detection

        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False 
    
    
    def display_score(self): #display the score
        font = pygame.font.SysFont('arial', 30, bold=True)
        score = font.render(f"Score: {self.snake.length-1}", True, (255,255,255))
        self.surface.blit(score, (650,10))
    
    def play_bg_music(self):  #play bg music continuously
        pygame.mixer.music.load("resources/music.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.snake.walk()
        self.blockade.draw()
        self.apple.draw()
        
        self.display_score()
        pygame.display.flip()

        # Snake colliding with Apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound1 = pygame.mixer.Sound("resources/yay.wav")
            pygame.mixer.Sound.play(sound1)
            self.snake.increase_length()
            self.apple.move()
        
        #Apple colliding with Blockade
        for i in range(len(self.blockade.x)):
            if self.is_collision(self.blockade.x[i], self.blockade.y[i], self.apple.x, self.apple.y):
                self.apple.move()
        
        #Apple colliding with Snake's Body Parts
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.apple.move() 

        # Snake colliding with Itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound2 = pygame.mixer.Sound("resources/noo.mp3")
                pygame.mixer.Sound.play(sound2)
                raise "Colision detected"


        # Snake colliding with Blockade
        for i in range(len(self.blockade.x)):    
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.blockade.x[i], self.blockade.y[i]):
                    sound2 = pygame.mixer.Sound("resources/noo.mp3")
                    pygame.mixer.Sound.play(sound2)
                    raise "Colision detected"
        
        # Snake going out of bounds
        if self.snake.x[0] > 800 or self.snake.x[0] < 0 or self.snake.y[0] > 600 or self.snake.y[0] < 0:
            self.snake.wall_crossing()

                            
    def show_game_over(self):
        self.background = pygame.image.load("resources/bg2.jpg").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.surface.blit(self.background, (0,0)) 
        font = pygame.font.SysFont('impact', 40)
        line1 = font.render(f"Game OVER! Your Score is: {self.snake.length}", True, (255,155,0))
        self.surface.blit(line1, (150,200))
        line2 = font.render("To play the game again, hit ENTER!", True, (255,255,255))
        self.surface.blit(line2, (100,300))
        line3 = font.render("To exit press ESCAPE!", True, (255,255,255))
        self.surface.blit(line3, (200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()
    
    def reset(self):
        self.snake = snake(self.surface, self.block, self.background, 1)
        self.apple = apple(self.surface)
        self.blockade = blockade(self.surface)


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if pause == False:
                        if event.key == K_LEFT and self.snake.direction != 'right': #Cant go behind the body
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != 'left':
                            self.snake.move_right()
                        if event.key == K_UP and self.snake.direction != 'down':
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != 'up':
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_game_over()
                
                self.reset()

            time.sleep(0.2)

if __name__ == '__main__':
    game = Game()
    game.run()
