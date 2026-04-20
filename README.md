<h1><img src="images/minitimer_logo.png" width="55%" alt="minitimer logo"></h1>

A minimal, elegant Pomodoro timer for macOS — available as both a **desktop GUI app** and a **CLI tool**.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?logo=apple)](https://www.apple.com/macos/)

---

## Features

- ⏱ **Circular progress ring** that transitions from green → amber → red as time runs out
- ▶️ **Start / Pause / Resume / Reset** controls
- 🎛 **Quick presets** — 5, 15, 25 and 45 minutes
- 🔔 **Alarm sound** when the session completes (non-blocking playback via `afplay`)
- 🌙 **Modern dark UI** — glassmorphism card, subtle animations, system font
- 💻 **CLI mode** still fully available as a lightweight fallback

---

## Screenshots

> *Coming soon*

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/miguelsalva/minitimer.git
cd minitimer
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Requirements:** Python 3.9+, `PySide6`, `playsound`

> [!NOTE]
> On macOS with a Homebrew-managed Python, installing packages system-wide is restricted (PEP 668).
> Using a virtual environment as shown above is the recommended approach.

---

## Usage

### GUI (recommended)

```bash
python3 minitimer_gui.py
```

Select a preset (5m / 15m / 25m / 45m), press **Start**, and focus. The ring fills down as time passes and an alarm plays when the session ends.

### CLI

Run with the default Pomodoro duration (25 minutes):

```bash
python3 minitimer.py
```

Or specify a custom duration:

```bash
python3 minitimer.py 10m   # 10 minutes
python3 minitimer.py 90s   # 90 seconds
```

---

## Project Structure

```
minitimer/
├── minitimer.py          # CLI timer (standalone, no GUI dependency)
├── minitimer_gui.py      # PySide6 desktop application
├── requirements.txt      # Python dependencies
├── vinyl-piano_100bpm_C_minor.mp3   # Alarm sound
└── images/
    └── minitimer_logo.png
```

---

## The Pomodoro Technique

The [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) is a time management method that uses timed intervals (typically 25 minutes) of focused work separated by short breaks. minitimer implements the core timer functionality so you can follow this rhythm without distractions.

---

## Credits

- Alarm sound: [vinyl-piano](https://samplefocus.com/samples/vinyl-piano) from [Sample Focus](https://samplefocus.com), converted to MP3
- Tomato icon: [Freepik](https://www.flaticon.com/authors/freepik) via [flaticon.com](https://www.flaticon.com)

---

## Contributing

Contributions, ideas and feedback are welcome. Feel free to open an issue or submit a pull request.

---

## License

[MIT](LICENSE) © Miguel Salvá
