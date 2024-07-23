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
pip install -r data_files/requirements.txt

echo "Do you also want to be able to use gpt <prompt> with gptc <prompt> ? (y/n)"
read answer

#remove the gpt_cli.py file if it exists
if [ -f ~/gpt_cli ]; then
  rm -R ~/gpt_cli
fi

#remove the gptc command if it exists
if [ -f /usr/local/bin/gptc ]; then
  rm /usr/local/bin/gptc
fi

#remove the gpt command if it exists
if [ -f /usr/local/bin/gpt ]; then
  rm /usr/local/bin/gpt
fi

#add the gpt_cli command to the PATH
echo '#!/bin/bash
python ~/gpt_cli/gpt_cli.py "$@"' > gptc

mv gptc /usr/local/bin/gptc
chmod +x /usr/local/bin/gptc

if [[ "$answer" == "y" || "$answer" == "Y" ]];then
  cp /usr/local/bin/gptc /usr/local/bin/gpt
  chmod +x /usr/local/bin/gpt
fi

mkdir ~/gpt_cli
cp data_files/gpt_cli.py ~/gpt_cli

echo " "
echo "Installation complete have fun :)"