## Project: AI Algorithm Comparison
I am creating a snake bot that uses a GUI control system with drop down menus to switch up the graphing method of the project. I want to experiment with Q-learning, sarsa, deep q learning, and try to wire the fruit fly connectome  to play snake. 


This repository serves as the template for your course project. Below is an explanation of the structure of the project and the purpose of each file. Your project must retain this basic structure. As you progress, you should add details about your specific project to this readme (e.g., Replace "This file will contain the implementations of the AI algorithms/agents used in your project" with "This file contains the implementations of the X, Y, and Z algorithms..."). 
## Start Demo

![Start demo](start_training.png)
---


### 1. `algorithms.py`
Algorithm.py contains the 
This file will contain the implementations of the AI algorithms/agents used in your project.  
- Ensure your code is well-documented with comments explaining each algorithm.

### 2. `comparisons.py`  
I splurged and made a GUI, so comparisons.py functionality will be handled through the gui.

![Start demo](snake_graph.png)


### 3. `demo.py`  
This file stores the GUI of my snake game. Pressing start training starts training. It also resets training right now. Still has some things that need adjusting, but these are quick fixes that will be separate from the main project. The biggest hurdle was setting up the GUI and embedding the graph. 


#### Submission Requirements:
- **Progress Report:** Demonstrate *random agents* attempting to solve each problem.  
- **Final Report:** Demonstrate *each algorithm* attempting to solve at least one problem.  

#### Guidelines for Demonstrations:
Keep the demonstrations concise but meaningful to highlight key behaviors. Some agent types (e.g., random agents) may struggle or fail to solve a problem. Some problems may take a long time to complete (e.g., a full game of chess). In such cases, you should cut off the demonstration after a representative sample of the agent's behavior and problem mechanics has been shown. 

### 4. `problems.py`  
This file will contain the implementation of the problems you are solving with your AI algorithms.  
- Ensure that the problems are clearly defined and modular, so the algorithms can be easily tested on each.  
- For the **progress report**, this file should be fully implemented and require no major edits afterward.

---

## Instructions for Students

### Step 0: Prepare Python Environment
These instructions will setup the evaluation environment we will use to evaluate your project. Use this environment (without addition or modification) to make sure your code will run the same on our machines.
- Download and install [Anaconda](https://www.anaconda.com/download)
- Open Terminal (or Anaconda prompt in Windows)
- `conda create --name evalenv python=3.9`
- `conda activate evalenv`
- `pip install --upgrade pip`
- `pip install -r requirements.txt`
