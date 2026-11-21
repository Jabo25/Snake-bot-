
#this will be renamed to assist with the player agent. 
#through inheretence, the player object type will be modified to deal with new algorithms. 
#the inhereted class will be an algorithm object which is going to be a player atruibute
import threading
import multiprocessing
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
                                               NavigationToolbar2Tk)
root = tk.Tk()
#maybe make an object called a game to store the local game stats. 

# set environment constants
GRID_SIZE = (50,50)
RESOLUTION = (600,600)
SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
SPEED = 100
EPOCHS = 100
EPSILON = 1
GAMMA = 0


#modes the snake in most recent direction
def moveSnake(snake_clone1, dir_clone1):
        snake_clone = snake_clone1.copy()
        dir_clone = dir_clone1

        head = snake_clone[0]
        tail = snake_clone[-1]
        tail = snake_clone[-1]
        snake_clone.pop()
        snake_clone.insert(0, (head[0]+dir_clone[0], head[1]+dir_clone[1]))
        return snake_clone


#this function checks for collisions which would end the game  
def collisionCheck(snake_clone1):
    snake_clone = snake_clone1.copy()
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

    return collision
      
#has eaten an apple and gets score
def hasEaten(snake_copy1):
    snake_copy = snake_copy1.copy()
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
            
# 20 sewcs second 2000
class player: 
    def __init__(self, agentType=None, averageScore=0, name=None):

        # self.plotThread = threading.Thread(
        #     target=self.plotWorker,
        #     daemon=True
        # )
        # self.plotThread.start()
        self.agentType = agentType
        self.averageScore = averageScore
        self.finalScoreList = []
        self.totalGames = 0
        self.GameHistory = []
        self.Name = name

        self.df = pd.DataFrame()

        self.snakeHistory = []
        self.appleHistory = []  # Stores apple at target time step
        self.stepsSinceLastApple = []
        self.scoreHistory = []
        self.stepCount = 0
        self.directionHistory = []
        self.foodDistance = []
        self.SnakeAfterFood = []  # Stores the snake when it last ate
        self.AppleList = []  # Stores apple each time it is generated
        EPSILON = 0.3
        self.gameTotal = 0
        self.FinalScore = 0  # Stores apple each time it is generated

        #fun test
        # self.fig, self.ax = plt.subplots()
        self.fig, self.ax = plt.subplots(figsize=(3, 2), dpi=80)
        (self.line,) = self.ax.plot([], [], label="Score")

        # 3. Setup static labels once
        self.ax.set_title("Score")
        self.ax.set_xlabel("Game")
        self.ax.set_ylabel("Score")
        self.norm = "l1"
        # plt.show(block=False)

    
    def addStats(self, snake, apple, stepCount, score, direction):
        # global df, snakeHistory, appleHistory, stepsSinceLastApple, score, stepCount, directionHistory, direction, snake, apple 
        self.snakeHistory.append(snake)
        self.appleHistory.append(apple)
        self.stepsSinceLastApple.append(stepCount)
        self.scoreHistory.append(score)
        self.directionHistory.append(direction)
        self.foodDistance.append(abs(snake[0][0]-apple[0]) + abs(snake[0][1]-apple[1]))
        
    def resetPlayer(self):
        self.snakeHistory.clear()
        self.appleHistory.clear()
        self.stepsSinceLastApple.clear()
        self.scoreHistory.clear()
        self.directionHistory.clear()
        self.foodDistance.clear()


        

    def getDistance(self,direction):
        apple = self.appleHistory[-1]
        snake = self.snakeHistory[-1][0]        
        snake = (snake[0]+direction[0], snake[1]+direction[1])
        # return abs(abs(snake[0]-apple[0])**2 + abs(snake[1]-apple[1])**2)
        if self.norm == "l1":
            return abs(abs(snake[0] - apple[0]) +  abs(snake[1] - apple[1]))
        elif self.norm == "l2":
            return abs(abs(snake[0]-apple[0])**2 + abs(snake[1]-apple[1])**2)
        else:
            return max(abs(snake[0] - apple[0]), abs(snake[1] - apple[1]))


    def getDirection(self):
        # if(len(self.directionHistory) == 0):
        #     return (0,1)
        if not self.snakeHistory or not self.snakeHistory[-1]:
            return (0, 1)

        snake = self.snakeHistory[-1]
        direction = self.directionHistory[-1]
        inverseDir = (direction[0]*-1,direction[1]*-1)
        options = []
        InverseCase = True
        directionList = []#[(0,1), (0,-1), (1,0), (-1,0)]
        if(inverseDir != (0,1)):
            snake_copy = moveSnake(snake, (0,1))
            if(not collisionCheck(snake_copy)):
                options.append(self.getDistance((0,1)))
                directionList.append((0,1))
        if(inverseDir != (0,-1)):
            snake_copy = moveSnake(snake, (0,-1))
            if(not collisionCheck(snake_copy)):
                options.append(self.getDistance((0,-1)))
                directionList.append((0,-1))
        if(inverseDir != (1,0)):
            snake_copy = moveSnake(snake, (1,0))
            if(not collisionCheck(snake_copy)):
                options.append(self.getDistance((1,0)))
                directionList.append((1,0))
        if(inverseDir != (-1,0)):
            snake_copy = moveSnake(snake, (-1,0))
            if(not collisionCheck(snake_copy)):
                options.append(self.getDistance((-1,0)))
                directionList.append((-1,0))


           # consider right and left  IE
        
        min = 99999999999999
        for x,y in zip(options, directionList):
            if min> x:
                min = x
                direction = y
        if(len(options) == 0):
            return (0,1)
        return direction

    def makePlot(self):
        games = list(range(1, len(self.finalScoreList) + 1))

        self.line.set_xdata(games)
        self.line.set_ydata(self.finalScoreList)

        self.ax.relim()
        self.ax.autoscale_view()

        self.fig.canvas.draw_idle()

        return self.fig

    def gameOver(self):
        #make a plot of progress
        #print total scores
        #reset everything

        #what types of plots:
            # line plot
            # histogram of the scores
            # matplotlib.pyplot.plot(*args, scalex=True, scaley=True, data=None, **kwargs)[source]
        # 12.5 seconds with just this if
        if(len(self.scoreHistory) != 0):
            self.finalScoreList.append(self.scoreHistory[-1])

        # 
        self.df = pd.DataFrame(
                            {
                                "snake": self.snakeHistory,
                                "apple": self.appleHistory,
                                "stepsSinceLastApple": self.stepsSinceLastApple,
                                "score": self.scoreHistory,
                                "direction": self.directionHistory
                            }
                        )
        
        self.GameHistory.append(self.df)
       
        self.df = pd.DataFrame()
        self.gameTotal = self.gameTotal+1
        self.FinalScore = 0 #set final score to 0. 

        # self.resetPlayer()#might cause major bug later
        if len(self.scoreHistory) !=0:
            if self.gameTotal % 10 == 0:
            # threading.Thread(target=self.makePlot).start()
                self.makePlot()
            # self.makePlot()
        # self.resetPlayer()#resets the player at the end of the game new function might be needed here
        # else:
            # self.fig

        self.resetPlayer()

        # return self.makePlot()
        
        # pass

        # second 2000 = 30 seconds
        






