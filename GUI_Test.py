import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Create the main window
window = tk.Tk()
window.title("AutoDrawGUI Beta 1.0")
window.geometry("800x600")

# Allow window resizing both horizontally and vertically
window.resizable(True, True)

# Create a label widget to display the selected image
imageLabel = tk.Label(window)
imageLabel.pack(pady=30)  # Add some padding around the label


# Function to open a file dialog for selecting an image
def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if file_path:
        display_image(file_path)


# Function to be called when the button is clicked
def display_image(file_path):
    image = Image.open(file_path)
    image = image.resize((400, 400))  # Resize the image to fit the label
    photo = ImageTk.PhotoImage(image=image) # Convert the image to a format that tkinter can display
    imageLabel.config(image=photo) 
    imageLabel.image = photo  # Keep a reference to the photo//prevents garbage collection 

# Create a button widget to browse for an image
browse_button = tk.Button(window, text="Browse Image", command=browse_image)
browse_button.pack()

# Start the main event loop
window.mainloop()
