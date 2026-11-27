import threading
import random
import pandas as pd
import tkinter as tk
# import keyboard
import time
import problems as st


import faulthandler

faulthandler.dump_traceback_later(10, repeat=True)

# pip3 install plot
#pip3 install pandas
# pip3 install keyboard
# set environment constants


# set environment constants
GRID_SIZE = (50,50)
RESOLUTION = (600,600)
SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
SPEED = 0
EPOCHS = 100
EPSILON = 1
GAMMA = 0
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
canvas_rects = {}
apple_rect_id = None
show = False



# window.update()
reset = False # tells game to reset in the game loop. 
#game controller (stores current vars agent stores curr + past vars)


snake = [(GRID_SIZE[0]/2, GRID_SIZE[1]/2)]
tail = snake[-1]
apple = ()
score = 0
direction = (0,1)
gamesPlayed = 0

#extra statistics for the snake
agent = st.Qlearning()#make player object

#reset environment/restart game vars(locks)
state = False
gameOver = False







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
    # if(show):
        # renderSnake(snake[0][0],snake[0][1], False)

        
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
    elif len(snake) >= GRID_SIZE[0]*GRID_SIZE[1]:
        collision == True
    
    if collision == True:
        gameTotal = gameTotal+1
        print("game over", gameTotal)
    return collision
            
#generates a new apple            
def makeApple():
    global apple
    while True:
        if(len(snake)== GRID_SIZE[0]*GRID_SIZE[1]):
            break
        elif(len(snake)>GRID_SIZE[0]*GRID_SIZE[1]):
            raise RuntimeError("this is an error in the make appple function since the apple has no home")
        apple = (random.randint(0, GRID_SIZE[0]-1), random.randint(0, GRID_SIZE[1]-1))
        if apple not in snake:
            break
    # agent.SnakeAfterFood.append(snake)
    agent.AppleList.append(apple)



#has eaten an apple and gets score
def hasEaten(snake_copy):
    global snake, apple, tail, score, stepCount


    if snake_copy == None:
        if snake[0] == apple:
            snake.append(tail)
            # renderSnake(tail[0], tail[1], False)
            if len(snake) >= GRID_SIZE[0]*GRID_SIZE[1]:
                print("you won")
            else:
                print(" in else statement making apple now", len(snake), GRID_SIZE[0]*GRID_SIZE[1])
                
                makeApple()


#  in else statement making apple now 15 16
# you won
#  in else statement making apple now 17 16
# Timeout (0:00:10)!
                score = score+10 
                stepCount = 0
       
        else:
            stepCount = stepCount+1
            # renderSnake(tail[0],tail[1], True)
        return stepCount, score
    else:
        if snake_copy[0] == apple:
            return True
        else:
            return False
            

#initialize to starting state
def start():
    global tail, snake, apple, score, direction, plot, stepCount, reset


    # canvas.delete("all")
    # window.update()
    snake.append((GRID_SIZE[0]/2, GRID_SIZE[1]/2))
    while(len(snake) != 0):
        snake.pop()
    snake.append((GRID_SIZE[0]/2, GRID_SIZE[1]/2))
    tail = snake[-1]
    score = 0
    direction = (0,1)
    makeApple()
    agent.addStats(snake, apple, stepCount, score, direction)
    snake = [(GRID_SIZE[0] / 2, GRID_SIZE[1] / 2)]
    tail = snake[-1]
    score = 0
    direction = (0, 1)
    stepCount = 0
    reset = False # when start game is presssed finishes reset. 


    
    # plot = agent.gameOver() #returns the plot object so that the gui doesn't have a null object for the plot. might break stuff?


