#!/bin/bash

#check if root and exit if it is
if [ "$EUID" -eq 0 ]; then
  echo "Please do not run this script as root"
  exit
fi

#check if python is installed
if ! [ -x "$(command -v python)" ]; then
  echo 'Error: you need to install python and add it the PATH in order to use gpt_cli.' >&2
  exit 1
fi

#check if pip is installed
if ! [ -x "$(command -v pip)" ]; then
  echo 'Error: you need to install pip and add it to the PATH in order to use gpt_cli.' >&2
  exit 1
fi

#install the required python packages
pip install -r requirements.txt

#add the gpt_cli command to the PATH
echo '#!/bin/bash
python ~/gpt_cli/gpt_cli.py "$@"' > gptc

mv gptc /usr/local/bin/gptc
chmod +x /usr/local/bin/gptc

mkdir ~/gpt_cli
cp gpt_cli.py ~/gpt_cli

echo " "
echo "Installation complete have fun :)"