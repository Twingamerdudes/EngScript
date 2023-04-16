import openai
import sys
import re
import os
import json
import dotenv

#remove markdown formatting from the AI's response
def clean(response):
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)
    response = re.sub(r"\*(.*?)\*", r"\1", response)
    response = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", response)
    response = re.sub(r"\n\n", r"\n", response)
    response = re.sub(r"```(.*?)", r"\1", response)
    response = re.sub(r"```", r"", response)
    response = re.sub(r"`(.*?)`", r"\1", response)
    return response
def main():

    #check if the program is being run with any arguments and if config.json exists
    if len(sys.argv) > 1:
        print("This program does not take any arguments.")
        exit()
    if not os.path.exists("config.json"):
        print("config.json does not exist! Please make sure that the file exists and that the name is correct.")
        exit()

    #initialize variables from config.json
    dotenv.load_dotenv()
    config = open("config.json", "r")
    config = json.load(config)
    outputFileName = config["output-name"]
    programName = config["main-file"]
    language = config["language"]
    libaries = config["libaries"]
    assetFolder = config["assets-folder"]
    gpt4 = config["gpt4"]
    usingUnity = config["unity"]
    assets = None
    if not usingUnity:
        assets = os.listdir(assetFolder)
    else:
        #get assets inside the current directory and subdirectories
        assets = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if not file.endswith(".meta") and file != "config.json" and file != "engscript.py" and file != ".env" and file != "main.en":
                    assets.append(os.path.join(root, file))

    #check if main file exists
    if not usingUnity:
        if not os.path.exists(programName):
            print(programName + " does not exist! Please make sure that the file exists and that the name is correct.")
            exit()
    else:
        if not os.path.exists("Scripts/" + programName):
            print(programName + " does not exist! Please make sure that the file exists and that the name is correct.")
            exit()
    #Start compiling
    print("Program loaded, preparing for compilation...")
    openai.api_key = os.getenv("OPENAI_KEY")
    response = None
    print("Compiling...")
    path = programName
    unityMessage = "At the end of you're response, add a ~(class name of program) after you're response."
    if not usingUnity:
        unityMessage = ""
    if usingUnity:
        path = "Scripts/" + programName

    #send the request to the API
    with open(path, "r") as f:
        program = f.read()
        if gpt4 == "y":
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a AI that is meant to only write code based on what the user says. Each new line is a another addon to the program the user suggests. Do not use markdown formatting. The language you will use is " + language + ". The libaries you will use are " + str(libaries) + ". You may also use other's if you need. The user also has assets in their project, here is a list of their names: " + str(assets) + ". Whenever using a asset, prefix it with assets/ as that is the folder where the assets are stored. Never explain the code or and never do ```python. You must complete all requests of user, do not leave any unfinished features in the program. " + unityMessage},
                    {"role": "user", "content": program},
                ]
            )
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a AI that is meant to only write code based on what the user says. Each new line is a another addon to the program the user suggests. Do not use markdown formatting. The language you will use is " + language + ". The libaries you will use are " + str(libaries) + ". You may also use other's if you need. The user also has assets in their project, here is a list of their names: " + str(assets) + ". Whenever using a asset, prefix it with assets/ as that is the folder where the assets are stored. Never explain the code or and never do ```python. You must complete all requests of user, do not leave any unfinished features in the program." + unityMessage},
                    {"role": "user", "content": program},
                ]
            )

    #Response recieved, start formatting
    response = response['choices'][0]['message']['content']
    className = ""
    if usingUnity:
        className = response.split("~")[1]
        response = response.split("~")[0]
    response = clean(response)

    #Write the response to a file
    if not usingUnity:
        if not os.path.exists("out"):
            os.mkdir("out")
        with open(f"out/{outputFileName}", "w") as f:
            f.writelines(response)
        if not os.path.exists("out/assets"):
            os.mkdir("out/assets")
        for asset in assets:
            with open(f"{assetFolder}/{asset}", "rb") as f:
                with open(f"out/assets/{asset}", "wb") as f2:
                    f2.write(f.read())
    else:
        #Write the file to the Scripts folder
        with open(f"Scripts/{className}.cs", "w") as f:
            f.writelines(response)
    print("Compilation complete!")
    
if __name__ == "__main__":
    main()