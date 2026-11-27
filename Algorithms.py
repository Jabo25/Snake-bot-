
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
import random
root = tk.Tk()
#maybe make an object called a game to store the local game stats. 

# set environment constants
GRID_SIZE = (10,10)
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

apple = ()
#has eaten an apple and gets score
def hasEaten(snake_copy, apple):
    if snake_copy[0] == apple:
        return True
    else:
        return False
    
    # 200 at 5000 400 max 10k


# 20 sewcs second 2000
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
        # self.foodDistance = []
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
        # self.foodDistance.append(abs(snake[0][0]-apple[0]) + abs(snake[0][1]-apple[1]))
        
    def resetPlayer(self):
        self.snakeHistory.clear()
        self.appleHistory.clear()
        self.stepsSinceLastApple.clear()
        self.scoreHistory.clear()
        self.directionHistory.clear()
        # self.foodDistance.clear()

    def getDistance(self,direction):
        apple = self.appleHistory[-1]
        snake = self.snakeHistory[-1][0]        
        snake = (snake[0]+direction[0], snake[1]+direction[1])
        # return abs(abs(snake[0]-apple[0])**2 + abs(snake[1]-apple[1])**2)
        if self.norm == "L1":
            return abs(abs(snake[0] - apple[0]) +  abs(snake[1] - apple[1]))
        elif self.norm == "L2":
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
# 18 seconds vs 15. secs--long = 26 secs vs 16 w new way
        # self.resetPlayer()#might cause major bug later
        # if len(self.scoreHistory) !=0:
            # if self.gameTotal % 10 == 0:
            # threading.Thread(target=self.makePlot).start()
                # self.makePlot()
            # self.makePlot()
        # self.resetPlayer()#resets the player at the end of the game new function might be needed here
        # else:
            # self.fig

        self.resetPlayer()

        # return self.makePlot()
        
        # pass

        # second 2000 = 30 seconds
        







# params:
    # 1. Q(S, A)
    # 2. alpha
    # 3. Furure reward
    # 4. discounted future reward (gama)
    # best action value pair of next state
    # immidiate reward
    # action value of curr state

        # Q_table[current_state, action] += learning_rate * 
        # (reward + discount_factor * np.max(Q_table[next_state]) - Q_table[current_state, action])

    # Q(S_t, A_t) ← Q(S_t, A_t) + α[R_(t+1) + γ max_a (Q(S_(t+1), a) - Q(S_t, A_t))]