#move all player stats into the player object
# first 100 games = 2.6 seconds
# 200 = 5.5-5 secondds ish
# 300 = 8 seconds
# 400 = 11 seconds
# 500 = 15 seconds
# 600 = 21 seconds
# 700 = 26 seconds
# 800 = 33 seconds
# 900 = 40 seconds
# 1000 = 46 seconds
















# #this will be renamed to assist with the player agent. 
# #through inheretence, the player object type will be modified to deal with new algorithms. 
# #the inhereted class will be an algorithm object which is going to be a player atruibute
# import threading
# import multiprocessing
# import pandas as pd
# import matplotlib.pyplot as plt
# import tkinter as tk
# from tkinter import ttk
# from tkinter import * 
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
#                                                NavigationToolbar2Tk)
# root = tk.Tk()
# #maybe make an object called a game to store the local game stats. 

# # set environment constants
# GRID_SIZE = (50,50)
# RESOLUTION = (600,600)
# SQUARE_SIZE = (RESOLUTION[0]/(GRID_SIZE[0]),RESOLUTION[1]/(GRID_SIZE[1])) #body seg size
# SPEED = 100
# EPOCHS = 100
# EPSILON = 1
# GAMMA = 0


# #modes the snake in most recent direction
# def moveSnake(snake_clone1, dir_clone1):
#         snake_clone = snake_clone1.copy()
#         dir_clone = dir_clone1

