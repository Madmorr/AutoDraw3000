import tkinter as tk
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

# Create a label widget to display the selected image
imageLabel = tk.Label(window)
imageLabel.pack(pady=30)  # Add some padding around the label


# Function to open a file dialog for selecting an image
def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if file_path:
        display_image(file_path)


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


# Create a button widget to browse for an image
browse_button = tk.Button(window, text="Browse Image", command=browse_image)
browse_button.pack()

# Start the main event loop
window.mainloop()
