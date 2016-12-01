#conding:utf-8
import os
import time
import re
import argparse
import threading
import fileinput
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
global cacheTime
cacheTime=0
parser=argparse.ArgumentParser()
parser.add_argument('-s',type=str,help='commit的版本号标记字符，默认“:::”',default=':::')
args = parser.parse_args()
sign=args.s;
def gitCommit(commit,test):
    try:
        os.system('git pull origin master')
        os.system('git add .')
        os.system('git commit -m"'+commit.replace(sign,'')+'"')
        os.system('git push origin master')
    except:
        print("push失败！")
class EventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
    def on_created(self,data):
        action(data)
    def on_deleted(self,data):
        action(data)
    def on_modified(self,data):
        action(data)
    def on_moved(self,data):
        action(data)
def action(data):
    global cacheTime
    if int(time.time())-int(cacheTime)>2:
        commit=replaceStr(data)
        time.sleep(1)
        th=threading.Thread(target=gitCommit,args=(commit,123))
        th.start();
        cacheTime=time.time()
def replaceStr(data):
    strings=str(time.time())
    for line in fileinput.input(data.src_path,inplace=1):
        strs=line.replace(sign,'');
        if(line!=strs):
            strings=strs
            print('')
        else:
            print(line)
    return strings
if __name__=='__main__':
    ev=EventHandler()
    observer=Observer()
    observer.schedule(ev, os.getcwd(), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()