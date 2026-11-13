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
    import snake_copy as sn
finally:
    tk.Tk = tk_root_factory
    tk.Label = tk_label_factory
    tk.Canvas = tk_canvas_factory
    root.mainloop = root_mainloop

root.title("Complete Your Profile")
setScreenSize = False
Speed = tk.Scale(root, from_=0, to=42, orient = tk.HORIZONTAL)
Speed.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
tk.Label(root, text="Speed:", ).grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)


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

    if epochs.get() != "":
        sn.EPOCHS = epochs.get()
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
    




# Grid size dropdown
tk.Label( root, text="Grid size:",).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

grid_size = ttk.Combobox( root,
    values=["Small", "Medium", "Large", "Extra Large"],
    state="readonly",
)
grid_size.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)




# Training Algorithm dropdown
tk.Label(root, text="Algorithm:",).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
eye_color = ttk.Combobox(root, values=["Fruit Fly", "Epsilon greedy", "Q-learining", "Modified Q learning", "NN"],state="readonly",)
eye_color.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# Height entry
tk.Label(root, text="Epsilon:", ).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
Epsilon = ttk.Entry(root)
Epsilon.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Epochs entry
tk.Label(root,text="epochs:",).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
epochs = ttk.Entry(root)
epochs.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)


# gama entry
tk.Label(root, text="Gamma:", ).grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
Gamma = ttk.Entry(root)
Gamma.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

# game total
tk.Label(root, text="Game Total:", ).grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
gameTotal = ttk.Entry(root)
gameTotal.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)


# reset buton
reset = ttk.Button(root, text="Reset",)
reset.grid(row=7, column=0, padx=5, pady=10, sticky=tk.W)

#stop training
stop = ttk.Button(root, text="Stop Training",)
stop.grid(row=7, column=1, padx=5, pady=10, sticky=tk.W)

#start training button
start = ttk.Button(root, command=setScreenSize, text="Start Training",)
start.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky=tk.W)


#start training button
def button():
    setattr(sn, "show", not sn.show)
    if(not sn.show):
        showGame.config(text="Show Gameplay")
    else:
        showGame.config(text="Hide Game Play")
    
showGame = ttk.Button(root, text="Hide Game Play", command = button)


showGame.grid(row=7, column=4, columnspan=2, padx=5, pady=5, sticky=tk.W)



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


