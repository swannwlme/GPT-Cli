# <p align="center"> <img src="https://static.vecteezy.com/system/resources/previews/022/841/114/original/chatgpt-logo-transparent-background-free-png.png" width=23 height=23 /> GPT-Cli</p>

![Demo image](readme_assets/image.png)

**gpt_cli** is a useful yet powerful tool developped in Python that adds Chat-GPT and other OpenAI tools directly to your terminal !

</br>
 
## <p align="center">🪛 Current tools</p>
* **Command generator** : Simply explain in the terminal what you want to do and Chat-GPT will generate the command and execute it ! => No more code needed :)

* **Ask GPT** : Just want to ask a question to Chat-GPT you can do it easily here and choose between GPT 3.5-turbo, GPT 4o or GPT 4o-mini

* **Generate Image** : You can quickly generate an image from your shell 

* **Transform text to speech** : Easily transform your text to a speech by using command ```gptc -a <prompt>```

To get every possible commands, simply use ```gptc -h```

```
Usage: gptc [options] <prompt> => Generates command based on the prompt and executes it
Arguments:
-h, --help : Display this help message
-v, --version : Get current version of gpt_cli
-nc, --no-code, --nocode : Generate a response without code
-nf, --no-frame : Removes the frame around the assistant response
-f, --force : Executes the command without asking for confirmation
-4o, --4o : Use GPT-4.0 model
-min, --mini : Use GPT-4-mini model
-img, --image, -i : Generate an image based on the prompt
-prev : Display a preview of the image => needs to be used after -img or --image
-a, --audio : Generate audio based on the prompt
-v, --voice : Specify the voice for the audio (f or m) => needs to be used after -a or --audio
-f : Specify to Chat-GPT the files and folders in your current working directory
-fR : Specify to Chat-GPT the files and folders and sub-files/folders from your current working directory
-L <value> : Specify the depth of the -fR command (default = 3) => to use after -fR
--change-key : Change the OpenAI API key
```


</br>

## <p align="center">⬇️ Install GPT-Cli</p>

### Windows
Simply launch the `install.bat` script

### MacOS / Linux
Give yourself the permission to execute the install.sh script with this command :
```bash
chmod +x install.sh
```
Then, execute the bash script
```bash
./install.sh
```


</br>

## <p align="center">🧠 Examples</p>

![Example Image](readme_assets/image_exemple2.png)
 
![Example Image 2](readme_assets/image3.png)

</br>

<p align="right">By swannwlme</p>
