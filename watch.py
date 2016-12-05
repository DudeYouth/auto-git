#conding:utf-8
import os
import time
import re
import argparse
import threading
import fileinput
import random
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
global cacheTime
cacheTime=1
parser=argparse.ArgumentParser()
lock=threading.Lock();
parser.add_argument('-s',type=str,help='commit的版本号标记字符，默认“:::”',default=':::')
args = parser.parse_args()
sign=args.s;
def gitCommit(commit):
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
    try:
        if cacheTime:
            cacheTime=0
            commit=replaceStr(data)
            gitCommit(commit)
            # time.sleep(1)
            # th=threading.Thread(target=gitCommit,args=(commit,123))
            # th.start();
    except Exception as e:
        print(e)
    finally:
        cacheTime=1
def replaceStr(data):
    lock.acquire()
    try:
        strings=str(time.time())
        for line in fileinput.input(data.src_path,inplace=True,backup=''): 
            strs=line.replace(sign,'');
            if(line!=strs):
                strings=strs
                print('')
            else:
                print(line)
    except:
        print("检测失败")
    finally:
        fileinput.close()
        lock.release();
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