import threading
import multiprocessing

import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("Complete Your Profile")
root.resizable(False, False)



from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import threading
import time
startedGameLoop = False #tells to start game loop vs reset game

# Keep all form fields on the left
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=0)

game_frame = ttk.Frame(root)
game_frame.grid(row=0, column=3, rowspan=7, padx=20, pady=10)

# snake_copy creates its own Tk window and enters mainloop during import.
# Route those calls into this GUI so its game canvas is embedded here.
tk_root_factory = tk.Tk
tk_label_factory = tk.Label
tk_canvas_factory = tk.Canvas
root_mainloop = root.mainloop

def embedded_root(*args, **kwargs):
    return root

def embedded_label(master=None, *args, **kwargs):
    if master is root:
        master = game_frame
    return tk_label_factory(master, *args, **kwargs)

def embedded_canvas(master=None, *args, **kwargs):
    if master is root:
        master = game_frame
    return tk_canvas_factory(master, *args, **kwargs)

tk.Tk = embedded_root
tk.Label = embedded_label
tk.Canvas = embedded_canvas
root.mainloop = lambda *args, **kwargs: None
try:
    import Algorithms as sn
finally:
    tk.Tk = tk_root_factory
    tk.Label = tk_label_factory
    tk.Canvas = tk_canvas_factory
    root.mainloop = root_mainloop

root.title("Complete Your Profile")
setScreenSize = False



def setScreenSize():
    global startedGameLoop
    if(grid_size.get() == "Small"):
        sn.GRID_SIZE = (4,4)
    if(grid_size.get() == "Medium"):
        sn.GRID_SIZE = (10,10)
    if(grid_size.get() == "Large"):
        sn.GRID_SIZE = (20,20)
    if(grid_size.get() == "Extra Large"):
        sn.GRID_SIZE = (50,50)
    sn.agent.norm = norm.get()

    if epochs.get() != "":
        sn.EPOCHS = int(epochs.get())
    if Gamma.get() != "":
        sn.GAMMA = epochs.get()    
    if Epsilon.get() != "":
        sn.EPSILON = epochs.get()        
    sn.SQUARE_SIZE = (sn.RESOLUTION[0]/(sn.GRID_SIZE[0]),sn.RESOLUTION[1]/(sn.GRID_SIZE[1])) #body seg size
    sn.snake = [(sn.GRID_SIZE[0]/2, sn.GRID_SIZE[1]/2)]
    sn.SPEED = Speed.get()
    # gameOver = False
    print(startedGameLoop, "not started")
    if(not startedGameLoop):
        sn.run(True)
        startedGameLoop = True
    else:
        sn.start()
        sn.gameOver = False
    


                                                                            #DROP DOWN MENU's



# Grid size dropdown.                   ROW 0                         CONTROLLER NAME = 
tk.Label( root, text="Grid size:",).grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
grid_size = ttk.Combobox( root, values=["Small", "Medium", "Large", "Extra Large"], state="readonly",)
grid_size.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
grid_size.set("Large")


# Training Algorithm dropdown.          ROW 1
tk.Label(root, text="Algorithm:",).grid(row=1, column=0, padx=3, pady=5, sticky=tk.W)
eye_color = ttk.Combobox(root, values=["Fruit Fly", "Epsilon greedy", "Q-learining", "Modified Q learning", "NN", "Distance Heuristic"],state="readonly",)
eye_color.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
eye_color.set("Distance Heuristic")

# norm dropdown.                         ROW 2
tk.Label(root, text="Norm:",).grid(row=2, column=0, padx=1, pady=1, sticky=tk.W)
norm = ttk.Combobox(root, values=["L1", "L2", "Infinity"], state="readonly")
norm.grid(row=2, column=1, padx=1, pady=1, sticky=tk.W)
norm.set("L2")




                                                                        # PARAM ENTRY BOXES


# Epochs entry.                        ROW 3
tk.Label(root,text="epochs:",).grid(row=3, column=0, padx=5, pady=3, sticky=tk.W)
epochs = ttk.Entry(root)
epochs.grid(row=3, column=1, padx=5, pady=3, sticky=tk.W)
epochs.insert(0, 100)

# game total                           ROW 4
tk.Label(root, text="games per\n epoch:(future)", ).grid(row=4, column=0, padx=5, pady=3, sticky=tk.W)
gameTotal = ttk.Entry(root)
gameTotal.grid(row=4, column=1, padx=5, pady=3, sticky=tk.W)



                                                                        # Slide controls
