from openai import OpenAI
import os
import sys
import webbrowser
import requests
import json
from pathlib import Path
import platform
from rich.console import Console
from rich.markdown import Markdown


version = "1.5"

config_file = f"{str(Path.home())}/gpt_cli/gpt_cli.json"

# Check the os
# Get the name of the operating system
os_name = platform.system()

if not os.path.exists(config_file):
    print("No OpenAI api key found.")
    api = input("Please enter your OpenAI api key : ")
    with open(config_file, 'w') as f:
        json.dump({"api_key": api}, f)

# Load the API key from gpt_cli.json
with open(config_file) as f:
    data = json.load(f)
    api = data['api_key']

valid_key = False

while not valid_key:
    try :
        client = OpenAI(api_key=api)
        valid_key = True
    except:
        print("Invalid API key")
        api = input("Please enter your OpenAI api key : ")
        with open('gpt_cli.json', 'w') as f:
            json.dump({"api_key": api}, f)


code = True
model = "gpt-3.5-turbo"
img = False
prev = False
audio = False
voice = "onyx"
give_current_files=False
give_files = False
max_depth = 3
console = Console()

def printCommand(command):
    markdown = Markdown(f"```bash\n $ {command}\n```", style="green")
    console.print(markdown)

def printText(text):
    markdown = Markdown(text)
    console.print(markdown)

def list_directory_structure(root_dir, max_depth, current_depth=0, prefix=""):
    if current_depth > max_depth:
        return ""
    
    output = ""
    items = os.listdir(root_dir)
    pointers = ['├── '] * (len(items) - 1) + ['└── ']
    
    for pointer, item in zip(pointers, items):
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            output += f"{prefix}{pointer}{item}\n"
            if pointer == '└── ':
                next_prefix = prefix + '    '
            else:
                next_prefix = prefix + '│   '
            output += list_directory_structure(path, max_depth, current_depth + 1, next_prefix)
        else:
            output += f"{prefix}{pointer}{item}\n"
    
    return output

def get_files(prompt):
    if give_current_files:
        prompt += f"\nHere is the list of contents in the current directory : {os.listdir()}"
    elif give_files :
        dir_list = list_directory_structure(os.getcwd(), max_depth)
        prompt += f"\nHere is the list of contents in the current directory : \n{dir_list}"
    return prompt

def get_gpt_response(prompt, model, useMessages=False):
    prompt = f"You are a Command Line Interface expert and your task is to provide functioning shell commands on os : {os_name}. Return a CLI command and nothing else - do not send it in a code block, quotes, or anything else, just the pure text CONTAINING ONLY THE COMMAND. If possible, return a one-line command or chain many commands together. Return ONLY the command ready to run in the terminal. The command should do the following : {prompt}"
    prompt = get_files(prompt)
    print("Generating...")
    response = client.chat.completions.create(
        model=model, 
        messages=[{"role": "system", "content": prompt}]
    )
    printCommand(response.choices[0].message.content)
    # print(f"command : {response.choices[0].message.content}")
    return response.choices[0].message.content

def gpt_no_code_response(prompt, model):
    prompt = get_files(prompt)
    print("Generating...")
    response = client.chat.completions.create(
        model=model, 
        messages=[{"role": "system", "content": prompt}]
    )
    
    print("\n")
    printText(response.choices[0].message.content)
    print(" ")

def generate_image(prompt, prev):
    print("Generating image...")
    prompt = get_files(prompt)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    if prev:
        webbrowser.open(response.data[0].url)
    else :
        print(f"Image URL : {response.data[0].url}")
    image_url = response.data[0].url
    img_data = requests.get(image_url).content
    filename = 'generated.png'
    while os.path.exists(filename):
        filename = filename.replace(".png", "_1.png")
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    
    print(f"Image saved as {filename}")

