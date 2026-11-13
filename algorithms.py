
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
    # if(snake_clone == None):
        # head = snake[0]
        # tail = snake[-1]
        # snake.pop()
        # snake.insert(0, (head[0]+direction[0], head[1]+direction[1]))
        # if(show):
            # renderSnake(snake[0][0],snake[0][1], False)
        # return snake
    # else:
        head = snake_clone[0]
        tail = snake_clone[-1]
        tail = snake_clone[-1]
        snake_clone.pop()
        snake_clone.insert(0, (head[0]+dir_clone[0], head[1]+dir_clone[1]))
        # if(show):
            # renderSnake(snake[0][0],snake[0][1], False)
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
            

class player: 
    def __init__(self, agentType=None, averageScore=0, name=None):
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
        # plt.show(block=False)

    
    def addStats(self, snake, apple, stepCount, score, direction):
        # global df, snakeHistory, appleHistory, stepsSinceLastApple, score, stepCount, directionHistory, direction, snake, apple 
        self.snakeHistory.append(snake)
        self.appleHistory.append(apple)
        self.stepsSinceLastApple.append(stepCount)
        self.scoreHistory.append(score)
        self.directionHistory.append(direction)
        self.foodDistance.append(abs(snake[0][0]-apple[0]) + abs(snake[0][1]-apple[1]))
        

    def getDistance(self,direction):
        apple = self.appleHistory[-1]
        snake = self.snakeHistory[-1][0]        
        snake = (snake[0]+direction[0], snake[1]+direction[1])
        return abs(abs(snake[0]-apple[0]) + abs(snake[1]-apple[1]))


    def getDirection(self):
        # if(len(self.directionHistory) == 0):
        #     return (0,1)
        snake = self.snakeHistory[-1]
        direction = self.directionHistory[-1]
        inverseDir = (direction[0]*-1,direction[1]*-1)
        options = []
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
        
        min = 99999999999999
        for x,y in zip(options, directionList):
            if min> x:
                min = x
                direction = y
        if(len(options) == 0):
            return (0,1)
        return direction

    # def makePlot(self):
    #     # the figure that will contain the plot
    #     fig = Figure(figsize = (5, 5),
    #                 dpi = 100)
    #     plot1 = fig.add_subplot(111)


    #     # plt.pyplot.plot(title = "score", scalex=True, scaley=True, data=self.finalScoreList,)
    #     games = list(range(len(self.finalScoreList)))

        
        
    #     # self.fig, self.ax = plt.subplots()
    #     plot1.plot([], [], label="Score")
        
    #     # 3. Setup static labels once
    #     plot1.set_title("Score")
    #     plot1.set_xlabel("Game")
    #     plot1.set_ylabel("Score")
    #     plot1.set_data(games,self.finalScoreList)
    #     plot1.relim()
    #     plot1.autoscale_view()
    #     # plot1.set_ydata()
        


    #     # 6. Adjust the axis limits dynamically so everything stays in view
    #     if self.finalScoreList:
    #         plot1.set_xlim(0, max(1, len(self.finalScoreList) - 1))
    #         plot1.set_ylim(min(self.finalScoreList) - 1, max(self.finalScoreList) + 1)
    #         # plot1.set_xlim(0, max(1, len(self.finalScoreList) - 1))
    #         # plot1.set_ylim(min(self.finalScoreList) - 1, max(self.finalScoreList) + 1)
            

    #     # 7. Redraw the canvas and flush the GUI events to render the change
    #     fig.canvas.draw()
    #     fig.canvas.flush_events()
    #     return fig

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
        self.finalScoreList.append(self.scoreHistory[-1])
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
        return self.makePlot()

    # @might remove this line might be pointless. 
        # while(len(self.snakeHistory) != 0):
        #     self.snakeHistory.pop()
        #     self.appleHistory.pop()
        #     self.stepsSinceLastApple.pop()
        #     self.scoreHistory.pop()
        #     self.directionHistory.pop()
        #     self.foodDistance.pop()
         
                
        



# class Qlearning(player):
#     def bark(self):
#         return
# class SARSA(player):
#     def test():
#         return
# class fruitfly(player):
#     def test():
#         return




#     def updateStats():
#         print("this method is to update the player stats and upload it to the player object")

#     #this method is to update the direction the player is moving iisory
#     def getMove():
#         snake_copy.foodDistance.append(abs(snake[0][0]-apple[0]) + abs(snake[0][1]-apple[1]))
#         return direction

# class MyClass:
#     def __init__(self, attribute1, attribute2):
#         """
#         Initialize the class
#         """
#         self.attribute1 = attribute1
#         self.attribute2 = attribute2

#     def method1(self):
#         """
#         Description of method1.
#         """
#         pass

#     def method2(self, parameter):
#         """
#         Description of method2.
#         """
#         pass

#     def __str__(self):
#         """
#         Return a readable string representation.
#         """
#         return f"MyClass({self.attribute1}, {self.attribute2})"


# # Create an instance
# my_object = MyClass(value1, value2)

# # Call methods
# my_object.method1()
# my_object.method2(parameter)





    # def makePlot(self):
    #         # the figure that will contain the plot

    #     # plt.pyplot.plot(title = "score", scalex=True, scaley=True, data=self.finalScoreList,)
    #     games = list(range(len(self.finalScoreList)))


    #     # 5. Update the existing line's data instead of drawing a new one
    #     self.line.set_xdata(games)
    #     self.line.set_ydata(self.finalScoreList)

    #     # 6. Adjust the axis limits dynamically so everything stays in view
    #     if self.finalScoreList:
    #         self.ax.set_xlim(0, max(1, len(self.finalScoreList) - 1))
    #         self.ax.set_ylim(min(self.finalScoreList) - 1, max(self.finalScoreList) + 1)

    #     # 7. Redraw the canvas and flush the GUI events to render the change
    #     self.fig.canvas.draw()
    #     self.fig.canvas.flush_events()