# Gamma.                               ROW 5
Gamma = tk.Scale(root, from_=0.0, to=1.0,    resolution=0.01, orient = tk.HORIZONTAL)
Gamma.grid(row=5, column=1, padx=5, pady=3, sticky=tk.W)
Gamma.set(0.1)
tk.Label(root, text="Gamma:", ).grid(row=5, column=0, padx=5, pady=3, sticky=tk.W)
Gamma.grid(row=5, column=1, padx=5, pady=4, sticky=tk.W)

# Epsilon                              ROW 6
Epsilon = tk.Scale(root, from_=0.0, to=1.0,    resolution=0.01,  orient = tk.HORIZONTAL)
Epsilon.grid(row=6, column=1, padx=5, pady=3, sticky=tk.W)
Epsilon.set(0.1)
tk.Label(root, text="Epsilon:", ).grid(row=6, column=0, padx=5, pady=3, sticky=tk.W)


# set Render Speed                      ROW 7
Speed = tk.Scale(root, from_=0, to=100, orient = tk.HORIZONTAL)
Speed.grid(row=7, column=1, padx=5, pady=3, sticky=tk.W)
tk.Label(root, text="Render Speed:", ).grid(row=7, column=0, padx=3, pady=5, sticky=tk.W)








                                                                #BOTTOM ROW BUTTONS HERE (ROW 8)
def updateParams():
    global startedGameLoop
    if epochs.get() != "":
        sn.EPOCHS = int(epochs.get())
    if Gamma.get() != "":
        sn.GAMMA = epochs.get()    
    if Epsilon.get() != "":
        sn.EPSILON = epochs.get()        
    sn.SPEED = Speed.get()

    sn.agent.norm = norm.get().lower()

    print("Updated norm:", sn.agent.norm)
    # gameOver = False

# reset buton                        ROW 8.               #command = reset (is in the snake file)

button_frame = ttk.Frame(root)
button_frame.grid(row=7, column=2, columnspan=4, sticky=tk.W, padx=5)

reset = ttk.Button(button_frame, text="Reset", command=sn.reset)
reset.grid(row=0, column=0, padx=3, pady=5)

stop = ttk.Button(button_frame, text="Update Params", command=updateParams)
stop.grid(row=0, column=2, padx=(65,10), pady=5)



start = ttk.Button(button_frame, text="Start Training", command=setScreenSize)
start.grid(row=0, column=1, padx=3, pady=5)


# reset = ttk.Button(root, text="Reset", command = sn.reset)
# reset.grid(row=7, column=2, padx=1, pady=5, sticky=tk.W)
# command=setScreenSize
# # tk.Label(root, text="Render Speed:", ).grid(row=7, column=2, padx=3, pady=5, sticky=tk.W)


# #stop training
# stop = ttk.Button(root, text="update params", command = updateParams)
# stop.grid(row=7, column=3, padx=1, pady=5, sticky=tk.W)

# #start training button
# start = ttk.Button(root, command=setScreenSize, text="Start Training",)
# start.grid(row=7, column=4, columnspan=2, padx=1, pady=5, sticky=tk.W)



#start training button
def button():
    setattr(sn, "show", not sn.show)
    if(not sn.show):
        showGame.config(text="Show Gameplay")
    else:
        showGame.config(text="Hide Game Play")

showGame = ttk.Button(button_frame, text="Hide Game Play", command=button)
showGame.grid(row=0, column=3, padx=(80, 30), pady=5)    
showGame = ttk.Button(button_frame, text="Hide Game Play", command=button)
# showGame.grid(row=0, column=3, padx=7, pady=5)
# showGame = ttk.Button(root, text="Hide Game Play", command = button)
# showGame.grid(row=7, column=5, columnspan=2, padx=1, pady=5, sticky=tk.W)





# plot function is created for 
# plotting the graph in 
# tkinter window
def plot():

    
    plot_frame = ttk.Frame(root)  #attach plot frame to main window
    
    fig = sn.agent.fig
    canvas = FigureCanvasTkAgg(fig, master = plot_frame)  ##attach the plot to a canvas
    canvas.draw()
    # # canvas.draw_idle()

    # # # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # # # creating the Matplotlib toolbar
    # toolbar = NavigationToolbar2Tk(canvas,
    #                                plot_frame)
    # toolbar.update()
    plot_frame.grid(row=0, column=4, rowspan=7, padx=20, pady=10)


    return plot_frame



plot()
if(sn.gameOver):
    # plot_canvas.draw_idle()
    plot()



t2 = threading.Thread(target=root.mainloop())
t2.start()


