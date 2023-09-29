from typing import Any
import pygame
import random
from sys import exit

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Snake Animations
        self.snakeHeadRight = pygame.image.load('Art/Snake/SnakeHead.png').convert_alpha()
        self.snakeHeadLeft = pygame.transform.rotate(self.snakeHeadRight, 180)
        self.snakeHeadUp = pygame.transform.rotate(self.snakeHeadRight, 90)
        self.snakeHeadDown = pygame.transform.rotate(self.snakeHeadRight, -90)
        
        self.snakeTailRight = pygame.image.load('Art/Snake/SnakeTail.png').convert_alpha()
        self.snakeTailLeft = pygame.transform.rotate(self.snakeTailRight, 180)
        self.snakeTailUp = pygame.transform.rotate(self.snakeTailRight, 90)
        self.snakeTailDown = pygame.transform.rotate(self.snakeTailRight, -90)       

        self.snakeBodyRight = pygame.image.load('Art/Snake/SnakeBody.png').convert_alpha()
        self.snakeBodyLeft = pygame.transform.rotate(self.snakeBodyRight, 180)
        self.snakeBodyUp = pygame.transform.rotate(self.snakeBodyRight, 90)
        self.snakeBodyDown = pygame.transform.rotate(self.snakeBodyRight, -90)         

        self.snakeUpturnRight = pygame.image.load('Art/Snake/SnakeUpturn.png').convert_alpha()
        self.snakeUpturnLeft = pygame.transform.rotate(self.snakeUpturnRight, 180)
        self.snakeUpturnUp = pygame.transform.rotate(self.snakeUpturnRight, 90)
        self.snakeUpturnDown = pygame.transform.rotate(self.snakeUpturnRight, -90)   
     
        self.snakeDownturnRight = pygame.image.load('Art/Snake/SnakeDownturn.png').convert_alpha()
        self.snakeDownturnLeft = pygame.transform.rotate(self.snakeDownturnRight, 180)
        self.snakeDownturnUp = pygame.transform.rotate(self.snakeDownturnRight, 90)
        self.snakeDownturnDown = pygame.transform.rotate(self.snakeDownturnRight, -90)   

        self.initialPosition = (128,256)
        self.position = self.initialPosition
        
        self.initialDirection = right
        self.direction = self.initialDirection        
        self.pendingDirection = self.initialDirection
        
        self.body = [self.position,
                     (self.position[0] - gridLength, self.position[1]),
                     (self.position[0] - 2 * gridLength, self.position[1])]
        
        self.snakeMoveDelay = 0.20    
        
    def update(self): 
        xPos, yPos = self.position
        xDir, yDir = self.direction
        
        xUpdate = xPos + xDir * gridLength
        yUpdate = yPos + yDir * gridLength
        
        self.position = (xUpdate, yUpdate)

        if self.direction != self.pendingDirection:
            self.direction = self.pendingDirection
        
        if len(self.body) > 0:
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i] = self.body[i - 1]
            self.body[0] = self.position
                      
    def eatFood(self):
        self.body.append(self.body[-1])
        self.snakeMoveDelay -= 0.003 #Change this to 0 when simulating
        self.update() #So that the tail is rendered instantly!    

