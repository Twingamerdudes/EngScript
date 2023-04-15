import json
import os
if not os.path.exists("engscript.py"):
    print("engscript.py does not exist! Please make sure that the file is in the current directory and that the name is correct.")
    exit()
print("English Project Setup Tool")
print("Project Name: ", end="")
projectName = input()
print("Project Path (leave blank for root directory): ", end="")
projectPath = input()
projectPath = projectPath.replace("\\", "/")
#add the root directory to the beginning of the path
projectPath = f"{os.getcwd()}/{projectPath}"
print("What language will you be compiling to? (python, javascript, etc): ", end="")
language = input()
print("What libaries will you plan to use? (seperate with commas): ", end="")
libaries = input()
libaries = libaries.split(",")
print("What is the name of your main file (ex. main.en): ", end="")
mainFile = input()
print("What is the name of your output file (ex. main.py): ", end="")
outputFile = input()
print("What is the name of your assets folder (ex. assets): ", end="")
assetsFolder = input()
print("Creating config file...")
config = {
    "project-name": projectName,
    "language": language,
    "libaries": libaries,
    "main-file": mainFile,
    "output-name": outputFile,
    "assets-folder": assetsFolder
}
os.mkdir(f"{projectPath}/{projectName}")
os.mkdir(f"{projectPath}/{projectName}/assets")
with open(f"{projectPath}/{projectName}/config.json", "w") as f:
    f.write(json.dumps(config))
print("Config file created!")
print("Copying engscript.py...")
with open("engscript.py", "r") as f:
    with open(f"{projectPath}/{projectName}/engscript.py", "w") as f2:
        f2.write(f.read())
print("engscript.py copied!")
print("Copying .env...")
with open(".env", "r") as f:
    with open(f"{projectPath}/{projectName}/.env", "w") as f2:
        f2.write(f.read())
print(".env copied!")
print("Creating main file...")
with open(f"{projectPath}/{projectName}/{mainFile}", "w") as f:
    f.write("Display hello world to the console.")
print("Main file created!")
print("Done!")