#         head = snake_clone[0]
#         tail = snake_clone[-1]
#         tail = snake_clone[-1]
#         snake_clone.pop()
#         snake_clone.insert(0, (head[0]+dir_clone[0], head[1]+dir_clone[1]))
#         return snake_clone


# #this function checks for collisions which would end the game  
# def collisionCheck(snake_clone1):
#     snake_clone = snake_clone1.copy()
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

#     return collision
      
# #has eaten an apple and gets score
# def hasEaten(snake_copy1):
#     snake_copy = snake_copy1.copy()
#     global snake, apple, tail, score, stepCount
#     if snake_copy == None:
#         if snake[0] == apple:
#             snake.append(tail)
#             if len(snake) == GRID_SIZE[0]*GRID_SIZE[1]:
#                 print("you won")
#             else:
#                 # makeApple()
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
            



# class game:
#     def __init__(self, agentType=None, averageScore=0, name=None):
#         self.agentType = agentType
#         self.averageScore = averageScore
#         self.finalScoreList = []
#         self.totalGames = 0
#         self.GameHistory = []
#         self.Name = name
#         self.df = pd.DataFrame()
#         self.snakeHistory = []
#         self.appleHistory = []  # Stores apple at target time step
#         self.stepsSinceLastApple = []
#         self.scoreHistory = []
#         self.stepCount = 0
#         self.directionHistory = []
#         self.foodDistance = []
#         self.SnakeAfterFood = []  # Stores the snake when it last ate
#         self.AppleList = []  # Stores apple each time it is generated




        

# class player: 
#     def __init__(self, agentType=None, averageScore=0, name=None):
#         games = []# list that stores the history of every game
#         currentGame = game()
#         EPSILON = 0.3
#         self.gameTotal = 0
#         self.FinalScore = 0  # Stores apple each time it is generated

#         #fun test
#         # self.fig, self.ax = plt.subplots()
#         self.fig, self.ax = plt.subplots(figsize=(3, 2), dpi=80)
#         (self.line,) = self.ax.plot([], [], label="Score")

#         # 3. Setup static labels once
#         self.ax.set_title("Score")
#         self.ax.set_xlabel("Game")
#         self.ax.set_ylabel("Score")
#         self.norm = "l1"
#         # plt.show(block=False)

    
#     def addStats(self, snake, apple, stepCount, score, direction):
#         # global df, snakeHistory, appleHistory, stepsSinceLastApple, score, stepCount, directionHistory, direction, snake, apple 
#         self.gameList[-1].snakeHistory.append(snake)
#         self.gameList[-1].appleHistory.append(apple)
#         self.gameList[-1].stepsSinceLastApple.append(stepCount)
#         self.gameList[-1].scoreHistory.append(score)
#         self.gameList[-1].directionHistory.append(direction)
#         self.gameList[-1].foodDistance.append(abs(snake[0][0]-apple[0]) + abs(snake[0][1]-apple[1]))
        
#     def resetPlayer(self):
#         self.gameList.clear()
#         # self.snakeHistory.clear()
#         # self.appleHistory.clear()
#         # self.stepsSinceLastApple.clear()
#         # self.scoreHistory.clear()
#         # self.directionHistory.clear()
#         # self.foodDistance.clear()


        
#     #uses game object
#     def getDistance(self,direction):
#         apple = self.gameList[-1].appleHistory[-1]
#         snake = self.gameList[-1].snakeHistory[-1][0]        
#         snake = (snake[0]+direction[0], snake[1]+direction[1])