class Qlearning(player):

    # Reward (R ):                    R(x) = + or - 10 based on distance   --done
    # State Value (V):                V(s) = max Q(s,a)  --done
    # Action Value (Q):               Q(s,a) = E[R + γV(s')]      --done
    # Q-Learning Update Equation:     Q(s,a) = Q(s,a) + α[R + γ  V(s) - Q(s,a)]


    def __init__(self, agentType=None, averageScore=0, name=None):
        super().__init__(agentType="Qlearning", averageScore=averageScore, name=name)
        # Add any custom attributes you need here (e.g., tables, hyperparameters)            

        # NEW KEY PAIR CODE: dictionary_capitals['State'] = 'SA pair'
        self.actionTable = {} #makes a dictionary to store the q values
        # modified to work with q table
    def addStats(self, snake, apple, stepCount, score, direction):
        # super().addStats(snake, apple, stepCount, score, direction)
        super().addStats(snake, apple, stepCount, score, direction)

    #data structure that stores values needed
    class SA_Pair:
            
        def __init__(self, left,right,straight):
            #Values of actions 
            self.left = left
            self.right = right
            self.straight = straight
        def GetMaxDirection(self):
            if self.left > self.right and self.left > self.straight:
                return "left"
            elif self.right > self.left and self.right > self.straight:
                return "right"
            elif self.straight > self.left and self.straight > self.right:
                return "straight"
            else:
                # Handle ties
                return "tie"
    
    # tells the agent if direction is left right or straight
    def GlobalToLocalDir(self, newDirection):
        cur = self.directionHistory[-1]
        if cur == newDirection:
            return "straight"
        if cur == (0,1):
            if newDirection == (1,0):
                return "right"
            elif newDirection == (-1,0):
                return "left"
        elif cur == (0,-1):
            if newDirection == (-1, 0):
                return "right"
            elif newDirection == (1,0):
                return "left"
        elif cur == (1,0):
            if newDirection == (0, -1):
                return "right"
            elif newDirection == (0, 1):
                return "left"
        elif cur == (-1,0):
            if newDirection == (0, 1):
                return "right"
            elif newDirection == (0, -1):
                return "left"
        print("going straight debug statement")
        return "straight"


    def LocalToGlobalDir(self, newDirection):
        cur = self.directionHistory[-1]
        if "straight" == newDirection:
            return cur
        if cur == (0,1):
            if newDirection == "right":
                return (1,0)
            elif newDirection == "left":
                return (-1,0)
        elif cur == (0,-1):
            if newDirection == "right":
                return (-1, 0)
            elif newDirection == "left":
                return (1,0)
        elif cur == (1,0):
            if newDirection == "right":
                return (0, -1)
            elif newDirection == "left":
                return (0, 1)
        elif cur == (-1,0):
            if newDirection == "right":
                return (0, 1)
            elif newDirection == "left":
                return (0, -1)
        return cur


    # value of current state not needed i think. V(s) = max Q(s,a)
    def GetStateValue(self, snake):#--done

        #get the Q value 
        Q_value = self.actionTable.get((tuple(snake), tuple(self.appleHistory[-1]), snake[0]))

        #if it is a new state, (None) and populate Q table
        if(Q_value == None):
            self.actionTable[(tuple(snake), tuple(self.appleHistory[-1]), snake[0])] =  self.__class__.SA_Pair(0,0,0)
            Q_value = self.actionTable.get((tuple(snake), tuple(self.appleHistory[-1]), snake[0])) #

        #return the max value 
        return max(Q_value.right, Q_value.left, Q_value.straight) 

        # might be a bug on the returnof the function here


    # rework this function later
    # return the value of taking an action in state S                                # qpi(s,a)                                                  
    # (move snake clone and manually check score)
    #  Action Value (Q):               Q(s,a) = E[R + γV(s')]
    def GetActionValue(self, snake_copy): #get the direction
        # returns the future reward of next state
        Q_Table_Right, Q_Table_Left, Q_Table_Straight = 0,0,0

                #Get Straight, Right, and Left
        GoLeft = self.LocalToGlobalDir("left")
        GoRight = self.LocalToGlobalDir("right")
        GoStraight = self.LocalToGlobalDir("straight")

        #Get Action Values in all 3 directions    
        Q_Table_Left = self.GetStateValue(moveSnake(snake_copy,GoLeft))
        Q_Table_Right = self.GetStateValue(moveSnake(snake_copy, GoRight))
        Q_Table_Straight = self.GetStateValue(moveSnake(snake_copy,GoStraight))

        return self.__class__.SA_Pair(Q_Table_Left,Q_Table_Right,Q_Table_Straight) 

        # # what is the value of the move we just took
        # apple = self.appleHistory[-1] #get current apple location

        # reward = 0
        # if hasEaten(snake_copy, apple):    #eats
        #     reward =  10
        # elif collisionCheck(snake_copy): #death
        #     reward = -10

        # return self.GetStateValue(snake)


        # value = self.GetStateValue(snake_copy)
        # # gama = 0.1
        # # print(reward, "reward")
        # # print(value, "value")
        # return reward# + gama*value


    
    # #does reward after moving snake
    def GetNextReward(self,snake_copy):
        apple = self.appleHistory[-1] #get current apple location

        if hasEaten(snake_copy, apple):    #eats
            return 10
        elif collisionCheck(snake_copy): #death
            return -10
        else:
            return 0                #doesn't eat or die



    # retreive reward
    # retreive future reward                   currVal+ a[r+ ]
    # Q-Learning Update Equation:     Q(s,a) = Q(s,a) + α[R + γ max Q(s',a') - Q(s,a)]

