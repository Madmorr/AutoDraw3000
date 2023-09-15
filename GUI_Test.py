import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Basic GUI")
window.geometry("800x600")

# Allow window resizing both horizontally and vertically
window.resizable(True, True)

# Create a label widget
label = tk.Label(window, text="Hello World!")
label.pack(pady=20)  # Add some padding around the label


# Create a button widget
button = tk.Button(window, text="Click Me!")
button.pack()

# Function to be called when the button is clicked
def button_click():
    label.config(text="Button Clicked!")

# Bind the button's click event to the function
button.config(command=button_click)

# Start the main event loop
window.mainloop()
