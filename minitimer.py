#!/usr/bin/env python3
#
# FILE: minitimer.py
# AUTHOR: Miguel Salvá
# ABSTRACT: Timer for the CLI based on the Pomodoro Technique
#
# Supports both CLI and GUI modes.
# CLI usage: python minitimer.py [time]  (e.g. 25m, 50s)
# GUI usage: python minitimer_gui.py

import sys
import time as time_module
import subprocess

DEFAULT_SECONDS = 1500  # 25 minutes (Pomodoro standard)
ALARM = "vinyl-piano_100bpm_C_minor.mp3"


def format_time(seconds: int) -> str:
    """Return a time in seconds as a zero-padded MM:SS string."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def parse_time_arg(arg: str) -> int | None:
    """
    Parse a CLI time argument and return the equivalent number of seconds.
    Accepts formats: Xm (minutes) or Ys (seconds).
    Returns None if the format is invalid.
    """
    if arg.endswith("m"):
        try:
            return int(arg[:-1]) * 60
        except ValueError:
            return None
    elif arg.endswith("s"):
        try:
            return int(arg[:-1])
        except ValueError:
            return None
    return None


def run_cli(seconds: int) -> None:
    """Run the timer in CLI mode, printing countdown to stdout."""
    t = seconds
    while t > 0:
        print(f"Remaining time: {format_time(t)}", end="\r")
        t -= 1
        time_module.sleep(1)
    print("Remaining time: 00:00")
    subprocess.run(["afplay", ALARM], check=False)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        parsed = parse_time_arg(sys.argv[1])
        if parsed is None:
            print(
                "Incorrect time value. "
                "Please specify time in minutes (Xm) or seconds (Ys), "
                "or leave it blank for the default 25 minutes."
            )
            sys.exit(1)
        total = parsed
    else:
        total = DEFAULT_SECONDS

    run_cli(total)
