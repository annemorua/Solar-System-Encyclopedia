import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from slideshow import celestial_slide
from bars import setup_celestial

def main():
    main_window = tk.Tk()
    ency = SolarSystem(main_window)    #Creates an instance of the "SolarSystem" class which is the main class that manages the interface and functionality.
    screen_width = main_window.winfo_screenwidth()    #Gets the system screen dimensions with "winfo_screenwidth()" and "winfo_screenheight()".
    screen_height = main_window.winfo_screenheight()
    main_window.mainloop()    #Launches the main loop that keeps the window open and functional.
    return screen_width, screen_height

####Below are the 3 required functions used to perform the tests using pytest.
def check_celestial(ency):
    entered_text = ency.celestial_entry.get().strip().lower()    #Gets the text entered by the user, converts it to lowercase and removes extra spaces.
    #Associate the names of the bodies with numerical indices.
    celestials = {"mercury": 0, "venus": 1, "earth": 2, "mars": 3, "jupiter": 4, "saturn": 5, "uranus": 6, "neptune": 7, "sun": 8}
    if entered_text == "moon":    #If the entered text is "moon", it displays an informative message indicating that the Moon is not available.
        tk.messagebox.showinfo("Info", "The moon is not available yet.")
    elif entered_text in celestials:
        index = celestials.get(entered_text)    #If the text matches a body, the corresponding index is obtained and the "manage_frames" function is called.
        ency.manage_frames(ency.window.winfo_screenwidth(), ency.window.winfo_screenheight(), show_frame=ency.celestial_frame[index])
    else:    #If the entered text is not a valid name of a body, an error message is displayed.
        tk.messagebox.showerror("Error", "The entered celestial body is not valid. Please enter a valid celestial body.")

def calculate_time(height, acceleration):    #This function calculates the time of an object in free fall from a height.
    return np.sqrt(2 * height / acceleration)

def calculate_velocity(height, acceleration):    #This function calculates the final velocity of an object in free fall from a height.
    return np.sqrt(2 * acceleration * height)

