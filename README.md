## Project: AI Algorithm Comparison
I am creating a snake bot that uses a GUI control system with drop-down menus to switch up the graphing method of the project. I want to experiment with Q-learning, sarsa, deep q learning, and try to wire the fruit fly connectome  to play snake. 



## Start Demo 
#(algorithm selection button doesn't do anything now) 
Should run 100 rounds of snake (YOU DON'T WATCH THE ENTIRE THING)
Start training also resets the game board if you want to change board sizes. The hide gameplay button is also functional. 
![Start demo](start_training.png)
---


### 1. `algorithms.py`
My game loop is a nightmare and the next big thing I'm fixing. I initially coded it in pygame before realizing I couldn't embed pygame into tkinter because pygame and tkinter both wanted to hog the main OS thread; without multithreading, the pygame loop stops tkinter from refreshing. I spent a day converting the loop to run in tkinter. However, tkinter is a bottleneck and loops slowly. I plan on converting the loops to python and having a function that animates the states of the array for me. 

### 2. `comparisons.py`  
I splurged and made a GUI, so comparisons.py functionality will be handled through the gui.

![Start demo](snake_graph.png)


### 3. `demo.py`  
This file stores the GUI of my snake game. Pressing start training starts training. It also resets training right now. Still has some things that need adjusting, but these are quick fixes that will be separate from the main project. The biggest hurdle was setting up the GUI and embedding the graph. There is one bug that causes parts of the snake to not get animated during parts of the game, but it does not effect the physics of the game. 


### 4. `problems.py`  
Algorithm.py contains the agent object that controls the game. I wanted to set it up so that the agent had access to a bunch of game stats from the main file, and then, I could use inheritance to change the agent function. Ideally, I have the GUI spawn an agent and then pass the agent to the other file. There is a bug where when the apple is above the snake, the snake goes away from the apple before turning around and moving back towards the apple after it is made rational by running into a wall. 





###Reflection 
If I don't have enough commits, I don't think AI would opt to try doing multithreaded programing to get embedding a game into a gui. 