# Reward (R ):                    R(x) = + or - 10 based on distance   --done
# State Value (V):                V(s) = max Q(s,a)  --done
# Action Value (Q):               Q(s,a) = E[R + γV(s')]      --done
# Q-Learning Update Equation:     Q(s,a) = Q(s,a) + α[R + γq(s',a') - Q(s,a)]

        # select the action
        # update the reward
        # then go
                                                        

        #  Q(s,a) = Q(s,a) + α[vpi(s) - Q(s,a)]
    def getDirection(self):
        # Write your own decision logic here
        # You still have access to self.snakeHistory, self.appleHistory, etc.
        # gama done in function
        snake = self.snakeHistory[-1]
        left, right, straight = 0, 0, 0

        # reward + future reward
        Qpi = self.GetStateValue(snake) #this is old_q
        actionValue = self.GetActionValue(snake) #this is next value

        learningRate = 0.1
        gama = 0.9

        R = 0
        explore = random.randint(0,100)
        decision = None
        # DirectionString = actionValue.GetMaxDirection()
        DirectionString = self.actionTable[(tuple(snake), tuple(self.appleHistory[-1]), snake[0])].GetMaxDirection()



        #  Qpi + alpha * (R + gama * Qprime-Qpi)

        # move the snake
        # calculate reward
        # add to the q table

        # move the snake
        if(explore < 10):                              # explore
            god = random.randint(1,3)
            counter = 0
            def GetRandom(counter=0, choice=None):
                R = 0
                god = ((choice+counter) % 3)+1
                if god == 1:
                    decision = self.LocalToGlobalDir("left")
                elif god == 2:
                    decision = self.LocalToGlobalDir("right")
                elif god == 3:
                    decision = self.LocalToGlobalDir("straight")
                R = self.GetNextReward(moveSnake(snake, decision)) #move snake in decided direction
                #try every other number combo
                if R < 0 and counter <= 4:
                    return GetRandom(counter+1, choice)
                return decision, R
            decision, R = GetRandom(counter,god)

        else: #exploit
            #calculate the reward -- we already know the direction, so one calculation

            if(DirectionString == "tie"):                                 #create tie breaker
                decision = super().getDirection()
            else:
                decision = self.LocalToGlobalDir(DirectionString)        #no tie breaker needed
            
            #calgculate total reward
            R = self.GetNextReward(moveSnake(snake,decision))

        #edit GlobalToLocal of the decision
        #last step: calculate reward and step for the new state being edited

        # move the snake 
        # get the rewaard
        
        # Q(S,A)←Q(S,A)+α(R+γQ(S′,A′)−Q(S,A))
        # get the td loss


        # old_q = selected_action_value
        # next_value = 0 if game_over else max(next_state_action_values)
        # new_q = old_q + alpha * (reward + gamma * next_value - old_q)




        DecisionString = self.GlobalToLocalDir(decision)
        key = (tuple(snake), tuple(self.appleHistory[-1]), snake[0])
        LearningStep = self.actionTable[key]

        old_q = getattr(LearningStep, DecisionString)
        next_value = getattr(actionValue, DecisionString)

        if R == -10:  # collision ends the episode
            next_value = 0

        new_q = old_q + learningRate * (R + gama * next_value - old_q)
        setattr(LearningStep, DecisionString, new_q)

        # DecisionString = self.GlobalToLocalDir(decision)
        # Vprime = max(actionValue.left, actionValue.right, actionValue.straight)
        # Qpi = Qpi + learningRate*(R+gama*Vprime-Qpi)
        # #this solution might ignore the action value of the exploration step but does calcualte the reward for this step
        # # actionTable.get()
        # LearningStep = self.actionTable.get((tuple(snake), tuple(self.appleHistory[-1]), snake[0]))
        # if(DecisionString == "right"):
        #     LearningStep.right = Qpi
        # elif(DecisionString == "left"):
        #     LearningStep.left = Qpi
        # elif(DecisionString == "straight"):
        #     LearningStep.straight = Qpi
        # else:
        #     raise RuntimeError("there is a major error on  get direction in Qlearning", DecisionString)
        
        # #set value to learned value 
        # self.actionTable[(tuple(snake), tuple(self.appleHistory[-1]), snake[0])] = LearningStep
        
        return decision


        

        # update the action value
        # if(DirectionString == "left"):
        #     left =  Qpi + learningRate*(R + gama*Qprime.left - Qpi)
        #     right = Qprime.right
        #     straight = Qprime.straight
        # elif(DirectionString == "right"):
        #     left =  Qprime.left
        #     right = Qpi + learningRate*(R + gama*Qprime.right - Qpi)
        #     straight = Qprime.straight
        # elif DirectionString == "straight":
        #     right = Qprime.right
        #     left =  Qprime.left
        #     straight = Qpi + learningRate*(R + gama*Qprime.straight - Qpi)

        
        # reward = self.__class__.SA_Pair(left,right,straight)
        # self.actionTable[((tuple(snake), tuple(self.appleHistory[-1]), tuple(snake[-1])))] = reward
        # return decision 
        










                #Get Straight, Right, and Left
        # GoLeft = self.LocalToGlobalDir("left")
        # GoRight = self.LocalToGlobalDir("right")
        # GoStraight = self.LocalToGlobalDir("straight")

        # #Get Action Values in all 3 directions    
        # Q_Table_Left = self.GetStateValue(moveSnake(snake_copy,GoLeft))
        # Q_Table_Right = self.GetStateValue(moveSnake(snake_copy, GoRight))
        # Q_Table_Straight = self.GetStateValue(moveSnake(snake_copy,GoStraight))



        # #move snake 
        # if(explore < 10):
        #         god = random.randint(1,3)
        #         decision = super().getDirection()
                
        # else:
        #         if DirectionString != "tie":
        #             decision =  self.LocalToGlobalDir(DirectionString)
        #             R = self.GetNextReward(moveSnake(snake, self.LocalToGlobalDir(DirectionString)))
        #         else:
        #             decision =  super().getDirection()#self.directionHistory[-1]
        #             R = self.GetNextReward(moveSnake(snake, super().getDirection()))

        # # MaxQprime = max(Qprime.left, Qprime.right, Qprime.straight)        

        
        # # Qpi + alpha * (R + gama * Qprime-Qpi)



    
                # if reward.left >reward.straight and reward.right > reward.straight:
                #     decision =  self.LocalToGlobalDir("straight")
                
                # elif reward.right > reward.left and  reward.straight > reward.left:
                #     decision =  self.LocalToGlobalDir("left")

                # elif reward.straight > reward.right and reward.left > reward.right:
                #     decision =  self.LocalToGlobalDir("right")
                # else:
                #     decision =  super().getDirection()#self.directionHistory[-1]

        



        
        
        # this has no directin safety so it can drive it into a wall. OOOPS 
        # QL will fix it? I hope
 
            



        

        # Q(S_t, A_t) ← Q(S_t, A_t) + α[R_(t+1) + γ max_a (Q(S_(t+1), a) - Q(S_t, A_t))]


        # pass



    def gameOver(self):
        # Add any end-of-game updates here (optional)
        super().gameOver()  # Keeps parent's score logging and resetPlayer()
        pass


        # how should I calculate the value of a state?

        # has snake eaten?
        # yes: + 10
        # no: 0
        # straight




    # #does reward after moving snake
    # def GetNextReward(self,snake_copy):
    #     apple = self.appleHistory[-1] #get current apple location

    #     if hasEaten(snake_copy, apple):    #eats
    #         return 10
    #     elif collisionCheck(snake_copy): #death
    #         return -10
    #     else:
    #         return 0                #doesn't eat or die


    # returns an int with the estimated value of the state 
    # mixed curr and future reward functions whcih could be problematic              # Qpi(s)
    # def GetReward(self, snake_copy):
    #     # how should I calculate the value of a state?

    #     # has snake eaten?
    #     # yes: + 10
    #     # no: 0
    #     if len(self.scoreHistory) >1: #get current reward
    #         if self.scoreHistory[-1] != self.scoreHistory[-2]:
    #             return 10
    #     if collisionCheck(snake_copy): #death
    #         return -10
    #     return 0 #nothing




