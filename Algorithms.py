import threading
import random
import pandas as pd
import tkinter as tk
# import keyboard
import time
import problems as st


# pip3 install plot
#pip3 install pandas
# pip3 install keyboard
# set environment constants


# set environment constants
GRID_SIZE = (50,50)
RESOLUTION = (600,600)
SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
SPEED = 100
EPOCHS = 100
EPSILON = 1
GAMMA = 0
plot = None
#make screen appear
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"
gameTotal = 0
show = True
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)
label = tk.Label(window, text=f"Score: {0} game total:{0} ", font=("Consolas", 20))
label.pack()
canvas = tk.Canvas(window, bg=BG_COLOR, height=RESOLUTION[1], width=RESOLUTION[0])
canvas.pack()
window.update()

#game controller (stores current vars agent stores curr + past vars)
snake = [(GRID_SIZE[0]/2, GRID_SIZE[1]/2)]
tail = snake[-1]
apple = ()
score = 0
direction = (0,1)
score = 0
gamesPlayed = 0

#reset environment/restart game vars(locks)
state = False
gameOver = False


#extra statistics for the snake
agent = st.player()#make player object


#takes keyboard inputa and moves the snake
def getDirection(event):
    global direction, agent
    if(direction == "up"):
        if event.keysym == "Left" and direction != (1, 0):
            direction = (-1, 0)
        elif event.keysym == "Right" and direction != (-1, 0):
            direction = (1, 0)
        elif event.keysym == "Up" and direction != (0, 1):
            direction = (0, -1)
        elif event.keysym == "Down" and direction != (0, -1):
            direction = (0, 1)
        
    direction = agent.getDirection()
    return direction

#modes the snake in most recent direction
def moveSnake(snake_clone, dir_clone):
    global snake, direction, tail


    head = snake[0]
    tail = snake[-1]
    snake.pop()
    snake.insert(0, (head[0]+direction[0], head[1]+direction[1]))
    if(show):
        renderSnake(snake[0][0],snake[0][1], False)
    return snake

    

#this function checks for collisions which would end the game  
def collisionCheck(snake_clone):
    global gameTotal
    global snake
    if(snake_clone == None):
        snake_clone = snake
    collision = False
    for index, x in enumerate(snake_clone):
        if index != 0:
            if snake_clone[0] == x:
                collision = True
    if snake_clone[0][0] < 0 or snake_clone[0][0] >= GRID_SIZE[0] or snake_clone[0][1] < 0 or snake_clone[0][1] >= GRID_SIZE[1]:
        collision = True
    if collision == True:
        gameTotal = gameTotal+1
        print("game over")
    return collision
            
#generates a new apple            
def makeApple():
    global apple
    apple = (random.randint(0, GRID_SIZE[0]-1), random.randint(0, GRID_SIZE[1]-1))     
    for x in snake:
        if apple == x:
            makeApple()
            return

    agent.SnakeAfterFood.append(snake)
    agent.AppleList.append(apple)

    pixel_x = SQUARE_SIZE[0] * apple[0]
    pixel_y = SQUARE_SIZE[1] * apple[1]

    if(show):
        canvas.create_rectangle(
            pixel_x,
            pixel_y,
            pixel_x + SQUARE_SIZE[0],
            pixel_y + SQUARE_SIZE[1],
            fill=FOOD_COLOR
        )


def renderSnake(x,y, remove):
    
    global  color
    pixel_x = SQUARE_SIZE[0] * x
    pixel_y = SQUARE_SIZE[1] * y

    if not remove:
        canvas.create_rectangle(
            pixel_x,
            pixel_y,
            pixel_x + SQUARE_SIZE[0],
            pixel_y + SQUARE_SIZE[1],
            fill=SNAKE_COLOR
        )
    else:
        # pygame.draw.rect(surface, (0,0,0), rect)
        canvas.create_rectangle(
            pixel_x,
            pixel_y,
            pixel_x + SQUARE_SIZE[0],
            pixel_y + SQUARE_SIZE[1],
            fill=BG_COLOR,
            outline=BG_COLOR
        )
    
    # rgb = pygame.image.tobytes(surface, "RGB")# this creates 
    # image = Image.frombytes("RGB", surface.get_size(), rgb)
    # tk_image = ImageTk.PhotoImage(image)
    # image_callback(tk_image)


#has eaten an apple and gets score
def hasEaten(snake_copy):
    global snake, apple, tail, score, stepCount
    if snake_copy == None:
        if snake[0] == apple:
            snake.append(tail)
            if len(snake) == GRID_SIZE[0]*GRID_SIZE[1]:
                print("you won")
            else:
                makeApple()
                score = score+10 
                stepCount = 0
        else:
            stepCount = stepCount+1
            renderSnake(tail[0],tail[1], True)
        return stepCount, score
    else:
        if snake_copy[0] == apple:
            return True
        else:
            return False
            


def start():
    global tail, snake, apple, score, direction, plot, stepCount


    canvas.delete("all")
    window.update()
    snake.append((GRID_SIZE[0]/2, GRID_SIZE[1]/2))
    while(len(snake) != 0):
        snake.pop()
    snake.append((GRID_SIZE[0]/2, GRID_SIZE[1]/2))
    tail = snake[-1]
    score = 0
    direction = (0,1)
    makeApple()
    agent.addStats(snake, apple, stepCount, score, direction)
    # plot = agent.gameOver() #returns the plot object so that the gui doesn't have a null object for the plot. might break stuff?


def run(first):
    global state, x, y, snake, apple, score, gameOver, direction, stepCount, plot
    if(first):
        start()
        first = False
    
    getDirection("up")
    agent.addStats(snake, apple, stepCount, score, direction)


    if(state == False):
        moveSnake(None, None) #render part done here
        stepCount, score = hasEaten(None) #eats apple gets score
        gameOver = collisionCheck(None)
        window.update_idletasks()
        state = True
    if state == True:
        state = False
    label.config(text=f"Score: {score} game total:{gameTotal}")

    #game over loop wait for reset of game
    while gameOver == True:
        if(gameTotal <EPOCHS):
            plot = agent.gameOver() #makes data frame of the player stats of the round
            start()
            gameOver = False
        window.update()
    
        if(gameOver == False):
            break
    window.after(SPEED, lambda: run(False))


def reset():
    GRID_SIZE = (50,50)
    RESOLUTION = (600,600)
    SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
    SPEED = 100 
window.mainloop()

stepCount = 0
