import subprocess

#Automatically runs both potrace and juicy gcode when provided with a filename

def runPotrace(filename):
    #can replace this with a load from external file so that parameters can
    #be tweaked without messing with the program
    potraceArgs = "-s"
    #potraceArgs3 = "-s" + filename + bmpExtension
    #cwd may not be necessary
    potraceResult = subprocess.run([potraceLit, potraceArgs, filename], cwd = r"/home/w003gsl/seniordesign/code/AutoDraw3000", capture_output=True)
    if potraceResult.returncode != 0:
        print(potraceResult.stderr)
    return potraceResult.returncode

def runJuicyGCode(filename):
    #can replace this with a load from external file so that parameters can
    #be tweaked without messing with the program
    gCodeArgs2 = "-o" 
    gCodeOutputFile = "output.gcode"
    #cwd may not be necessary
    gCodeResult = subprocess.run([gCodeLit, filename, gCodeArgs2, gCodeOutputFile], cwd = r"/home/w003gsl/seniordesign/code/AutoDraw3000", capture_output=True)
    if gCodeResult.returncode != 0:
        print(gCodeResult.stderr)
        return gCodeResult.returncode * 10
    return 0


#main
bmpExtension = ".bmp"
#svgExtension = ".svg"
gcodeExtnsion = ".gcode"
potraceLit = "potrace"
gCodeLit = r"/home/w003gsl/seniordesign/juicy-gcode-1.0.0.0/juicy-gcode"
finalReturnCode = 0


#sanitization of filename goes here
#config path to potrace and juicy, use os.resolve()?
filename = input("Please enter a file name: ")
if ".bmp" in filename:
    print("Currently no support for potrace.")
    #finalReturnCode += runPotrace(filename)
    #finalReturnCode += runJuicyGCode(filename)
    #I think I could pipe the output directly to potrace if I felt like not saving an intermediate file
elif ".svg" in filename:
    finalReturnCode += runJuicyGCode(filename)
else:
    print("There is currently no support for that filename.\nPlease only use this program with .bmp or .svg files.")

#finalReturnCode += runPotrace(filename)
if finalReturnCode != 0:
    print("Could not convert files. Error code " + finalReturnCode.__str__())
else:
    print("Successful yay!")