# class Qlearning(player):
#     ACTIONS = ("left", "right", "straight")

#     def __init__(self, agentType=None, averageScore=0, name=None):
#         super().__init__(agentType="Qlearning", averageScore=averageScore, name=name)
#         self.actionTable = {}
#         self.learning_rate = 0.1
#         self.discount_factor = 0.9
#         self.epsilon = 0.1
#         self._pending_transition = None

#     class SA_Pair:
#         def __init__(self, left=0.0, right=0.0, straight=0.0):
#             self.left = left
#             self.right = right
#             self.straight = straight

#     def _state_key(self, snake, apple, direction):
#         return tuple(snake), tuple(apple), tuple(direction)

#     def _q_values(self, state_key):
#         values = self.actionTable.get(state_key)
#         if values is None:
#             values = self.SA_Pair()
#             self.actionTable[state_key] = values
#         return values

#     def _global_direction(self, action):
#         dx, dy = self.directionHistory[-1]
#         if action == "left":
#             return -dy, dx
#         if action == "right":
#             return dy, -dx
#         return dx, dy

#     def _update_pending(self, reward, next_state_key=None):
#         if self._pending_transition is None:
#             return

#         state_key, action, _ = self._pending_transition
#         values = self._q_values(state_key)
#         old_q = getattr(values, action)

