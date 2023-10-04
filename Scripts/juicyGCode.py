import subprocess
import os

#Automatically runs juicy gcode when provided with a filename


def runJuicyGCode(filename):
    #can replace this with a load from external file so that parameters can
    #be tweaked without messing with the program
    
    gCodeArgs2 = "-o" 
    gCodeOutputFile = "output.gcode"
    
    # Run the juicy-gcode tool with the specified arguments
    gCodeResult = subprocess.run([gCodeLit, filename, gCodeArgs2, gCodeOutputFile], capture_output=True)
    
    # Check if the juicy-gcode tool encountered any errors
    if gCodeResult.returncode != 0:
        print(gCodeResult.stderr)
        return gCodeResult.returncode * 10
    return 0


#main
# Get the current working directory
path = os.getcwd()

# Define the path to the juicy-gcode executable using the current directory
gCodeLit = path + r"\JuicyG-Code\juicy-gcode-1.0.0.0-Windows\juicy-gcode.exe"

finalReturnCode = 0


#sanitization of filename goes here
#config path to potrace and juicy, use os.resolve()?
filename = input("Please enter a file name: ")
if ".svg" in filename:
    finalReturnCode += runJuicyGCode(filename)
else:
    print("There is currently no support for that filename.\nPlease only use this program with.svg files.")


if finalReturnCode != 0:
    print("Could not convert files. Error code " + finalReturnCode.__str__())
else:
    print("Successful yay!")
