#!bin/bash
pkill -9 -f kodi
DISPLAY=:0 su -c "kodi &" - homeserver