#         next_value = 0.0
#         if next_state_key is not None:
#             next_values = self._q_values(next_state_key)
#             next_value = max(
#                 next_values.left,
#                 next_values.right,
#                 next_values.straight,
#             )

#         values_for_action = old_q + self.learning_rate * (
#             reward + self.discount_factor * next_value - old_q
#         )
#         setattr(values, action, values_for_action)
#         self._pending_transition = None

#     def getDirection(self):
#         if not (
#             self.snakeHistory
#             and self.appleHistory
#             and self.directionHistory
#             and self.scoreHistory
#         ):
#             raise RuntimeError("Q-learning needs recorded game state before choosing an action")

#         snake = self.snakeHistory[-1]
#         score = self.scoreHistory[-1]
#         state_key = self._state_key(
#             snake,
#             self.appleHistory[-1],
#             self.directionHistory[-1],
#         )

#         # Learn from the previous action using the actual state and score
#         # recorded by the game environment.
#         if self._pending_transition is not None:
#             _, _, previous_score = self._pending_transition
#             reward = score - previous_score
#             self._update_pending(reward, state_key)

#         values = self._q_values(state_key)

#         if random.random() < self.epsilon:
#             action = random.choice(self.ACTIONS)
#         else:
#             best_value = max(values.left, values.right, values.straight)
#             best_actions = [
#                 name for name in self.ACTIONS
#                 if getattr(values, name) == best_value
#             ]
#             action = random.choice(best_actions)

#         self._pending_transition = (state_key, action, score)
#         return self._global_direction(action)

#     def resetPlayer(self):
#         self._pending_transition = None
#         super().resetPlayer()

#     def gameOver(self):
#         # A collision ends the pending transition; do not bootstrap beyond it.
#         self._update_pending(-10)
#         super().gameOver()

# # #move all player stats into the player object
# # # game total
# # # first 100 games = 2.6 seconds
# # # 200 = 5.5-5 secondds ish
# # # 300 = 8 seconds
# # # 400 = 11 seconds
# # # 500 = 15 seconds
# # # 600 = 21 seconds
# # # 700 = 26 seconds
# # # 800 = 33 seconds
# # # 900 = 40 seconds
# # # 1000 = 46 seconds



# #with game over function removed:
# # 1000 games = 12 seconds = 1.2 seconds per 100
# # 12.5




#         # could be optimized to not edit memory and make new object each run
#                # action value and q table value 

