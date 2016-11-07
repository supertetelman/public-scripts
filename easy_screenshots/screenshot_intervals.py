#!/bin/env/python

'''
Script will take a SCREEN_SHOT_DIR and INTERVAL. It will then take a screenshot every interval and save
it into the directory. The filename will be of the format "data_time.png".

The snapshots are done in a background thread that allows for screenshots to be taken in very quick intervals. Without threading screenshots can only be taken in 2-3 second intervals.

The script currently grabs the entire screen. The screen grabbed is defined by the DISPLAYS variable.
this should be a number (0,1,2,3,4) corresponding to the monitor number you wish to capture.

Before running this you will need to install Desktopmagic:
    pip install Desktopmagic

You may also want to install the following three packages:
    pip install pyscreenshot
    pip install Pillow
    pip install pypiwin32
'''


from __future__ import print_function
#import pyscreenshot
import os
import datetime
import time
import threading
import argparse
from desktopmagic.screengrab_win32 import (
    getDisplayRects, getRectAsImage)

__author__  = "Adam Tetelman"


class Screenshot(threading.Thread):
    '''Class that is in charge of determining proper file names and taking a screenshot.
    This class uses pyscreenshot and Pillow which is only capable of grabbing the main screen.
    '''
    def __init__(self,directory):
        if directory[-1] != "\\":
            directory += "\\" # XXX: Directory names must end in \
        self.directory = directory
	threading.Thread.__init__(self)

    def get_file_name(self, **args):
        '''take the directory name return a full file name based off the current time'''
        return  self.directory + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f.png")

    def get_image(self):
        '''Return an image from the primary screen using pyscreenshot'''
        return pyscreenshot.grab() 
    
    def run(self):
        '''Get an image and save it to file'''
        self.get_image().save(self.get_file_name())
       

class Monitorshot(Screenshot):
    '''This  class allows you to specify a specific monitor to shoot'''
    def __init__(self, directory, monitor):
	self.monitor = monitor
        super(Monitorshot, self).__init__(directory)

    def get_image(self):
        '''Return an image from a specified display'''
        display = getDisplayRects()[self.monitor] # get the dimensions of the monitor
	return getRectAsImage(display)


class Rectshot(Screenshot):
    '''This  class allows you to specify a specific rectangle to shoot'''
    def __init__(self, directory, rect):
	self.rect = rect
        super(Rectshot, self).__init__(directory)

    def get_image(self):
        '''Get an image from a specific rectangle'''
	return getRectAsImage(self.rect)


def take_screen_shot(directory, display, Shot):
    '''Because taking a screenshot can be slow we run them in a thread that works in the background
    This allows you to set an interval that is smaller than 2 seconds.
    '''
    thread = Shot(directory,display)
    thread.start()


def verify_monitor(display):
    '''Verify the monitor chosen is valid.'''
    if len(getDisplayRects()) <= display:
        return True
    return False
 

def test(directory):
    take_screen_shot(directory, None, Screenshot)
    take_screen_shot(directory, 0, Monitorshot)
    take_screen_shot(directory, (0,0,256,256), Rectshot)


def main(directory, interval, display):
    '''Continually take a snapshot every interval'''
    if directory is None or not os.path.isdir(directory): # XXX: Verify the directory exists
        print("The directory %s does not seem to exist" %(directory))
	exit()
    if not os.access(directory, os.W_OK): # XXX: Verify the directory is writable
        print("The directory %s does not seem to be writable" %(directory))
	exit()
    if interval is None or interval <= .0001:
        print("The interview you specified seems to low")
    print("Beginning script.\n Every %f second a screenshot of monitor %s will be saved to %s" %(
    interval, str(display), directory))

    screenshot_class = Monitorshot
    if isinstance(display, tuple):
        screenshot_class = Rectshot

    while True:
        take_screen_shot(directory, display, screenshot_class)
        time.sleep(interval)


parser = argparse.ArgumentParser(description="A simple utility to take snapshots on an interval.")
parser.add_argument('-d', '--directory', dest='SCREEN_SHOT_DIR', action='store',default="C:\Users\Public\Pictures", help='The directory to save screenshot in.') 
parser.add_argument('-i', '--interval', dest='INTERVAL', action='store', default=.5, type=float, help='The interval at which to take screenshots. Formatted in seconds (10, .5, etc.)') 
parser.add_argument('-a', '--area', dest='AREA', action='store', help='An area of the screen to record. This argument should be 4 integers in quotes  as in: "1 1 10 10"') 
parser.add_argument('-m', '--monitor', dest='DISPLAY', action='store', type=int, help='A specific monitor to record. Expect an integer input ("0" or "1")') 


args = parser.parse_args()
if args.AREA is not None:
    args.DISPLAY = tuple([int(x) for x in args.AREA.strip().split(" ")]) # XXX: Properly format the input
    if len(args.DISPLAY) != 4:
        print("Area formatted incorrectly.")
	exit()
elif args.DISPLAY is None:
    print("Defaulting to monitor 0")
    args.DISPLAY = 0 # XXX: Default to monitor 0 if none specified
elif verify_monitor(args.DISPLAY): # XXX: Verify monitor exists
    print("Specified monitor is out of range")
    exit()


if False:
    test(args.SCREEN_SHOT_DIR)


if __name__ == "__main__":
    main(args.SCREEN_SHOT_DIR, args.INTERVAL, args.DISPLAY)

