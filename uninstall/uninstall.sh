#!/bin/bash

rm -R ~/gpt_cli
rm /usr/local/bin/gptc

if [ -f /usr/local/bin/gpt ]; then
  rm /usr/local/bin/gpt
fi