def get_help():
    print("\nUsage: gptc [options] <prompt> => Generates command based on the prompt and executes it")
    print("Arguments:")
    print("-h, --help : Display this help message")
    print("-v, --version : Get current version of gpt_cli")
    print("-nc, --no-code, --nocode : Generate a response without code")
    print("-4o, --4o : Use GPT-4.0 model")
    print("-min, --mini : Use GPT-4-mini model")
    print("-img, --image, -i : Generate an image based on the prompt")
    print("-prev : Display a preview of the image => needs to be used after -img or --image")
    print("-a, --audio : Generate audio based on the prompt")
    print("-v, --voice : Specify the voice for the audio (f or m) => needs to be used after -a or --audio")
    print("-f : Specify to Chat-GPT the files and folders in your current working directory")
    print("-fR : Specify to Chat-GPT the files and folders and sub-files/folders from your current working directory")
    print("-L <value> : Specify the depth of the -fR command (default = 3) => to use after -fR")
    print("--change-key : Change the OpenAI API key")
    print("\n")

def generate_audio(prompt, voice):
    prompt = get_files(prompt)
    print("Generating audio...")
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=prompt,
    )
    
    print("Saving audio file...")
    filename = 'generated.mp3'
    while os.path.exists(filename):
        filename = filename.replace(".mp3", "_1.mp3")
    response.write_to_file(filename)
    
    
    print(f"Audio saved as {filename}")



arguments = ["-h", "--help", "-nc", "--no-code", "--nocode", "-4o", "--4o", "-min", "--mini", "-no-code", "-img", "--image", "-i", "-prev", "--audio", "-a", "--voice", "-v", "--change-key", "-v", "--version", "-f", "-fR", "-L"]

if len(sys.argv) < 2:
    print("Usage: gptc [options] <prompt>")
    print("Use -h or --help for more options\n")
    sys.exit(1)

if sys.argv[1] in ["-h", "--help"]:
    get_help()
    sys.exit(0)

for arg in sys.argv[1:]:
    if arg in arguments:
        match arg:
            case "-nc" | "--no-code" | "--nocode":
                code = False
                sys.argv.remove(arg)

            case "-4o" | "--4o":
                model = "gpt-4.0"
                sys.argv.remove(arg)

            case "-min" | "--mini":
                model = "gpt-4o-mini"
                sys.argv.remove(arg)

            case "-img" | "--image" | "-i":
                gpt4o = False
                code = False
                img = True
                next_arg = sys.argv[sys.argv.index(arg) + 1]
                if next_arg == "-prev":
                    prev = True
                    sys.argv.remove(next_arg)
                sys.argv.remove(arg)
                break

            case "-audio" | "-a":
                gpt4o = False
                code = False
                img = False
                audio = True
                next_arg = sys.argv[sys.argv.index(arg) + 1]
                if next_arg in ["-v", "--voice"]:
                    voice = sys.argv[sys.argv.index(arg) + 2]
                    if voice in ["female", "f"]:
                        voice = "nova"
                    else:
                        voice = "onyx"
                    sys.argv.remove(next_arg)
                    sys.argv.remove(voice)
                sys.argv.remove(arg)
                break

            case "--change-key":
                print("Please enter your OpenAI api key: ")
                api = input()
                with open('gpt_cli.json', 'w') as f:
                    json.dump({"api_key": api}, f)
                sys.exit(0)

            case "-v" | "--version":
                print(f"\nCurrent gpt_cli version: {version}\n")
                sys.exit(0)

            case "-f":
                give_current_files = True
                give_files = False
                sys.argv.remove(arg)

            case "-fR":
                give_files = True
                sys.argv.remove(arg)

            case "-L":
                max_depth = int(sys.argv[sys.argv.index(arg) + 1])
                sys.argv.remove(arg)
                sys.argv.remove(str(max_depth))

            case _:
                sys.argv.remove(arg)
    else:
        break

if img:
    prompt = " ".join(sys.argv[1:])
    generate_image(prompt, prev)
elif audio:
    prompt = " ".join(sys.argv[1:])
    generate_audio(prompt, voice)
elif code:
    prompt = " ".join(sys.argv[1:])
    os.system(get_gpt_response(prompt, model))
else:
    prompt = " ".join(sys.argv[1:])
    gpt_no_code_response(prompt, model)