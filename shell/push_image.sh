#!/bin/bash
sudo su -s /bin/bash homeassistant
source /srv/homeassistant/bin/activate
python3 /home/homeassistant/.homeassistant/shell/push_image.py