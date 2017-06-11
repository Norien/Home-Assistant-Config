#!/bin/bash
pkill -9 -f buffer.py
rm /home/homeassistant/.homeassistant/shell/gif_maker/nohup.out
cd /home/homeassistant/.homeassistant/shell/gif_maker
source venv/bin/activate
nohup python buffer.py -c config.yaml &