#game loop
def run(first):
    global state, x, y, snake, apple, score, gameOver, direction, stepCount, plot, reset
    # global 
    if(first):
        start()
        first = False
    while(1):
        getDirection("up")
        agent.addStats(snake, apple, stepCount, score, direction)
        resetSkip = False
        #spinning lock (inefficient, but doesn't matter)
        i = 0
        while reset:
            # print("waiting for start command")
            resetSkip = True
            i += 1
            # this is there for multi threading.
            #otherwise the loop hogs the gui update thread (SO COOL)
            if i == 1000:
                break
            
    
        if(state == False and resetSkip == False):
            moveSnake(None, None) #render part done here
            stepCount, score = hasEaten(None) #eats apple gets score
            gameOver = collisionCheck(None)
            # window.update_idletasks() 
            state = True
        if state == True and resetSkip == False:
            state = False
        # label.config(text=f"Score: {score} game total:{gameTotal}")#big time sucker function

        #game over loop wait for reset of game
        while gameOver == True and resetSkip == False:
            if(gameTotal <EPOCHS):
                # plot = i have no idea why this isn't nbeing used...old code but handled in gui/demo.py which is better
                agent.gameOver() #makes data frame of the player stats of the round
                # agent.resetPlayer()#resets the player at the end of the game new function might be needed here

                start()
                gameOver = False
            # window.update()
        
            if(gameOver == False):
                break
        
        if  resetSkip and not reset:
            start()
            resetSkip = False
    
#resets training and everything back to its original state. 
def reset():
    global GRID_SIZE, RESOLUTION, SQUARE_SIZE, SPEED, reset, score, direction, gamesPlayed, gameTotal, show, window, label, canvas, snake, tail, apple
    # GRID_SIZE = (50,50)
    # RESOLUTION = (600,600)
    # SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
    SPEED = 100 
    gameTotal = 0
    score = 0
    # # while(len(snake) != 0):
    # #     snake.pop()
    # # snake = [(GRID_SIZE[0]/2, GRID_SIZE[1]/2)]
    # # canvas.pack()
    # # window.update()

    # #game controller (stores current vars agent stores curr + past vars)
    # # tail = snake[-1]
    # # apple = ()
    # # direction = (0,1)
    # score = 0
    # gamesPlayed = 0
    reset = True
    agent.resetPlayer() #this was a big redundancy headache i neeed to fix



stepCount = 0




# render the snake. Will be replaced with render every 1000 turns
# def renderSnake(x,y, remove):
    
#     global  color, canvas_rects, apple_rect_id, apple

#     if apple_rect_id is not None:
#         canvas.delete(apple_rect_id)
#     pixel_x = SQUARE_SIZE[0] * apple[0]
#     pixel_y = SQUARE_SIZE[1] * apple[1]
#     apple_rect_id = canvas.create_rectangle(
#         pixel_x, pixel_y,
#         pixel_x + SQUARE_SIZE[0], pixel_y + SQUARE_SIZE[1],
#         fill=FOOD_COLOR
#     )
#     pixel_x = SQUARE_SIZE[0] * x
#     pixel_y = SQUARE_SIZE[1] * y

#     if not remove:
#         rect_id = canvas.create_rectangle(
#             pixel_x,
#             pixel_y,
#             pixel_x + SQUARE_SIZE[0],
#             pixel_y + SQUARE_SIZE[1],
#             fill=SNAKE_COLOR
#         )
#         canvas_rects[(x, y)] = rect_id
#         # canvas.create_rectangle(
#         #     pixel_x,
#         #     pixel_y,
#         #     pixel_x + SQUARE_SIZE[0],
#         #     pixel_y + SQUARE_SIZE[1],
#         #     fill=SNAKE_COLOR
#         # )
#     else:
#         # pygame.draw.rect(surface, (0,0,0), rect)
#         rect_id = canvas_rects.pop((x, y), None)
#         canvas.create_rectangle(
#             pixel_x,
#             pixel_y,
#             pixel_x + SQUARE_SIZE[0],
#             pixel_y + SQUARE_SIZE[1],
#             fill=BG_COLOR,
#             outline=BG_COLOR
#         )
#         if rect_id is not None:
#             canvas.delete(rect_id)




# this is the old code that broke it 
# import threading
# import random
# import pandas as pd
# import tkinter as tk
# # import keyboard
# import time
# import problems as st


# # pip3 install plot
# #pip3 install pandas
# # pip3 install keyboard
# # set environment constants


# import faulthandler