# NOTE: pendingDirection was introduced to avoid the snake making a 180 and instead of a
#       u-turn when two keys are pressed in rapid succession. This works because the update()
#       method is not running at 60fps but your inputs are. So as soon as you press a key, the
#       pending direction is instantaneously changed, but the update() method still hasn't 
#       updated to the new direction because of the different frame rate.
#       Assume your snake is going right, your direction is (-1,0) 
#       Now suppose you press up and left rapidly. This changes your pending direction to up,
#       but it cant change it to left because your current direction (self.direction) going right
#       and so the if statement below blocks it from happening. So the snake safely goes up. But now
#       that it's going up, the left-control is registered and your snake can instantly turn left.

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.direction != down:
            self.pendingDirection = up    
        if keys[pygame.K_DOWN] and self.direction != up:
            self.pendingDirection = down          
        if keys[pygame.K_LEFT] and self.direction != right:
            self.pendingDirection = left  
        if keys[pygame.K_RIGHT] and self.direction != left:
            self.pendingDirection = right
            
    def resetGame(self):
        self.position = self.initialPosition
        self.direction = self.initialDirection
        self.pendingDirection = self.initialDirection
        self.body = [self.position,
                     (self.position[0] - gridLength, self.position[1]),
                     (self.position[0] - 2 * gridLength, self.position[1])]
        self.snakeMoveDelay = 0.20                      
 
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        

        #Food Sprites
        self.foodPaths = ['Art/Fruits/Brinjal.png',
                          'Art/Fruits/Cabbage.png',
                          'Art/Fruits/Carrot.png',
                          'Art/Fruits/Corn.png',
                          'Art/Fruits/Grape.png',
                          'Art/Fruits/Kiwi.png',
                          'Art/Fruits/Mango.png',
                          'Art/Fruits/Mushroom.png',
                          'Art/Fruits/Orange.png',
                          'Art/Fruits/Pear.png',
                          'Art/Fruits/Pepper.png']
        
        self.respawnFood()

    def generateRandomPosition(self): #Don't store this as a variable! Making it a function will make it random every time.
        while True:
            x = random.randint(1, gridCount - 2) * gridLength
            y = random.randint(1, gridCount - 2) * gridLength

            if (x, y) not in snake.body:
                return x, y

    def randomizeFood(self):
        self.randomFoodPath = random.choice(self.foodPaths)
        self.image = pygame.image.load(self.randomFoodPath).convert_alpha()
        self.rect = self.image.get_rect()

    def respawnFood(self):
        self.foodPosition = self.generateRandomPosition()
        self.randomizeFood()
#==========================================================================

pygame.init()
pygame.display.set_caption("✧*̥˚ Aryaman's Snake *̥˚✧")
pygame.display.set_icon(pygame.image.load('Art/Snake/SnakeHead.png'))

#Direction Controls
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

#Screen Configurations
screenLength = 576
gridCount = 18
gridLength = screenLength // gridCount
screen = pygame.display.set_mode((screenLength,screenLength))

bgSurf = pygame.image.load('Art/Background.png').convert()
fontTitle = pygame.font.Font('Art/MonsterFriendFore.otf', 50)
fontSubtitle = pygame.font.Font('Art/MonsterFriendFore.otf', 16)
fontScore = pygame.font.Font('Art/MonsterFriendFore.otf', 32)

gameName = fontTitle.render('Snake!',False,"#ae3434")
gameNameRect = gameName.get_rect(center = (screenLength/2, 200))

myName = fontSubtitle.render('by Aryaman',False,"#a18431")
myNameRect = gameName.get_rect(center = (screenLength/2+103, 250))

#Snake and Food Configurations
snake = Snake()
# snakeMoveDelay = 0.20 (This has been moved to snake() class)
lastMoveTime = 0

food = Food()
 
# Main Loop Configurations
gameRunning = True
clock = pygame.time.Clock()
highScore = 0

#==========================================================================

