# Updating the code to include two frames with the specified elements in each frame

import tkinter as tk
import os
import subprocess
import platform
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics import renderPDF  
from pdf2image import convert_from_bytes  
import paho.mqtt.publish as publish

#use geometry manager grid 


BROKER_IP = '10.16.62.201'

def send_command(command):
    publish.single("robot/control", command, hostname=BROKER_IP)
  
window = tk.Tk()
window.title("AutoDrawGUI Beta 1.0")
window.geometry("400x600")
window.resizable(True, True)

# Function to update the scrollregion
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

# Create a canvas and a scrollbar
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the scrollbar and canvas
scrollbar.pack(side=tk.RIGHT, fill='y')
canvas.pack(side=tk.LEFT, fill='both', expand=True)

# Create a frame inside the canvas
container_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=container_frame, anchor='nw')

# Bind the configure event
container_frame.bind('<Configure>', on_configure)

# Replacing main_frame with container_frame for your widgets
main_frame = container_frame  # Use container_frame instead of main_frame for your contents
manual_controls_frame = tk.Frame(window)  # This remains as it is

# Function to raise a frame to the top
def raise_frame(frame):
    frame.tkraise()



for frame in (main_frame, manual_controls_frame):
    frame.grid(row=0, column=0, sticky='news')

# Main Frame content

# Get the current working directory
path = os.getcwd()

# Determine the operating system
os_name = platform.system()

# Define the path to the juicy-gcode executable based on the operating system
if os_name == "Darwin":  # macOS
    gCodeLit = os.path.join(path, "JuicyG-Code", "juicy-gcode-1.0.0.0-Mac", "juicy-gcode-1.0.0.0", "juicy-gcode")
elif os_name == "Linux":
    gCodeLit = os.path.join(path, "JuicyG-Code", "juicy-gcode-1.0.0.0-Linux", "juicy-gcode-1.0.0.0", "juicy-gcode")
elif os_name == "Windows":
    gCodeLit = os.path.join(path, "JuicyG-Code", "juicy-gcode-1.0.0.0-Windows", "juicy-gcode.exe")
else:
    raise Exception(f"Unsupported operating system: {os_name}")

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
    file_path = filedialog.askopenfilename(filetypes=[("All Images", "*.png *.jpg *.jpeg *.bmp *.svg"), ("SVG files", "*.svg"), ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp")])
    if file_path:
        selected_file = file_path  
        display_image(file_path)
        # Check if SVG or another format
        if selected_file.lower().endswith('.svg'):
            convert_button.config(state=tk.DISABLED)
            generate_button.config(state=tk.NORMAL)
        else:
            convert_button.config(state=tk.NORMAL)
            generate_button.config(state=tk.DISABLED)


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
        
def convert_image_to_svg():
    global selected_file

    # Step 1: Convert the image to BMP format.
    bmp_file = selected_file + ".bmp"
    Image.open(selected_file).convert("L").save(bmp_file)  # Convert image to grayscale and save as BMP

    # Step 2: Convert BMP to SVG using potrace.
    svg_file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
    if not svg_file_path:  # If user cancels the save dialog
        os.remove(bmp_file)  # remove temporary BMP file
        return
    subprocess.run(["potrace", bmp_file, "-s", "-o", svg_file_path])

    # Step 3: Clean up the temporary BMP file.
    os.remove(bmp_file)

    # Step 4: Update GUI.
    selected_file = svg_file_path  # update the selected file to the new SVG
    display_image(svg_file_path)  # display the new SVG
    convert_button.config(state=tk.DISABLED)
    generate_button.config(state=tk.NORMAL)


browse_button = tk.Button(main_frame, text="Browse Image", command=browse_image)
browse_button.pack()

imageLabel = tk.Label(main_frame)
imageLabel.pack(pady=30)

convert_button = tk.Button(main_frame, text="Convert to SVG", command=convert_image_to_svg, state=tk.DISABLED)
convert_button.pack(pady=10)

generate_button = tk.Button(main_frame, text="Generate G-Code", command=generate_gcode, state=tk.DISABLED)
generate_button.pack(pady=10)

gcodeDisplay = tk.Text(main_frame, width=50, height=20)
gcodeDisplay.pack(pady=10, padx=10)

# Manual Controls Frame content
tk.Button(manual_controls_frame, text="Forward", command=lambda: send_command("forward")).pack()
tk.Button(manual_controls_frame, text="Backward", command=lambda: send_command("backward")).pack()
tk.Button(manual_controls_frame, text="Left", command=lambda: send_command("left")).pack()
tk.Button(manual_controls_frame, text="Right", command=lambda: send_command("right")).pack()
tk.Button(manual_controls_frame, text="Back to Main", command=lambda: raise_frame(main_frame)).pack()

# Add the Manual Controls button to the main frame
manual_controls_button = tk.Button(main_frame, text="Manual Controls", command=lambda: raise_frame(manual_controls_frame))
manual_controls_button.pack()

# Initially, raise the main frame
raise_frame(main_frame)

window.mainloop()

