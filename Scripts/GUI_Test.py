import tkinter as tk
import os
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics import renderPDF  
from pdf2image import convert_from_bytes  


# Create the main window
window = tk.Tk()
window.title("AutoDrawGUI Beta 1.0")
window.geometry("800x600")

# Allow window resizing both horizontally and vertically
window.resizable(True, True)


# Define the path to the juicy-gcode executable
path = os.getcwd()
gCodeLit = path + r"\JuicyG-Code\juicy-gcode-1.0.0.0-Windows\juicy-gcode.exe"

# global var to hold path of chosen file
selected_file = ""

def runJuicyGCode(filename):
    gCodeArgs2 = "-o" 
    gCodeOutputFile = "output.gcode"
    gCodeResult = subprocess.run([gCodeLit, filename, gCodeArgs2, gCodeOutputFile], capture_output=True, text=True)
    
    if gCodeResult.returncode != 0:
        print(gCodeResult.stderr)
        return None
    with open(gCodeOutputFile, 'r') as f:
        gcode_content = f.read()
    return gcode_content

# Function to open a file dialog for selecting an image
def browse_image():
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if file_path:
        selected_file = file_path  
        display_image(file_path)
        generate_button.config(state=tk.NORMAL)  # Enable the "Generate G-Code" button


# Function to be called when the button is clicked
def display_image(file_path):
    if file_path.lower().endswith('.svg'):
        # Convert SVG to PDF using svglib and reportlab
        drawing = svg2rlg(file_path)

        # Set canvas size to the size of the SVG drawing
        width, height = drawing.minWidth(), drawing.height
        pdf_bytes = BytesIO()
        c = Canvas(pdf_bytes, pagesize=(width, height))

        # Draw the SVG centered on the canvas
        renderPDF.draw(drawing, c, (width - drawing.minWidth()) / 2, (height - drawing.height) / 2)
        c.save()

        # Convert PDF to PNG using pdf2image
        pages = convert_from_bytes(pdf_bytes.getvalue())
        image = pages[0] if pages else None

    else:
        image = Image.open(file_path)

    image = image.resize((400, 400))  # Resize the image to fit the label
    photo = ImageTk.PhotoImage(image=image)  # Convert the image to a format that tkinter can display
    imageLabel.config(image=photo)
    imageLabel.image = photo  # Keep a reference to the photo to prevent garbage collection

def generate_gcode():
    global selected_file
    if ".svg" in selected_file:
        gcode = runJuicyGCode(selected_file)
        if gcode:
            gcodeDisplay.delete(1.0, tk.END)  # Clear the text widget
            gcodeDisplay.insert(tk.END, gcode)  # Insert the G-code into the text widget
        else:
            gcodeDisplay.delete(1.0, tk.END)
            gcodeDisplay.insert(tk.END, "Error generating G-Code.")
    else:
        gcodeDisplay.delete(1.0, tk.END)
        gcodeDisplay.insert(tk.END, "Please select an SVG file first.")


# Create a button widget to browse for an image
browse_button = tk.Button(window, text="Browse Image", command=browse_image)
browse_button.pack()

# Create a label widget to display the selected image
imageLabel = tk.Label(window)
imageLabel.pack(pady=30)  # Add some padding around the label

# Create a button widget to generate G-Code
generate_button = tk.Button(window, text="Generate G-Code", command=generate_gcode, state=tk.DISABLED)
generate_button.pack(pady=10)

# Create a Text widget to display the G-code
gcodeDisplay = tk.Text(window, width=50, height=20)
gcodeDisplay.pack(pady=10, padx=10)


# Start the main event loop
window.mainloop()
