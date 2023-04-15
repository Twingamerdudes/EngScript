import openai
import sys
import re
import os
import json
import dotenv
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
    if len(sys.argv) > 1:
        print("This program does not take any arguments.")
        exit()
    if not os.path.exists("config.json"):
        print("config.json does not exist! Please make sure that the file exists and that the name is correct.")
        exit()
    dotenv.load_dotenv()
    config = open("config.json", "r")
    config = json.load(config)
    outputFileName = config["output-name"]
    programName = config["main-file"]
    language = config["language"]
    libaries = config["libaries"]
    assetFolder = config["assets-folder"]
    assets = os.listdir(assetFolder)
    #check if the file exists
    if not os.path.exists(programName):
        print(programName + " does not exist! Please make sure that the file exists and that the name is correct.")
        exit()
    print("Program loaded, preparing for compilation...")
    openai.api_key = os.getenv("OPENAI_KEY")
    response = None
    print("Compiling...")
    with open(programName, "r") as f:
        program = f.read()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a AI that is meant to only write code based on what the user says. Each new line is a another addon to the program the user suggests. Do not use markdown formatting. The language you will use is " + language + ". The libaries you will use are " + str(libaries) + ". You may also use other's if you need. The user also has assets in their project, here is a list of their names: " + str(assets) + ". Whenever using a asset, prefix it with assets/ as that is the folder where the assets are stored. Never explain the code or and never do ```python."},
                {"role": "user", "content": program},
            ]
        )
    response = response['choices'][0]['message']['content']
    response = clean(response)
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
    print("Compilation complete!")
if __name__ == "__main__":
    main()