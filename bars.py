import tkinter as tk
from tkinter import ttk
import time
import threading
import json
import random

with open("texts/composition_data.txt", "r") as file:
    composition_data = json.load(file)

def update_bars(progress_bars, labels, targets, steps):
    for i in range(steps):    #Controls how many times all progress bars will be updated.
        for bar, target, label in zip(progress_bars, targets, labels):
            current_value = bar["value"]    #Gets the current value of the bar.
            if current_value < target:
                # Calculate the new value as the minimun between the target and the current value incremented by 1.
                new_value = min(target, current_value + 1)
                bar["value"] = new_value    #Updates the progress bar to the new value.
                # Updates the associated label text with the new value, formatted to four decimal places.
                label.config(text=f"{new_value:.4f}%")
        time.sleep(0.05)

def create_bars(frame, body):
    frame.pack_forget()    #Clears the frame.
    progress_bars, labels = [], []    #Saves the progress bars and the labels that will display percentage values.

    # Access the "composition_data" dictionary with the key "body" to obtain the chemical composition of the celestial body.
    compositions = composition_data[body]
    compounds, percentages = list(compositions.keys()), list(compositions.values())

    styles = {}
    for compound in compounds:
        color = f"#{random.randint(0, 0xFFFFFF):06x}"   #For each compound, a random color is generated in RGB hexadecimal format.
        styles[compound] = color
    style = ttk.Style()
    style.theme_use("default")    #Change the current theme to the default theme.
    for compound, color in styles.items():
        #Define a custom style for each progress bar.
        style.configure(f"{compound}.Vertical.TProgressbar", troughcolor="white", background=color, thickness=40, bordercolor="white")

    def run_bars():
        #Reset the bars to 0.
        for bar in progress_bars:
            bar["value"] = 0
        threading.Thread(target=update_bars, args=(progress_bars, labels, percentages, 100)).start()

    #Creates a button that when clicked calls the "run_bars" function, which starts the progress of the bars.
    start_button = tk.Button(frame, text="Run", command=run_bars, bg="white")
    start_button.pack(pady=(10, 5), anchor="center")

    #Create a frame inside the main frame to hold the progress bars.
    bar_frame = tk.Frame(frame, bg="white")
    bar_frame.pack(pady=(5, 10), anchor="center")

    for i, compound in enumerate(compounds):
        #Creates a label initialized with the text "0%".
        label = tk.Label(bar_frame, text="0%", bg="white")
        label.grid(row=0, column=i, pady=5)
        labels.append(label)
        #Create progress bars starting at 0%
        bar = ttk.Progressbar(bar_frame, orient="vertical", length=400, mode="determinate", style=f"{compound}.Vertical.TProgressbar")
        bar.grid(row=1, column=i, padx=10)
        bar["value"] = 0
        progress_bars.append(bar)
        #Create a canvas to display compound texts tilted 45 degrees.
        text_frame = tk.Canvas(bar_frame, width=100, height=120, bg="white", bd=0, highlightthickness=0)
        text_frame.grid(row=2, column=i, pady=5)
        text_frame.create_text(70, 35, text=compound, angle=-45, font=("Arial", 10), anchor="n")

def setup_celestial(frame, body):
    create_bars(frame, body)
