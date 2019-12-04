#!/usr/bin/env python3
#
# FILE: minitimer.py
# AUTHOR: Miguel Salvá
# ABSTRACT: Timer for the CLI based on the Pomodoro Technique
#
# This program requires the playsound library to run

import sys
import time
from playsound import playsound

DEFAULT_TIME = 1500  # 25min by default for Pomodoro Technique
ALARM = "vinyl-piano_100bpm_C_minor.mp3"


def format_time(s):
    """Function that gets a time in seconds and returns it in format MM:SS"""
    minutes = int(s / 60)
    seconds = s % 60
    if minutes < 10 and seconds < 10:
        print("0"+ str(minutes) + ":" + "0" + str(seconds), end="\r")
    else:
        if minutes >= 10 and seconds < 10:
            print(str(minutes) + ":" + "0" + str(seconds), end="\r")
        else:
            if minutes < 10 and seconds >= 10:
                print("0" + str(minutes) + ":" + str(seconds), end="\r")
            else:
                print(str(minutes) + ":" + str(seconds), end="\r")


# Main
if len(sys.argv) > 1:
    if sys.argv[1][len(sys.argv[1])-1:len(sys.argv[1])] == "m":
        t = int(sys.argv[1][0:len(sys.argv[1])-1]) * 60
    else:
        if sys.argv[1][len(sys.argv[1])-1:len(sys.argv[1])] == "s":
            t = int(sys.argv[1][0:len(sys.argv[1])-1])
        else:
            print("Incorrect time value. Please specify time in minutes (Xm) or seconds (Ys) or leave it blank (25m by default)")
else:
    t = DEFAULT_TIME

while t > 0:
    print("Remaining time: ", end = "")
    format_time(t)
    t = t - 1
    time.sleep(1)
print("Remaining time: 00:00")    
playsound(ALARM)
