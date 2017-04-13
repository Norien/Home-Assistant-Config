#!/usr/bin/python

import json
import requests
import StringIO
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def TimestampMillisec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) 

def formatRecursiveDict(data):
    return dict(map(lambda (x, y): (x.encode('ascii'), y.encode('ascii')), data.iteritems()))

def formatDict(data):
    return dict(map(lambda (x, y): (x.encode('ascii'), y.encode('ascii')) if x != 'details' else (x.encode('ascii'), formatRecursiveDict(y)), data.iteritems()))

r = requests.get('https://ADDRESS TO API');
s = str(r.text)[17:-1]
data = json.loads(s);
schedule = data['schedules']['S1595']
print min(filter(lambda time: int(time) * 1000 > current_milli_time(), schedule.iterkeys()))