# # two rewards:
#     # Reward value stored in the q table
#     # the reward value calcuated by snake movement
#         # 4 parts:
#             # 1) check state value. 
#             # 2) check state value of q table
#             # 3) check action value
#             # 4) check action value on the q table




                                            
class Qlearning(player):

    def __init__(self, agentType=None, averageScore=0, name=None):
        super().__init__(agentType="Qlearning", averageScore=averageScore, name=name)

        self.actionTable = {}

        # Epsilon decay
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995

        # Q-learning parameters
        self.learningRate = 0.1
        self.gamma = 0.9

    def addStats(self, snake, apple, stepCount, score, direction):
        super().addStats(snake, apple, stepCount, score, direction)

    class SA_Pair:
        def __init__(self, left=0, right=0, straight=0):
            self.left = left
            self.right = right
            self.straight = straight

        def GetMaxDirection(self):
            if self.left > self.right and self.left > self.straight:
                return "left"
            elif self.right > self.left and self.right > self.straight:
                return "right"
            elif self.straight > self.left and self.straight > self.right:
                return "straight"
            return "tie"

    def GlobalToLocalDir(self, newDirection):
        cur = self.directionHistory[-1]

        if cur == newDirection:
            return "straight"

        if cur == (0, 1):
            if newDirection == (1, 0):
                return "right"
            elif newDirection == (-1, 0):
                return "left"

        elif cur == (0, -1):
            if newDirection == (-1, 0):
                return "right"
            elif newDirection == (1, 0):
                return "left"

        elif cur == (1, 0):
            if newDirection == (0, -1):
                return "right"
            elif newDirection == (0, 1):
                return "left"

        elif cur == (-1, 0):
            if newDirection == (0, 1):
                return "right"
            elif newDirection == (0, -1):
                return "left"

        return "straight"

    def LocalToGlobalDir(self, newDirection):
        cur = self.directionHistory[-1]

        if newDirection == "straight":
            return cur

        if cur == (0, 1):
            if newDirection == "right":
                return (1, 0)
            elif newDirection == "left":
                return (-1, 0)

        elif cur == (0, -1):
            if newDirection == "right":
                return (-1, 0)
            elif newDirection == "left":
                return (1, 0)

        elif cur == (1, 0):
            if newDirection == "right":
                return (0, -1)
            elif newDirection == "left":
                return (0, 1)

        elif cur == (-1, 0):
            if newDirection == "right":
                return (0, 1)
            elif newDirection == "left":
                return (0, -1)

        return cur

    def GetStateValue(self, snake):
        key = (tuple(snake), tuple(self.appleHistory[-1]), snake[0])

        Q_value = self.actionTable.get(key)

        if Q_value is None:
            self.actionTable[key] = self.__class__.SA_Pair()
            Q_value = self.actionTable[key]

        return max(Q_value.right, Q_value.left, Q_value.straight)

    def GetActionValue(self, snake_copy):
        GoLeft = self.LocalToGlobalDir("left")
        GoRight = self.LocalToGlobalDir("right")
        GoStraight = self.LocalToGlobalDir("straight")

        Q_Table_Left = self.GetStateValue(moveSnake(snake_copy, GoLeft))
        Q_Table_Right = self.GetStateValue(moveSnake(snake_copy, GoRight))
        Q_Table_Straight = self.GetStateValue(moveSnake(snake_copy, GoStraight))

        return self.__class__.SA_Pair(
            Q_Table_Left,
            Q_Table_Right,
            Q_Table_Straight
        )

    def GetNextReward(self, snake_copy):
        apple = self.appleHistory[-1]

        if hasEaten(snake_copy, apple):
            return 10
        elif collisionCheck(snake_copy):
            return -10

        return 0

    def getDirection(self):

        snake = self.snakeHistory[-1]

        Qpi = self.GetStateValue(snake)
        actionValue = self.GetActionValue(snake)

        R = 0
        decision = None

        # Choose whether to explore or exploit
        explore = random.random()

        DirectionString = actionValue.GetMaxDirection()

        if explore < self.epsilon:

            # EXPLORE
            god = random.randint(1, 3)

            def GetRandom(c=0, choice=None):

                nonlocal R

                g = ((choice + c) % 3) + 1

                if g == 1:
                    decision = self.LocalToGlobalDir("left")
                elif g == 2:
                    decision = self.LocalToGlobalDir("right")
                else:
                    decision = self.LocalToGlobalDir("straight")

                R = self.GetNextReward(moveSnake(snake, decision))

                if R < 0 and c < 2:
                    return GetRandom(c + 1, choice)

                return decision, R

            decision, R = GetRandom(0, god)

        else:

            # EXPLOIT
            if DirectionString == "tie":
                decision = super().getDirection()
            else:
                decision = self.LocalToGlobalDir(DirectionString)

            R = self.GetNextReward(moveSnake(snake, decision))

        # Q-learning update
        DecisionString = self.GlobalToLocalDir(decision)

        key = (tuple(snake), tuple(self.appleHistory[-1]), snake[0])

        LearningStep = self.actionTable[key]

        old_q = getattr(LearningStep, DecisionString)

        next_value = getattr(actionValue, DecisionString)

        # Terminal state
        if R == -10:
            next_value = 0

        new_q = old_q + self.learningRate * (
            R + self.gamma * next_value - old_q
        )

        setattr(LearningStep, DecisionString, new_q)

        # EPSILON DECAY
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

        return decision

    def gameOver(self):
        super().gameOver()
