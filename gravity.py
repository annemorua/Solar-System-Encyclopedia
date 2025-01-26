import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
from project import calculate_time, calculate_velocity

#Contains for each celestial body its gravitational acceleration.
bodies = {"mercury": {"coords": (290, 50), "acceleration": 3.7},
    "venus": {"coords": (290, 50), "acceleration": 8.87},
    "earth": {"coords": (290, 50), "acceleration": 9.81},
    "mars": {"coords": (290, 50), "acceleration": 3.73},
    "jupiter": {"coords": (290, 50), "acceleration": 24.79},
    "saturn": {"coords": (290, 50), "acceleration": 10.44},
    "uranus": {"coords": (290, 50), "acceleration": 8.87},
    "neptune": {"coords": (290, 50), "acceleration": 11.15},
    "sun": {"coords": (290, 50), "acceleration": 274},
    "default": {"coords": (110, 50), "acceleration": 9.81}}

def setup_canvas(frame, planet):
    celestial2 = planet
    #Create a light blue canvas where the balls fall.
    canvas = tk.Canvas(frame, width=400, height=400, bg="skyblue")
    canvas.pack()
    #Creates a button that when clicked calls the "start_falling" function, which starts the balls falling.
    start_button = tk.Button(frame, text="Start", command=lambda: start_falling(canvas, img, "default", celestial2))
    start_button.pack()
    #Open the ball image.
    image = Image.open("images/headers/ball.png")
    image = image.resize((90, 90), Image.LANCZOS)
    img = ImageTk.PhotoImage(image)    #Converts the image into a format that can be used in a Tkinter Canvas.
    return canvas, img

balls = []    #Used to store references to the balls on the canvas.
def start_falling(canvas, img, celestial1, celestial2):
    global balls
    if balls:
        for ball in balls:
            canvas.delete(ball)    #Removes balls from the canvas.
    for body in bodies.values():
        body["velocity"] = 0    #Resets the velocity of all balls to 0.

    #Obtains the data of the two bodies to simulate.
    body1 = bodies[celestial1]
    body2 = bodies[celestial2]
    #Creates the images on the canvas at the coordinates obtained with the image of the ball.
    ball1 = canvas.create_image(*body1["coords"], image=img, anchor=tk.CENTER)
    ball2 = canvas.create_image(*body2["coords"], image=img, anchor=tk.CENTER)
    balls.extend([ball1, ball2])    #Add the two created balls to the balls list.

    fall(canvas, ball1, celestial1, ball2, celestial2)

def fall(canvas, ball1, celestial1, ball2, celestial2):
    coords1, coords2 = canvas.coords(ball1), canvas.coords(ball2)    #Gets the current coordinates of ball1 and ball2 on the canvas.
    #Check if any of the balls coordinates are not available to prevent errors if the coordinates do not exist.
    if not coords1 or not coords2:
        return None    #If the coordinates of any of the balls are not found, the function ends.

    y1, y2 = coords1[1], coords2[1]    #Assign the y-coordinate of ball1 and ball2 to the variables y1 and y2 respectively.
    body1, body2 = bodies[celestial1], bodies[celestial2]    #Access data on the two celestial bodies.

    #Check if the y coordinate of the ball is less than 350, if yes, the ball keeps falling.
    if y1 < 350:
        #Calculates the balls new velocity using the gravitational acceleration of its respective celestial body.
        #The value 0.05 is the time that has passed between each update.
        body1["velocity"] += body1["acceleration"] * 0.05
        #Move the ball on the canvas along the y-axis according to its calculated velocity. The value 0 means that it does not move on the x-axis.
        canvas.move(ball1, 0, body1["velocity"])

    if y2 < 350:
        body2["velocity"] += body2["acceleration"] * 0.05
        canvas.move(ball2, 0, body2["velocity"])

    #Check if any of the balls have speed. If at least one of the balls is moving the simulation continues.
    if body1["velocity"] or body2["velocity"]:
        canvas.after(50, fall, canvas, ball1, celestial1, ball2, celestial2)

def create_calculator(frame, planet, calc_type):
    body = bodies[planet]

    def calculate():
        try:
            height = entry.get()    #Gets the value entered by the user in the input field.
            if height == "":    #If the user has not entered any value, send an error message.
                messagebox.showerror("Error", "Please enter a numeric value.")
            else:
                height = float(height)
                #Checks if the requested calculation type is "time". If so, the decay time is calculated.
                if calc_type == "time":
                    result = calculate_time(height, body["acceleration"])    #Displays the result of the time calculation.
                    result_label.config(text=f"Time: {result:.2f} s", fg="black")
                else:
                    result = calculate_velocity(height, body["acceleration"])    #Displays the result of the velocity calculation.
                    result_label.config(text=f"Velocity: {result:.2f} m/s", fg="black")
        except ValueError:
            #If the value entered is not a numeric value, send an error message.
            messagebox.showerror("Error", "Invalid Input. Please enter a valid numeric value.")

    frame = tk.Frame(frame, bg="white")
    frame.pack(expand=True, fill="both", pady=10)
    #Creates a label inside the frame with a message indicating the type of calculation the user is about to do.
    label = tk.Label(frame, text=f"Calculate the {calc_type} of an object falling from a certain height:", bg="white", font=("Arial", 12))
    label.grid(row=0, column=0, columnspan=3, pady=10)
    #Creates a label that asks the user to enter a height in meters, as indicated by SI.
    label = tk.Label(frame, text="Enter a height in meters:", bg="white", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="e")
    entry = tk.Entry(frame, font=("Arial", 12), width=10)
    entry.grid(row=1, column=1, pady=5, sticky="w")
    #Creates a button that when clicked calls the "calculate" function, which starts the calculations.
    button = tk.Button(frame, text="Calculate", command=calculate, bg="lightblue", font=("Arial", 10)).grid(row=1, column=1, pady=5, padx=100, sticky="w")
    #Create an empty label where the result of the calculation will be displayed.
    result_label = tk.Label(frame, text="", bg="white", font=("Arial", 12))
    result_label.grid(row=2, column=0, columnspan=3, pady=10)
    #Set the frame columns to expand into the available space.
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

def create_calculators(frame, planet):
    create_calculator(frame, planet, "time")
    create_calculator(frame, planet, "velocity")

def fall_planet(frame, planet):
    canvas, img = setup_canvas(frame, planet)
    start_falling(canvas, img, "default", planet)
    create_calculators(frame, planet)
