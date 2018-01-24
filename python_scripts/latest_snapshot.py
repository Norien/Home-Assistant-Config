import os.path, time, datetime
timestamp=(os.path.getmtime("/mnt/backup/snapshots"))
dt_obj = time.strftime('%b %d @ %I:%M%p', time.localtime(timestamp))
print dt_obj