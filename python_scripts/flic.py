#!/usr/bin/python
# coding: utf8
word = "value_json.processes.flic"
result = "false"
with open('/home/homeassistant/.homeassistant/home-assistant.log') as file: 
	data = file.read() 

if word in data:
    result = "true"
print result