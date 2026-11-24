


import threading
import multiprocessing

import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("Complete Your Profile")
root.resizable(False, False)

# https://github.com/ua-ista-455/applied-nlp-fa26-pre-trained-lm-jabo25.git
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



def start_training():
    training_thread = threading.Thread(
        target=sn.run,
        args=(True,)
    )

    training_thread.start()

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
        start_training()
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

# showGame = ttk.Button(button_frame, text="show")
# def replay_game(canvas):
#     """Renders the last recorded game state to the provided Tkinter Canvas."""
#     canvas.delete("all")  # Clear previous frame

#     # Access your stored history
#     snake_hist = sn.agent.snakeHistory
#     apple_hist = sn.agent.appleHistory
#     score_hist = sn.agent.scoreHistory

#     if not snake_hist or not apple_hist:
#         canvas.create_text(
#             canvas.winfo_width() // 2,
#             canvas.winfo_height() // 2,
#             text="No game history to replay",
#             font=("Arial", 12),
#             fill="white"
#         )
#         return

#     # Render the final state (instant)
#     final_snake = snake_hist[-1]
#     final_apple = apple_hist[-1]
#     final_score = score_hist[-1] if score_hist else 0

#     # Draw Apple
#     ax, ay = final_apple
#     size = sn.SQUARE_SIZE[0]
#     canvas.create_rectangle(
#         ax * size, ay * size,
#         (ax + 1) * size, (ay + 1) * size,
#         fill="#FF0000", outline="black"
#     )

#     # Draw Snake
#     for seg in final_snake:
#         sx, sy = seg
#         canvas.create_rectangle(
#             sx * size, sy * size,
#             (sx + 1) * size, (sy + 1) * size,
#             fill="#00FF00", outline="black"
#         )

#     # Update score label (if it exists in sn module)
#     if hasattr(sn, 'label'):
#         sn.label.config(text=f"Score: {final_score}")



# showGame = ttk.Button(button_frame, text="show training", command=button)

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



def renderSnake(x,y, remove):
    print(x,y)
    # global  sn.color, canvas_rects, apple_rect_id, apple
    apple = sn.apple

    #evaluate for render glitch with apple generation removal. after eaten

    
   #add squares back
    pixel_x = sn.SQUARE_SIZE[0] * x
    pixel_y = sn.SQUARE_SIZE[1] * y

    if not remove:  #EATEN keep square
        rect_id = sn.canvas.create_rectangle(
            pixel_x,
            pixel_y,
            pixel_x + sn.SQUARE_SIZE[0],
            pixel_y + sn.SQUARE_SIZE[1],
            fill=sn.SNAKE_COLOR
        )
        sn.canvas_rects[(x, y)] = rect_id


        # apple removal
        pixel_x = sn.SQUARE_SIZE[0] * apple[0]
        pixel_y = sn.SQUARE_SIZE[1] * apple[1]
        apple_rect_id = sn.canvas.create_rectangle(
        pixel_x, pixel_y,
        pixel_x + sn.SQUARE_SIZE[0], pixel_y + sn.SQUARE_SIZE[1],
        fill=sn.FOOD_COLOR)
        rect_id = sn.canvas_rects.pop((apple[0], apple[1]), None)


    else:#DIDN'T EAT remove square
        # pygame.draw.rect(surface, (0,0,0), rect)
        rect_id = sn.canvas_rects.pop((x, y), None)
        
        #make new snake seg
        sn.canvas.create_rectangle(
            pixel_x,
            pixel_y,
            pixel_x + sn.SQUARE_SIZE[0],
            pixel_y + sn.SQUARE_SIZE[1],
            fill=sn.BG_COLOR,
            outline=sn.BG_COLOR
        )
        if rect_id is not None:
            sn.canvas.delete(rect_id)
        
        #make apple
        if remove:
                        # apple removal
            pixel_x = sn.SQUARE_SIZE[0] * apple[0]
            pixel_y = sn.SQUARE_SIZE[1] * apple[1]
            apple_rect_id = sn.canvas.create_rectangle(
            pixel_x, pixel_y,
            pixel_x + sn.SQUARE_SIZE[0], pixel_y + sn.SQUARE_SIZE[1],
            fill=sn.FOOD_COLOR)
            rect_id = sn.canvas_rects.pop((apple[0], apple[1]), None)
        # root.after(0, lambda: sn.label.config(text=f"Score: {sn.score} game total:{sn.gameTotal}"))


#runAnimation was coded by AI. I am writing this so prof knows
#this one uses my render snake function I coded. 
# The old renderSnake did not use my code
# I have to reconfigure my entire archetecture of my game to optimize for speed
# def runAnimation(canvas, step=0, snake_state=None, frame_count=None):
#     agent = sn.agent