# faulthandler.dump_traceback_later(10, repeat=True)
# # set environment constants
# GRID_SIZE = (50,50)
# RESOLUTION = (600,600)
# SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
# SPEED = 0
# EPOCHS = 100
# EPSILON = 1
# GAMMA = 0
# #make screen appear
# SNAKE_COLOR = "#00FF00"
# FOOD_COLOR = "#FF0000"
# BG_COLOR = "#000000"
# gameTotal = 0
# show = True
# window = tk.Tk()
# window.title("Snake Game")
# window.resizable(False, False)
# label = tk.Label(window, text=f"Score: {0} game total:{0} ", font=("Consolas", 20))
# label.pack()
# canvas = tk.Canvas(window, bg=BG_COLOR, height=RESOLUTION[1], width=RESOLUTION[0])
# canvas.pack()
# canvas_rects = {}
# apple_rect_id = None
# show = False



# # window.update()
# reset = False # tells game to reset in the game loop. 
# #game controller (stores current vars agent stores curr + past vars)


# snake = [(GRID_SIZE[0]/2, GRID_SIZE[1]/2)]
# tail = snake[-1]
# apple = ()
# score = 0
# direction = (0,1)
# gamesPlayed = 0

# #extra statistics for the snake
# agent = st.Qlearning()#make player object

# #reset environment/restart game vars(locks)
# state = False
# gameOver = False





# #takes keyboard inputa and moves the snake
# def getDirection(event):
#     global direction, agent
#     if(direction == "up"):
#         if event.keysym == "Left" and direction != (1, 0):
#             direction = (-1, 0)
#         elif event.keysym == "Right" and direction != (-1, 0):
#             direction = (1, 0)
#         elif event.keysym == "Up" and direction != (0, 1):
#             direction = (0, -1)
#         elif event.keysym == "Down" and direction != (0, -1):
#             direction = (0, 1)
        
#     direction = agent.getDirection()
#     return direction

# #modes the snake in most recent direction
# def moveSnake(snake_clone, dir_clone):
#     global snake, direction, tail


#     head = snake[0]
#     tail = snake[-1]
#     snake.pop()
#     snake.insert(0, (head[0]+direction[0], head[1]+direction[1]))
#     # if(show):
#         # renderSnake(snake[0][0],snake[0][1], False)

        
#     return snake

    

# #this function checks for collisions which would end the game  
# def collisionCheck(snake_clone):
#     global gameTotal
#     global snake
#     if(snake_clone == None):
#         snake_clone = snake
#     collision = False
#     for index, x in enumerate(snake_clone):
#         if index != 0:
#             if snake_clone[0] == x:
#                 collision = True
#     if snake_clone[0][0] < 0 or snake_clone[0][0] >= GRID_SIZE[0] or snake_clone[0][1] < 0 or snake_clone[0][1] >= GRID_SIZE[1]:
#         collision = True
#     if collision == True:
#         gameTotal = gameTotal+1
#         print("game over", gameTotal)
#     elif len(snake) == GRID_SIZE[0]*GRID_SIZE[1]:
#         gameTotal = gameTotal+1
#         collision = True
#         print("You won", gameTotal)
    
    
#     return collision
            
# #generates a new apple            
# def makeApple():
#     global apple
#     while True:
#         apple = (random.randint(0, GRID_SIZE[0]-1), random.randint(0, GRID_SIZE[1]-1))
#         if apple not in snake:
#             break
#     agent.AppleList.append(apple)
#     # if(len(snake) == GRID_SIZE[0]**2):






# #has eaten an apple and gets score
# def hasEaten(snake_copy):
#     global snake, apple, tail, score, stepCount, gameOver
#     if snake_copy == None:
#         if snake[0] == apple:
#             snake.append(tail)
#             # renderSnake(tail[0], tail[1], False)
#             if len(snake) == GRID_SIZE[0]*GRID_SIZE[1]:
#                 print("you won")

#                 gameOver = True  # ← ends the game
#                 return stepCount, score  # ← stops hasEaten
#             else:
#                 makeApple()
#                 score = score+10 
#                 stepCount = 0
#         else:
#             stepCount = stepCount+1
#             # renderSnake(tail[0],tail[1], True)
#         return stepCount, score
#     else:
#         if snake_copy[0] == apple:
#             return True
#         else:
#             return False
            

# #initialize to starting state
# def start():
#     global tail, snake, apple, score, direction, plot, stepCount, reset