# Main Loop
while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    currentTime = pygame.time.get_ticks()
    
    #Snake Configurations
    if currentTime - lastMoveTime > snake.snakeMoveDelay * 1000:
        lastMoveTime = currentTime
        snake.update()

    snake.playerInput()

    if (snake.position[0] < gridLength or snake.position[0] >= screenLength-gridLength or
        snake.position[1] < gridLength or snake.position[1] >= screenLength-gridLength or
        snake.position in snake.body[1:]):
        food.respawnFood()
        snake.resetGame()

    if snake.position == food.foodPosition:
        food.respawnFood()
        snake.eatFood()    
     
    #Drawings            
    screen.blit(bgSurf,(0,0))
       
    score = len(snake.body) - 2
    if score > highScore:
        highScore = score
    
    viewScore = fontSubtitle.render(f'Score: {score}',False,"#5e342c")
    viewScoreRect = viewScore.get_rect(center = (100, 45))
    
    viewHighScore = fontSubtitle.render(f'Highscore: {highScore}',False,"#5e342c")
    viewHighScoreRect = viewHighScore.get_rect(center = (screenLength-127, 45))
    
    if score <= 1:
            screen.blit(gameName, gameNameRect)
            screen.blit(myName, myNameRect)
    else: 
        screen.blit(viewScore, viewScoreRect)
        screen.blit(viewHighScore, viewHighScoreRect)
    
    
    foodRect = pygame.Rect(food.foodPosition, food.rect.size)          
    screen.blit(food.image, foodRect)

    
    # Snake Head Render    
    if snake.body[1][0] > snake.body[0][0]:
        screen.blit(snake.snakeHeadLeft, snake.body[0])
    elif snake.body[1][0] < snake.body[0][0]:
        screen.blit(snake.snakeHeadRight, snake.body[0])
    elif snake.body[1][1] < snake.body[0][1]:
        screen.blit(snake.snakeHeadDown, snake.body[0])
    elif snake.body[1][1] > snake.body[0][1]:
        screen.blit(snake.snakeHeadUp, snake.body[0])
    # Snake Tail Render
    if len(snake.body) > 1:
        if snake.body[-2][0] > snake.body[-1][0]:
            screen.blit(snake.snakeTailRight, snake.body[-1])
        elif snake.body[-2][0] < snake.body[-1][0]:
            screen.blit(snake.snakeTailLeft, snake.body[-1])
        elif snake.body[-2][1] > snake.body[-1][1]:
            screen.blit(snake.snakeTailDown, snake.body[-1])
        elif snake.body[-2][1] < snake.body[-1][1]:
            screen.blit(snake.snakeTailUp, snake.body[-1])         
    # Snake Body Render        
    for index, segment in enumerate(snake.body[1:-1]):       
        #Bent Segments
        if snake.body[index+2][0] > snake.body[index+1][0] and snake.body[index][1] > snake.body[index+1][1]:
            screen.blit(snake.snakeUpturnLeft, snake.body[index+1])
        elif snake.body[index+2][0] < snake.body[index+1][0] and snake.body[index][1] > snake.body[index+1][1]:
            screen.blit(snake.snakeDownturnDown, snake.body[index+1])
            
        elif snake.body[index+2][0] > snake.body[index+1][0] and snake.body[index][1] < snake.body[index+1][1]:
            screen.blit(snake.snakeDownturnUp, snake.body[index+1])
        elif snake.body[index+2][0] < snake.body[index+1][0] and snake.body[index][1] < snake.body[index+1][1]:
            screen.blit(snake.snakeUpturnRight, snake.body[index+1])
            
        elif snake.body[index][0] > snake.body[index+1][0] and snake.body[index+2][1] < snake.body[index+1][1]:
            screen.blit(snake.snakeUpturnDown, snake.body[index+1])
        elif snake.body[index][0] < snake.body[index+1][0] and snake.body[index+2][1] < snake.body[index+1][1]:
            screen.blit(snake.snakeDownturnLeft, snake.body[index+1])
            
        elif snake.body[index][0] > snake.body[index+1][0] and snake.body[index+2][1] > snake.body[index+1][1]:
            screen.blit(snake.snakeDownturnRight, snake.body[index+1])
        elif snake.body[index][0] < snake.body[index+1][0] and snake.body[index+2][1] > snake.body[index+1][1]:
            screen.blit(snake.snakeUpturnUp, snake.body[index+1])   
                     
        #Body Segments                           
        elif snake.body[index+1][0] > snake.body[index][0]:
            screen.blit(snake.snakeBodyLeft, snake.body[index+1])
        elif snake.body[index+1][0] < snake.body[index][0]:
            screen.blit(snake.snakeBodyRight, snake.body[index+1])            
        elif snake.body[index+1][1] > snake.body[index][1]:
            screen.blit(snake.snakeBodyUp, snake.body[index+1])
        elif snake.body[index+1][1] < snake.body[index][1]:
            screen.blit(snake.snakeBodyDown, snake.body[index+1])
    
    pygame.display.update()
    clock.tick(60)