#     if frame_count is None:
#         frame_count = min(
#             len(agent.snakeHistory),
#             len(agent.appleHistory),
#             len(agent.directionHistory),
#         )

#     if frame_count == 0:
#         canvas.delete("all")
#         canvas.create_text(
#             (canvas.winfo_width() or 600) / 2,
#             (canvas.winfo_height() or 600) / 2,
#             text="No game history to replay",
#             fill="white",
#         )
#         return

#     if step >= frame_count:
#         canvas.create_text(
#             (canvas.winfo_width() or 600) / 2,
#             (canvas.winfo_height() or 600) / 2,
#             text="Replay Complete",
#             fill="white",
#             font=("Arial", 12),
#         )
#         return

#     if snake_state is None:
#         current_snake = [
#             tuple(segment) for segment in agent.snakeHistory[step]
#         ]
#     else:
#         current_snake = list(snake_state)

#     canvas.delete("all")
#     sn.canvas_rects.clear()
#     apple_rect_id = None

#     def draw_segment(x, y):
#         nonlocal apple_rect_id

#         if apple_rect_id is not None:
#             canvas.delete(apple_rect_id)

#         before = set(canvas.find_all())
#         renderSnake(x, y, False)

#         for item_id in set(canvas.find_all()) - before:
#             if (
#                 canvas.type(item_id) == "rectangle"
#                 and canvas.itemcget(item_id, "fill") == sn.FOOD_COLOR
#             ):
#                 apple_rect_id = item_id

#     saved_apple = sn.apple
#     sn.apple = agent.appleHistory[step]
#     try:
#         # Draw body segments directly (renderSnake only draws head + apple)
#         for sx, sy in current_snake[1:]:
#             pixel_x = sn.SQUARE_SIZE[0] * sx
#             pixel_y = sn.SQUARE_SIZE[1] * sy
#             canvas.create_rectangle(
#                 pixel_x, pixel_y,
#                 pixel_x + sn.SQUARE_SIZE[0], pixel_y + sn.SQUARE_SIZE[1],
#                 fill=sn.SNAKE_COLOR, outline="black"
#             )

#         # Call renderSnake once for the head (it draws head + apple)
#         if current_snake:
#             hx, hy = current_snake[0]
#             draw_segment(hx, hy)
#     finally:
#         sn.apple = saved_apple

#     if step + 1 >= frame_count:
#         canvas.after(
#             100,
#             lambda: canvas.create_text(
#                 (canvas.winfo_width() or 600) / 2,
#                 (canvas.winfo_height() or 600) / 2,
#                 text="Replay Complete",
#                 fill="white",
#                 font=("Arial", 12),
#             ),
#         )
#         return

#     next_apple = agent.appleHistory[step + 1]
#     apple_changed = next_apple != agent.appleHistory[step]
#     previous_score = None
#     next_score = None
#     next_reset = False

#     if len(agent.scoreHistory) > step + 1:
#         previous_score = agent.scoreHistory[step]
#         next_score = agent.scoreHistory[step + 1]
#         next_reset = next_score < previous_score or (
#             apple_changed and next_score <= previous_score
#         )

#     has_step_counts = len(agent.stepsSinceLastApple) > step + 1
#     if (
#         not next_reset
#         and has_step_counts
#         and agent.stepsSinceLastApple[step] > 0
#         and agent.stepsSinceLastApple[step + 1] == 0
#         and (next_score is None or next_score <= previous_score)
#     ):
#         next_reset = True

#     duplicate_start = (
#         not apple_changed
#         and previous_score is not None
#         and next_score == previous_score
#         and has_step_counts
#         and agent.stepsSinceLastApple[step] == 0
#         and agent.stepsSinceLastApple[step + 1] == 0
#     )

#     dx, dy = agent.directionHistory[step]
#     next_head = (current_snake[0][0] + dx, current_snake[0][1] + dy)
#     moved_snake = [next_head] + current_snake

#     if not apple_changed:
#         moved_snake.pop()

#     collided = (
#         next_head[0] < 0
#         or next_head[0] >= sn.GRID_SIZE[0]
#         or next_head[1] < 0
#         or next_head[1] >= sn.GRID_SIZE[1]
#         or next_head in moved_snake[1:]
#     )
#     next_reset = next_reset or collided

#     if next_reset:
#         next_snake = [
#             tuple(segment) for segment in agent.snakeHistory[step + 1]
#         ]
#     elif duplicate_start:
#         next_snake = current_snake
#     else:
#         next_snake = moved_snake

#     canvas.after(
#         100,
#         lambda s=step + 1, state=next_snake, count=frame_count:
#             runAnimation(canvas, s, state, count),
#     )

