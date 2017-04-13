#!/bin/bash

rm /home/homeassistant/.homeassistant/home-assistant.log && touch /home/homeassistant/.homeassistant/home-assistant.log && chown -R -v homeassistant:homeassistant /home/homeassistant/.homeassistant/home-assistant.log