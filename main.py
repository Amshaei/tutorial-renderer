import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image

def previous_image():
    global current_index
    if current_index > 0:
        current_index -= 1
    update_image_label()

def next_image():
    global current_index
    if current_index < len(images) - 1:
        current_index += 1
    update_image_label()

def open_file(image_label):
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, 'r') as file:
            content = file.read()
            mod_image = image.copy()
            lines = content.split('\n')
            line_height = 20
            x, y = 10, 20
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (255,255,255)
            thickness = 1
            for line in lines:
                cv.putText(mod_image, line, (x, y), font, font_scale, color, thickness, cv.LINE_AA)
                y += line_height
            update_image_label(image_label, mod_image)

def update_image_label(image_label, image):
    # convert to tkinter compatible format
    image_pil = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2GRAY))
    image_tk = ImageTk.PhotoImage(image_pil)
    image_label.configure(image=image_tk)
    image_label.image = image_tk

root = tk.Tk()

# get screen dimensions
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
root.geometry(f"{screen_w}x{screen_h}+0+0")

root.configure(bg="#121212")
root.title("File Preview")

# left grid
options_frame = tk.Frame(root)
options_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

# Create Group
group_frame = tk.Frame(options_frame)
group_frame.pack()

# Add to group
group_label = tk.Label(group_frame, text="Output Options")
group_label.pack()

# highlight options
lines = tk.Entry(group_frame)
lines.pack()

# button
open_button = tk.Button(group_frame, text="Open File", command=lambda: open_file(image_label))
open_button.pack(pady=10)

# right grid
image_frame = tk.Frame(root)
image_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

# image
width = 800
height = 600
blank_image = np.zeros((height, width, 3), dtype=np.uint8)

# output file
output_file = "assets/blank.jpg"
cv.imwrite(output_file, blank_image)

# get image
image = cv.imread(output_file)

# resize
resized_image = cv.resize(image, (width, height))

image_pil = Image.fromarray(cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY))
image_tk = ImageTk.PhotoImage(image_pil)

# put in image_frame
image_label = tk.Label(image_frame, image=image_tk)
image_label.pack()

button_frame = tk.Frame(image_frame)
button_frame.pack(pady=10)

previous_button = tk.Button(button_frame, text="< Previous", command=previous_image)
previous_button.grid(row=0, column=0, padx=5)

next_button = tk.Button(button_frame, text="Next >", command=next_image)
next_button.grid(row=0, column=2, padx=5)

index_label = tk.Label(button_frame, text="Image 0/0")
index_label.grid(row=0, column=1)

# Adjust column weights for grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()
