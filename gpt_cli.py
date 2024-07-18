from openai import OpenAI
import os
import sys
import webbrowser
import requests
import json
from pathlib import Path

version = "1.0.0"

config_file = f"{str(Path.home())}/gpt_cli/gpt_cli.json"

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

def get_gpt_response(prompt, model):
    prompt = f"You are a Command Line Interface expert and your task is to provide functioning shell commands. Return a CLI command and nothing else - do not send it in a code block, quotes, or anything else, just the pure text CONTAINING ONLY THE COMMAND. If possible, return a one-line bash command or chain many commands together. Return ONLY the command ready to run in the terminal. The command should do the following : {prompt}"
    response = client.chat.completions.create(
        model=model, 
        messages=[{"role": "system", "content": prompt}]
    )
    print(f"command : {response.choices[0].message.content}")
    return response.choices[0].message.content

def gpt_no_code_response(prompt, model):
    response = client.chat.completions.create(
        model=model, 
        messages=[{"role": "system", "content": prompt}]
    )
    print("\n")
    print(response.choices[0].message.content)
    print(" ")

def generate_image(prompt, noprev):
    print("Generating image...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    if not noprev:
        webbrowser.open(response.data[0].url)
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
    print("-img, --image, -i : Generate an image based on the prompt")
    print("-noprev : Do not display the preview of the image => needs to be used after -img or --image")
    print("-a, --audio : Generate audio based on the prompt")
    print("-v, --voice : Specify the voice for the audio (f or m) => needs to be used after -a or --audio")
    print("--change-key : Change the OpenAI API key")
    print("\n")

def generate_audio(prompt, voice):
    print("Generating audio...")
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=prompt,
        
    )
    filename = 'generated.mp3'
    while os.path.exists(filename):
        filename = filename.replace(".mp3", "_1.mp3")
    response.write_to_file(filename)
    
    print(f"Audio saved as {filename}")
    



arguments = ["-h", "--help", "-nc", "--no-code", "--nocode", "-4o", "--4o", "-no-code", "-img", "--image", "-i", "-noprev", "--audio", "-a", "--voice", "-v", "--change-key", "-v", "--version"]

if len(sys.argv) < 2:
    print("Usage: gpt [options] <prompt>")
    print("Use -h or --help for more options\n")
    sys.exit(1)

code = True
gpt4o = False
img = False
noprev = False
audio = False
voice = "onyx"

if sys.argv[1] in ["-h", "--help"]:
    get_help()
    sys.exit(0)

for arg in sys.argv[1:]:
    if arg in arguments:
        if arg in ["-nc", "--no-code", "--nocode"]:
            code = False
            sys.argv.remove(arg)
        elif arg in ["-4o", "--4o"]:
            gpt4o = True
            sys.argv.remove(arg)
        elif arg in ["-img", "--image", "-i"]:
            gpt4o = False
            code=False
            img = True
            if sys.argv[sys.argv.index(arg)+1] in ["-noprev"]:
                noprev = True
                sys.argv.remove(sys.argv[sys.argv.index(arg)+1])
            sys.argv.remove(arg)
            break
        elif arg in ["-audio", "-a"]:
            gpt4o = False
            code=False
            img = False
            audio = True
            if sys.argv[sys.argv.index(arg)+1] in ["-v", "--voice"]:
                voice = sys.argv[sys.argv.index(arg)+2]
                if voice == "female" or "f":
                    voice = "nova"
                else:
                    voice = "onyx"
                sys.argv.remove(sys.argv[sys.argv.index(arg)+1])
                sys.argv.remove(sys.argv[sys.argv.index(arg)+1])
            sys.argv.remove(arg)
            break
        elif arg in ["--change-key"]:
            print("Please enter your OpenAI api key : ")
            api = input()
            with open('gpt_cli.json', 'w') as f:
                json.dump({"api_key": api}, f)
            sys.exit(0)
        elif arg in ["-v", "--version"]:
            print(f"\nCurrent gpt_cli version : {version}\n")
            exit(0)
        else :
            sys.argv.remove(arg)
    else:
        break


if gpt4o:
    model = "gpt-4.0"
else:
    model = "gpt-3.5-turbo"

if img:
    prompt = " ".join(sys.argv[1:])
    generate_image(prompt, noprev)
elif audio:
    prompt = " ".join(sys.argv[1:])
    generate_audio(prompt, voice)
elif code:
    prompt = " ".join(sys.argv[1:])
    print(get_gpt_response(prompt, model))
else:
    prompt = " ".join(sys.argv[1:])
    gpt_no_code_response(prompt, model)