#     # canvas.delete("all")
#     # window.update()
#     snake.append((GRID_SIZE[0]/2, GRID_SIZE[1]/2))
#     while(len(snake) != 0):
#         snake.pop()
#     snake.append((GRID_SIZE[0]/2, GRID_SIZE[1]/2))
#     tail = snake[-1]
#     score = 0
#     direction = (0,1)
#     makeApple()
#     agent.addStats(snake, apple, stepCount, score, direction)
#     snake = [(GRID_SIZE[0] / 2, GRID_SIZE[1] / 2)]
#     tail = snake[-1]
#     score = 0
#     direction = (0, 1)
#     stepCount = 0
#     reset = False # when start game is presssed finishes reset. 


    
#     # plot = agent.gameOver() #returns the plot object so that the gui doesn't have a null object for the plot. might break stuff?


# def run(first):
#     global state, x, y, snake, apple, score, gameOver, direction, stepCount, plot, reset
#     if(first):
#         start()
#         first = False

#     if not reset:
#         if(state == False):
#             moveSnake(None, None)
#             stepCount, score = hasEaten(None)
#             gameOver = collisionCheck(None)
#             state = True
#         if state == True:
#             state = False
#         agent.addStats(snake, apple, stepCount, score, direction)

#         while gameOver == True:
#             if(gameTotal < EPOCHS):
#                 agent.gameOver()
#                 start()
#                 gameOver = False
#             break

#     if gameTotal < EPOCHS:
#         window.after(SPEED, lambda: run(False))
    
# #resets training and everything back to its original state. 
# def reset():
#     global GRID_SIZE, RESOLUTION, SQUARE_SIZE, SPEED, reset, score, direction, gamesPlayed, gameTotal, show, window, label, canvas, snake, tail, apple
#     # GRID_SIZE = (50,50)
#     # RESOLUTION = (600,600)
#     # SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
#     SPEED = 100 
#     gameTotal = 0
#     score = 0
#     # # while(len(snake) != 0):
#     # #     snake.pop()
#     # # snake = [(GRID_SIZE[0]/2, GRID_SIZE[1]/2)]
#     # # canvas.pack()
#     # # window.update()

#     # #game controller (stores current vars agent stores curr + past vars)
#     # # tail = snake[-1]
#     # # apple = ()
#     # # direction = (0,1)
#     # score = 0
#     # gamesPlayed = 0
#     reset = True
#     agent.resetPlayer() #this was a big redundancy headache i neeed to fix



# stepCount = 0




# #render the snake. Will be replaced with render every 1000 turns
# # def renderSnake(x,y, remove):
    
# #     global  color, canvas_rects, apple_rect_id, apple

# #     if apple_rect_id is not None:
# #         canvas.delete(apple_rect_id)
# #     pixel_x = SQUARE_SIZE[0] * apple[0]
# #     pixel_y = SQUARE_SIZE[1] * apple[1]
# #     apple_rect_id = canvas.create_rectangle(
# #         pixel_x, pixel_y,
# #         pixel_x + SQUARE_SIZE[0], pixel_y + SQUARE_SIZE[1],
# #         fill=FOOD_COLOR
# #     )
# #     pixel_x = SQUARE_SIZE[0] * x
# #     pixel_y = SQUARE_SIZE[1] * y

# #     if not remove:
# #         rect_id = canvas.create_rectangle(
# #             pixel_x,
# #             pixel_y,
# #             pixel_x + SQUARE_SIZE[0],
# #             pixel_y + SQUARE_SIZE[1],
# #             fill=SNAKE_COLOR
# #         )
# #         canvas_rects[(x, y)] = rect_id
# #         # canvas.create_rectangle(
# #         #     pixel_x,
# #         #     pixel_y,
# #         #     pixel_x + SQUARE_SIZE[0],
# #         #     pixel_y + SQUARE_SIZE[1],
# #         #     fill=SNAKE_COLOR
# #         # )
# #     else:
# #         # pygame.draw.rect(surface, (0,0,0), rect)
# #         rect_id = canvas_rects.pop((x, y), None)
# #         canvas.create_rectangle(
# #             pixel_x,
# #             pixel_y,
# #             pixel_x + SQUARE_SIZE[0],
# #             pixel_y + SQUARE_SIZE[1],
# #             fill=BG_COLOR,
# #             outline=BG_COLOR
# #         )
# #         if rect_id is not None:
# #             canvas.delete(rect_id)

# # window.mainloop()
