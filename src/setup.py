import json
import os

#check if engscript.py exists and .env exists
if not os.path.exists("engscript.py"):
    print("engscript.py does not exist! Please make sure that the file is in the current directory and that the name is correct.")
    exit()
if not os.path.exists(".env"):
    print(".env does not exist! Please make sure that the file is in the current directory and that the name is correct.")
    exit()

#Basic setup
print("English Project Setup Tool")
print("Project Name: ", end="")
projectName = input()
print("Import into Unity(y/n): ", end="")
unity = input()
if unity == "n":
    #Start non-unity setup
    print("Starting normal setup...")
    print("Project Path (leave blank for root directory): ", end="")
    projectPath = input()
    projectPath = projectPath.replace("\\", "/")
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
    print("Do you want (and have access) to GPT-4 to generate code? (y/n): ", end="")
    gpt4 = input()
    if gpt4 == "y":
        print("GPT-4 has been enabled!")
    else:
        print("GPT-3.5-turbo has been enabled!")
    print("Creating config file...")

    #Create config json
    config = {
        "project-name": projectName,
        "language": language,
        "libaries": libaries,
        "main-file": mainFile,
        "output-name": outputFile,
        "assets-folder": assetsFolder,
        "gpt4": gpt4,
        "unity": False
    }

    #Start acutally setting up the project
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
else:
    #Start Unity setup
    print("Starting Unity setup...")
    print("Unity Project Directory (leave blank for root path): ", end="")
    projectPath = input()
    projectPath = projectPath.replace("\\", "/")
    projectPath = f"{os.getcwd()}/{projectPath}"
    print("What is the name of your main file (ex. main.en): ", end="")
    mainFile = input()
    print("Do you want (and have access) to GPT-4 to generate code? (y/n): ", end="")
    gpt4 = input()
    if gpt4 == "y":
        print("GPT-4 has been enabled!")
    else:
        print("GPT-3.5-turbo has been enabled!")
    print("Creating config file...")

    #Create config json
    config = {
        "project-name": projectName,
        "language": "C#",
        "libaries": "UnityEngine",
        "main-file": mainFile,
        "output-name": "Main.cs",
        "assets-folder": "Assets",
        "gpt4": gpt4,
        "unity": True
    }

    #Start acutally setting up the project
    with open(f"{projectPath}/Assets/config.json", "w") as f:
        f.write(json.dumps(config))
    print("Config file created!")
    print("Copying engscript.py...")
    with open("engscript.py", "r") as f:
        with open(f"{projectPath}/Assets/engscript.py", "w") as f2:
            f2.write(f.read())
    print("engscript.py copied!")
    print("Copying .env...")
    with open(".env", "r") as f:
        with open(f"{projectPath}/Assets/.env", "w") as f2:
            f2.write(f.read())
    print(".env copied!")
    print("Checking if Scripts Folder exists...")

    #Unity specific setup
    if not os.path.exists(f"{projectPath}/Assets/Scripts"):
        print("Scripts folder does not exist! Creating...")
        os.mkdir(f"{projectPath}/Assets/Scripts")
        print("Scripts folder created!")
    if not os.path.exists(f"{projectPath}/Assets/Resources"):
        print("Resources folder does not exist! Creating...")
        os.mkdir(f"{projectPath}/Assets/Resources")
        print("Resources folder created!")
        
    print("Creating main file...")
    with open(f"{projectPath}/Assets/Scripts/{mainFile}", "w") as f:
        f.write("Display hello world to the console.")
    print("Main file created!")
    print("Done!")