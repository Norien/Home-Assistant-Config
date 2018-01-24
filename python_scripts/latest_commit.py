import os.path, time, datetime
timestamp=(os.path.getmtime("/home/homeassistant/.homeassistant/.git/index"))
dt_obj = time.strftime('%b %d @ %I:%M%p', time.localtime(timestamp))
print dt_obj