#         # return abs(abs(snake[0]-apple[0])**2 + abs(snake[1]-apple[1])**2)
#         if self.norm == "l1":
#             return abs(abs(snake[0] - apple[0]) +  abs(snake[1] - apple[1]))
#         elif self.norm == "l2":
#             return abs(abs(snake[0]-apple[0])**2 + abs(snake[1]-apple[1])**2)
#         else:
#             return max(abs(snake[0] - apple[0]), abs(snake[1] - apple[1]))

#     #uses game object
#     def getDirection(self):
#         # if(len(self.directionHistory) == 0):
#         #     return (0,1)
#         if not self.gameList[-1].snakeHistory or not self.gameList[-1].snakeHistory[-1]:
#             return (0, 1)

#         snake = self.gameList[-1].snakeHistory[-1]
#         direction = self.gameList[-1].directionHistory[-1]


        
#         inverseDir = (direction[0]*-1,direction[1]*-1)
#         options = []
#         InverseCase = True
#         directionList = []#[(0,1), (0,-1), (1,0), (-1,0)]
#         if(inverseDir != (0,1)):
#             snake_copy = moveSnake(snake, (0,1))
#             if(not collisionCheck(snake_copy)):
#                 options.append(self.getDistance((0,1)))
#                 directionList.append((0,1))
#         if(inverseDir != (0,-1)):
#             snake_copy = moveSnake(snake, (0,-1))
#             if(not collisionCheck(snake_copy)):
#                 options.append(self.getDistance((0,-1)))
#                 directionList.append((0,-1))
#         if(inverseDir != (1,0)):
#             snake_copy = moveSnake(snake, (1,0))
#             if(not collisionCheck(snake_copy)):
#                 options.append(self.getDistance((1,0)))
#                 directionList.append((1,0))
#         if(inverseDir != (-1,0)):
#             snake_copy = moveSnake(snake, (-1,0))
#             if(not collisionCheck(snake_copy)):
#                 options.append(self.getDistance((-1,0)))
#                 directionList.append((-1,0))


#            # consider right and left  IE
        
#         min = 99999999999999
#         for x,y in zip(options, directionList):
#             if min> x:
#                 min = x
#                 direction = y
#         if(len(options) == 0):
#             return (0,1)
#         return direction


#     def makePlot(self):
#         games = list(range(1, len(self.gameList[-1].finalScoreList) + 1))

#         self.line.set_xdata(games)
#         self.line.set_ydata(self.finalScoreList)

#         self.ax.relim()
#         self.ax.autoscale_view()

#         self.fig.canvas.draw_idle()

#         return self.fig

#     def gameOver(self):
#         #make a plot of progress
#         #print total scores
#         #reset everything

#         #what types of plots:
#             # line plot
#             # histogram of the scores
#             # matplotlib.pyplot.plot(*args, scalex=True, scaley=True, data=None, **kwargs)[source]
#         if(len(self.scoreHistory) != 0):
#             self.finalScoreList.append(self.scoreHistory[-1])
        
#         self.df = pd.DataFrame(
#                             {
#                                 "snake": self.snakeHistory,
#                                 "apple": self.appleHistory,
#                                 "stepsSinceLastApple": self.stepsSinceLastApple,
#                                 "score": self.scoreHistory,
#                                 "direction": self.directionHistory
#                             }
#                         )
#         self.GameHistory.append(self.df)
#         self.df = pd.DataFrame()
#         self.gameTotal = self.gameTotal+1
#         self.FinalScore = 0 #set final score to 0. 


#         if len(self.scoreHistory) !=0:
#             return self.makePlot()
#         else:
#             return self.fig
#         # return self.makePlot()







# #move all player stats into the player object
# # game total
# # first 100 games = 2.6 seconds
# # 200 = 5.5-5 secondds ish
# # 300 = 8 seconds
# # 400 = 11 seconds
# # 500 = 15 seconds
# # 600 = 21 seconds
# # 700 = 26 seconds
# # 800 = 33 seconds
# # 900 = 40 seconds
# # 1000 = 46 seconds



#with game over function removed:
# 1000 games = 12 seconds = 1.2 seconds per 100
# 12.5