def runAnimation(canvas, step=0, frames=None):
    agent = sn.agent

    if frames is None:
        frames = []

        def append_game(snake_history, apple_history, direction_history):
            count = min(
                len(snake_history),
                len(apple_history),
                len(direction_history),
            )
            if count == 0:
                return

            if snake_history[0]:
                current_snake = [
                    tuple(segment) for segment in snake_history[0]
                ]
            else:
                current_snake = [
                    (sn.GRID_SIZE[0] / 2, sn.GRID_SIZE[1] / 2)
                ]

            for index in range(count):
                # start() records the initial snake before run() records it again.
                if index == 1:
                    pass
                elif index > 1:
                    dx, dy = direction_history[index - 1]
                    apple_was_eaten = (
                        apple_history[index] != apple_history[index - 1]
                    )
                    moved_snake = [
                        (current_snake[0][0] + dx, current_snake[0][1] + dy)
                    ] + current_snake

                    if not apple_was_eaten:
                        moved_snake.pop()

                    current_snake = moved_snake

                frames.append(
                    (tuple(current_snake), tuple(apple_history[index]))
                )

        for game in agent.GameHistory:
            if not game.empty:
                append_game(
                    list(game["snake"]),
                    list(game["apple"]),
                    list(game["direction"]),
                )

        append_game(
            list(agent.snakeHistory),
            list(agent.appleHistory),
            list(agent.directionHistory),
        )

    if not frames:
        canvas.delete("all")
        canvas.create_text(
            (canvas.winfo_width() or 600) / 2,
            (canvas.winfo_height() or 600) / 2,
            text="No game history to replay",
            fill="white",
        )
        return

    if step >= len(frames):
        canvas.create_text(
            (canvas.winfo_width() or 600) / 2,
            (canvas.winfo_height() or 600) / 2,
            text="Replay Complete",
            fill="white",
            font=("Arial", 12),
        )
        return

    current_snake, apple = frames[step]

    canvas.delete("all")
    sn.canvas_rects.clear()
    size_x, size_y = sn.SQUARE_SIZE

    # Draw the body; renderSnake draws the head and apple.
    for sx, sy in current_snake[1:]:
        canvas.create_rectangle(
            sx * size_x,
            sy * size_y,
            (sx + 1) * size_x,
            (sy + 1) * size_y,
            fill=sn.SNAKE_COLOR,
            outline="black",
        )

    saved_apple = sn.apple
    sn.apple = apple
    try:
        hx, hy = current_snake[0]
        renderSnake(hx, hy, False)
    finally:
        sn.apple = saved_apple

    if step + 1 < len(frames):
        canvas.after(
            100,
            lambda s=step + 1, saved_frames=frames:
                runAnimation(canvas, s, saved_frames),
        )
    else:
        canvas.after(
            100,
            lambda: canvas.create_text(
                (canvas.winfo_width() or 600) / 2,
                (canvas.winfo_height() or 600) / 2,
                text="Replay Complete",
                fill="white",
                font=("Arial", 12),
            ),
        )


def on_replay():
    
    runAnimation(sn.canvas, step=0)
    # pass



showGame = ttk.Button(button_frame, text="Replay", command=on_replay)
# showGame = ttk.Button(button_frame, text="show training", command=lambda: runAnimation(sn.canvas))
showGame.grid(row=0, column=3, padx=(80, 30), pady=5)   


# showGame = ttk.Button(button_frame, text="show training", command=button)
# showGame.grid(row=0, column=3, padx=(80, 30), pady=5) 







# showGame = ttk.Button(button_frame, text="show training", command=button)
# showGame.grid(row=0, column=3, padx=7, pady=5)
# showGame = ttk.Button(root, text="Hide Game Play", command = button)
# showGame.grid(row=7, column=5, columnspan=2, padx=1, pady=5, sticky=tk.W)


# def updateGUI():
#     sn.label.config(
#         text=f"Score: {sn.score} game total: {sn.gameTotal}"
#     )

#     root.after(100, updateGUI)


# def start_training():
#     training_thread = threading.Thread(
#         target=sn.run,
#         args=(True,),
#         daemon=True
#     )

#     training_thread.start()

#     updateGUI()


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


    # return plot_frame
    # pass



if sn.gameTotal == 0 :
    plot()
# if(sn.gameOver):
    # plot_canvas.draw_idle()
    # plot()


root.mainloop()
# t2 = threading.Thread(target=root.mainloop())
# t2.start() 





#the plan for this:
    # have a create new agent button
    # the new agent button adds an agent onto a list. 
    # the start training trains that agent. 
    # and the stats will be handled. 
    # for a prototype agent, what I need to do is Um,,,,
