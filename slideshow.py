import tkinter as tk
from PIL import Image, ImageTk

def load_image(photo, width, height, directory):
    image = Image.open(f"{directory}/{photo}" )
    image = image.resize((width, height), Image.LANCZOS)    #Resize the image to the dimensions of the frame.
    return image

def update_image(label, images, current_image_index):
    img = ImageTk.PhotoImage(images[current_image_index[0]])    #Converts image to Tkinter compatible format.
    label.config(image=img)    #Set the label to display the new image.
    label.image = img

def change_image(label, images, current_image_index, arrow):
    #Adjusts the index of the current image by adding or subtracting 1, depending on the direction of the arrow the user clicked.
    current_image_index[0] = (current_image_index[0] + arrow) % len(images)
    #The %len(images) operation causes that if it reaches the end of the list of images, it returns to the beginning, and vice versa
    update_image(label, images, current_image_index)

def create_slideshow(frame, body_name, num_images):
    directory = f"images/{body_name}_photos"
    images = []
    for i in range(1, num_images + 1):
        #At each iteration, the "load_image" function is called to load an image and resize it to 472x472 pixels.
        image = load_image(f"Image{i}.png", 472, 472, directory)
        images.append(image)
    current_image_index = [0]

    #Create a frame that will contain the slideshow.
    slide_frame = tk.Frame(frame, bg="white", borderwidth=4, highlightbackground="black", highlightthickness=1)
    slide_frame.pack(pady=(0, 20))
    #Create a label inside "slide_frame" to display the images.
    label = tk.Label(slide_frame, bg="white")
    label.pack(pady=(0, 5))
    #Create an additional frame inside slide_frame to hold the "previous" and "next" buttons.
    button_frame = tk.Frame(slide_frame, bg="white")
    button_frame.pack(side=tk.BOTTOM, pady=10)
    #Creates the "previous" button that, when clicked, calls the "change_image" function, which displays the image before the current one.
    prev_button = tk.Button(button_frame, text="◄", command=lambda: change_image(label, images, current_image_index, -1), bg="white", font=("Times", 25))
    prev_button.pack(side=tk.LEFT, padx=40)
    #Creates the "next" button that, when clicked, calls the "change_image" function, which displays the image after the current one.
    next_button = tk.Button(button_frame, text="►", command=lambda: change_image(label, images, current_image_index, 1), bg="white", font=("Times", 25))
    next_button.pack(side=tk.RIGHT, padx=40)

    update_image(label, images, current_image_index)
def celestial_slide(frame, body_name, num_images):
    create_slideshow(frame, body_name, num_images)
