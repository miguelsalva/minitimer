#!/usr/bin/env python3

import time

DEFAULT_TIME = 1500  # 25min by default for Pomodoro Technique


def format_time(s):
    """Function that gets a time in seconds and returns it in format MM:SS"""
    minutes = int(s / 60)
    seconds = s % 60
    print(str(minutes) + ":" + str(seconds))


t = DEFAULT_TIME
while t > 0:
    print("Remaining time:" )
    format_time(t)
    t = t - 1
    time.sleep(1)

