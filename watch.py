#conding=utf8
import os
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

global cacheTime
cacheTime=0

class EventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
    def on_created(self,data):
        action()
    def on_deleted(self,data):
        action()
    def on_modified(self,data):
        print(data)
        action()
    def on_moved(self,data):
        action()
def action():
    global cacheTime
    if int(time.time())-int(cacheTime)>2:
        time.sleep(1)
        os.system('git pull origin master')
        os.system('git add .')
        os.system('git commit -m"test"')
        os.system('git push origin master')
        cacheTime=time.time()
if __name__=='__main__':
    ev=EventHandler()
    observer=Observer()
    observer.schedule(ev, os.getcwd(), recursive=True)
    observer.start()
    print('Watching...')
    print(time.time())
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()