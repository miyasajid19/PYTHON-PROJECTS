from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os

# Function to change to the next image
def next_image(event=None):
    global counter, image_list
    counter = (counter + 1) % len(image_list)
    image_label.config(image=image_list[counter])
    info_label.config(text=f"Image {counter + 1} of {len(image_list)}")

# Function to change to the previous image
def prev_image(event=None):
    global counter, image_list
    counter = (counter - 1) % len(image_list)
    image_label.config(image=image_list[counter])
    info_label.config(text=f"Image {counter + 1} of {len(image_list)}")

# Function to open folder dialog and load images
def open_folder():
    global image_list, counter
    folder_path = filedialog.askdirectory()
    if folder_path:
        image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        # Dynamically resize images based on their original dimensions
        image_list = [Image.open(image) for image in image_paths]
        for i in range(len(image_list)):
            width, height = image_list[i].size
            if width > 1000 or height > 600:
                ratio = min(1000 / width, 600 / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image_list[i] = ImageTk.PhotoImage(image_list[i].resize((new_width, new_height)))
            else:
                image_list[i] = ImageTk.PhotoImage(image_list[i])
        counter = 0
        if image_list:
            image_label.config(image=image_list[counter])
            info_label.config(text=f"Image {counter + 1} of {len(image_list)}")

# Function to handle arrow key events
def on_arrow_key(event):
    if event.keysym == 'Right':
        next_image()
    elif event.keysym == 'Left':
        prev_image()

# Initialize Tkinter
root = Tk()
root.title("Image Viewer")

root.iconbitmap(r"gallery_icon_143014.ico")  # Update with your icon file path

# Set up components
image_label = Label(root)
info_label = Label(root, text="", font="Helvetica, 20")
button_open = Button(root, text="Open Folder", width=20, height=2, bg="blue", fg="white", command=open_folder)

# Display components
image_label.pack()
info_label.pack()
button_open.pack(pady=3)

# Bind arrow key events
root.bind('<Left>', on_arrow_key)
root.bind('<Right>', on_arrow_key)

# Run the main loop
root.mainloop()