class SolarSystem:
    def __init__(self, window):
        self.window = window
        self.window.overrideredirect(True)    #Hides standard window borders and controls.
        screen_width = self.window.winfo_screenwidth()    #Adjust the graphical interface to any resolution.
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")    #Sets the size of the main window to fill the entire screen.

        #Call the "load_texts" method to read and process data related to the physical and orbital characteristics of the bodies.
        self.data_physical, self.data_orbital = self.load_texts()
        self.setup_homepage(screen_width, screen_height)  # Call the "setup_homepage" method to create the initial interface elements for the main window.
        self.manage_frames(screen_width, screen_height)    #Call the "manage_frames" method to create the frames containing the bodies.
    def setup_frames(self, screen_width, screen_height):
        physical_data = self.data_physical    #The data_physical and data_orbital lists are extracted from the class attributes.
        orbital_data = self.data_orbital
        #Paths of the header images of the bodies and the sun.
        headers = ["images/headers/mercury_header.png", "images/headers/venus_header.png", "images/headers/earth_header.png", "images/headers/mars_header.png", "images/headers/jupiter_header.png", "images/headers/saturn_header.png", "images/headers/uranus_header.png", "images/headers/neptune_header.png", "images/headers/sun_header.png"]
        self.images = []
        for title in headers:    #Open and resize the images to a fixed size of 534x300 pixels.
            img = Image.open(title).resize((534, 300), Image.LANCZOS)
            self.images.append(img)
        self.r_images = []
        for image in self.images:    #Resized images are converted to PhotoImage objects, which tkinter can display.
            r_image = ImageTk.PhotoImage(image)
            self.r_images.append(r_image)
        self.labels = []
        for scro, image in zip(self.celestial_scroller, self.r_images):    #Labels are created for each image and assigned to the scrollable containers.
            label = tk.Label(scro, image=image, bg="white")
            self.labels.append(label)
        for label in self.labels:
            label.pack(anchor="nw", padx=screen_width // 2 - 267)    #Adjust the horizontal margin to center the images in the window.

        #Calls the specific methods of the bodies.
        self.slideshow(screen_width, screen_height)
        self.information("Physical Data", physical_data)
        self.information("Orbital Data", orbital_data)
        self.gravity(screen_width, screen_height)
        self.atmospheric_composition(screen_width, screen_height)

    def manage_frames(self, screen_width, screen_height, show_frame=None):
        #The class instance is checked to see if it already has the "celestial_frame" attribute. If it does not exist, the frames have not yet been created and they are created.
        if not hasattr(self, "celestial_frame"):
            self.celestial_frame = []    #Three empty lists are created to store the frames, canvases and scrollers.
            self.celestial_canvas = []
            self.celestial_scroller = []

            for i in range(9):    #Creating frames, canvas and scrollers.
                frame = tk.Frame(self.window)
                canvas = tk.Canvas(frame)
                scroller = tk.Frame(canvas, bg="white")
                self.celestial_frame.append(frame)
                self.celestial_canvas.append(canvas)
                self.celestial_scroller.append(scroller)
                #When the scroller is resized, "<Configure>" updates the scrollable region of the canvas based on the size of the content.
                scroller.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scroller, anchor="nw")    #The scroller is placed inside the canvas.
                canvas.pack(fill="both", expand=True)    #"fill=both" takes up all the available space, and "expand=True" expands to the size of the frame.

                exit_button = tk.Button(canvas, text="Exit", command=self.close_window)    #An "Exit" button is created on each canvas that closes the program.
                exit_button.place(x=screen_width - 35, y=screen_height - 35)
                #A "Back" button is created on each canvas to return to the main screen.
                back_button = tk.Button(canvas, text=" 🡰 ", command=lambda: self.manage_frames(screen_width, screen_height, self.homepage_frame))
                back_button.place(x=5, y=5)

            self.setup_frames(screen_width, screen_height)

        if show_frame:    #If a frame to display is given, all frames are first hidden with "pack_forget()".
            frames = [self.homepage_frame, *self.celestial_frame]
            for f in frames:
                f.pack_forget()
            show_frame.pack(fill="both", expand=True)    #Then the indicated frame is displayed.
            if show_frame in self.celestial_frame:    #If the "show_frame" corresponds to one of the body frames, its index is obtained and the corresponding canvas is accessed.
                index = self.celestial_frame.index(show_frame)
                canvas = self.celestial_canvas[index]
            else:
                canvas = None

            if canvas:
                canvas.bind_all("<MouseWheel>", lambda event: self.mouse_roller(event, canvas))    #The mouse wheel event is linked to allow scrolling within the canvas.
                canvas.configure(scrollregion=canvas.bbox("all"))    #Gets the bounds of the content within the canvas.

    def setup_homepage(self, screen_width, screen_height):
        self.homepage_frame = tk.Canvas(self.window, width=screen_width, height=screen_height)    #A canvas is created that serves as the basis for the home screen.
        self.homepage_frame.pack(fill="both", expand=True)
        #An entry is created where the user type the name of a celestial body. The validity of the entered text is then verified.
        self.celestial_entry = tk.Entry(self.homepage_frame, font=("Arial", 16), width=11)
        self.celestial_entry.place(x=screen_width / 2 - 60, y=screen_height / 2)
        #Creates a button that, when clicked, calls the "check_celestial" function, which verifies the entered text.
        self.check_button = tk.Button(self.window, text=" 🡲 ", command=lambda: check_celestial(self))
        self.check_button.place(x=screen_width / 2 + 80, y=screen_height / 2)

        image = Image.open("images/headers/homepage_image.png")    #Home screen background image.
        #Resizes the image to fit the width of the screen, keeping the original aspect ratio.
        r_image = image.resize((screen_width, round((screen_width * 1638) / 2560)), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(r_image)    #Converts image to Tkinter compatible object.
        self.homepage_frame.create_image(0, 0, anchor="nw", image=self.bg_image)    #Draw the background image on the home screen.

        #Create a button that, when clicked, displays a message box with instructions.
        self.help_button = tk.Button(self.window, text="   ?   ", bg="lightblue", command=lambda: tk.messagebox.showinfo(
                "Help",
                "Instructions:\n\n"
                "1. Enter the name of a celestial body in the input field. Valid options: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Sun.\n"
                """2. Click the "🡲" button to confirm your choice.\n"""
                """4. The "Exit" button will close the application."""))
        self.help_button.place(x=5, y=5)
        #Creates a button that, when clicked, calls the "close_window" function, which closes the program.
        self.exit_button = tk.Button(self.window, text="Exit", command=self.close_window)
        self.exit_button.place(x=screen_width - 35, y=screen_height - 35)

    def load_texts(self):
        #The file "characteristics.txt" is opened in read mode with the option "encoding=utf-8" to handle special characters and mathematical symbols.
        with open("texts/characteristics.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        data = {}    #Saves the categories and their respective information.
        title = None    #Saves the name of the data category (physical_body_name, orbital_body_name).
        texts_list = []    #Saves the lines related to that category.

        def sentences():
            if title and texts_list:
                # If the title starts with "physical" or "orbital", then the lines of "texts_list" are joined with newlines and saved in data.
                if title.startswith(("physical", "orbital")):
                    data[title] = "\n".join(texts_list)
                else:    #If title does not start with "physical" or "orbital", save "texts_list" directly to data.
                    data[title] = texts_list

        for line in lines:
            line = line.strip()
            if line.endswith(":"):    #If the line ends with ":", call "sentences()" to save the previous category.
                sentences()
                title = line[:-1]    #Update title with the current line, removing the ":".
                texts_list = []    #Reset "texts_list" to start accumulating new lines for this category.
            elif line:
                texts_list.append(line.replace("\\n", "\n"))    #If the line is not empty, replace "\n" with a real newline and add the line to "texts_list".
        sentences()
        #Create a dictionary with the title and its respective physical information, as well as the dimensions for the interface.
        physical_data = []
        for body in ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]:
            physical_data.append({ "title": "\n".join(data["phy_title"]), "information": data[f"physical_{body}"], "left_width": 14, "left_height": 16, "right_width": 20, "right_height": 16})
        physical_data.append({"title": "\n".join(data["phy_sun_title"]), "information": data["physical_sun"], "left_width": 14, "left_height": 21, "right_width": 22, "right_height": 21})
        #Create a dictionary with the title and its respective orbital information, as well as the dimensions for the interface.
        orbital_data = []
        for body in ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]:
            orbital_data.append({"title": "\n".join(data["orb_title"]), "information": data[f"orbital_{body}"], "left_width": 14, "left_height": 5, "right_width": 20, "right_height": 5})
        orbital_data.append({"title": "\n".join(data["orb_sun_title"]), "information": data["orbital_sun"], "left_width": 18, "left_height": 8, "right_width": 22, "right_height": 8})

        return physical_data, orbital_data

    def information(self, title, data):
        for i, (scro, setting) in enumerate(zip(self.celestial_scroller, data)):
            tk.Label(scro, text=title, fg="black", bg="white", font=("Times", 30)).pack(pady=(50, 0))    #Create a label with the category title.
            #Creates a frame that will serve as a container for the text boxes.
            frame = tk.Frame(scro, bg="white")
            frame.pack(pady=10, anchor="center")
            #Creates a text box that has a width and height defined by the values in the "setting" dictionary.
            left_text = tk.Text(frame, width=setting["left_width"], height=setting["left_height"], borderwidth=0, highlightthickness=0, font=("Times", 14))
            left_text.insert("1.0", setting["title"])    #Inserts the title text.
            left_text.config(state=tk.DISABLED)    #Sets the text box so that the user cannot edit the content.
            left_text.grid(row=0, column=0, padx=10)    #Place the text box in the first column.
            #Creates a text box that has a width and height defined by the values in the "setting" dictionary.
            right_text = tk.Text(frame, width=setting["right_width"], height=setting["right_height"], borderwidth=0, highlightthickness=0, font=("Times", 14))
            right_text.insert("1.0", setting["information"])    #Inserts the text of the information.
            right_text.config(state=tk.DISABLED)    #Sets the text box so that the user cannot edit the content.
            right_text.grid(row=0, column=1, padx=10)    #Place the text box in the second column.

    def setup_functions(self, title, action, action_args):    #Receives the title displayed in the interface, the function to be executed, and the list of arguments.
        for scro in self.celestial_scroller:
            #Creates the title of the different functions displayed in the interface.
            tk.Label(scro, text=title, fg="black", bg="white", font=("Times", 30)).pack(pady=(50, 0))

        for scro, args in zip(self.celestial_scroller, action_args):    #Each function is passed the scrollable container and the unpacked arguments.
            action(scro, *args)

    def slideshow(self, screen_width, screen_height):
        #Contains the names of the bodies and the number of images associated with each body.
        celestials = {"mercury": 8, "venus": 6, "earth": 8, "mars": 7, "jupiter": 8, "saturn": 7, "uranus": 6, "neptune": 6, "sun": 7}
        action_args = []
        for body, num_images in celestials.items():    #For each body add a tuple of the name and the number of images.
            action_args.append((body, num_images))
        self.setup_functions("Photo collection", celestial_slide, action_args)

    def gravity(self, screen_width, screen_height):
        from gravity import fall_planet    #The function is imported here due to a circular import.
        celestials = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "sun"]
        action_args = []
        for body in celestials:
            #For each body, add a tuple with a single element (the name) to send the contents as a single argument.
            action_args.append((body,))
        self.setup_functions("Gravitational force", fall_planet, action_args)

    def atmospheric_composition(self, screen_width, screen_height):
        celestials = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "sun"]
        action_args = []
        for body in celestials:
            #For each body, add a tuple with a single element (the name) to send the contents as a single argument.
            action_args.append((body,))
        self.setup_functions("Atmospheric composition", setup_celestial, action_args)

    def mouse_roller(self, event, canvas):
        if event.delta > 0:    #The mouse event triggers the function.
            canvas.yview_scroll(-1, "units")    #If the mouse wheel scroll is positive, scroll the canvas up
        else:
            canvas.yview_scroll(1, "units")    #If negative, scroll the canvas down.

    def close_window(self):
        self.window.quit()    #Calls the "quit()" method, stopping the main loop and closing the graphical interface..

if __name__ == "__main__":
    main()
