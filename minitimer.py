#!/usr/bin/env python3

import sys
import time

DEFAULT_TIME = 1500  # 25min by default for Pomodoro Technique


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


t = DEFAULT_TIME
while t > 0:
    print("Remaining time: ", end = "")
    format_time(t)
    t = t - 1
    time.sleep(1)

