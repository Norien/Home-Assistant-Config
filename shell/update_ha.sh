#!/bin/bash

# Become user 'hass'
sudo su -s /bin/bash homeassistant <<'EOF'
# Activate the virtualenv
source /srv/homeassistant/bin/activate
# Install Home Assistant
pip3 install --upgrade homeassistant
exit
EOF

# Restart Home Assistant
sudo systemctl restart home-assistant@homeserver