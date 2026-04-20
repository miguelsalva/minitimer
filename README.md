<h1><img src="images/minitimer_logo.png" width="55%" alt="minitimer logo"></h1>

A minimal, elegant Pomodoro timer for macOS — available as both a **desktop GUI app** and a **CLI tool**.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey?logo=apple)](https://www.apple.com/macos/)

---

## Features

- ⏱ **Circular progress ring** that transitions green → amber → red as time runs out
- ▶️ **Start / Pause / Resume / Reset** controls
- 🎛 **Quick presets** — 5, 15, 25 and 45 minutes
- 🔔 **Alarm sound** when the session completes (non-blocking playback via `afplay`)
- 📳 **Window shake** animation on alarm for a tactile alert feel
- 🌙 **Modern dark UI** — glassmorphism card, pulse animation, system font
- 💻 **CLI mode** still fully available as a lightweight fallback

---

## Screenshots

> *Coming soon*

---

## Installation

### Option A — Run directly (recommended for development)

**1. Clone the repository**

```bash
git clone https://github.com/miguelsalva/minitimer.git
cd minitimer
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Launch the app**

```bash
python minitimer_gui.py
```

> **Requirements:** Python 3.9+, `PySide6`

> [!NOTE]
> On macOS with a Homebrew-managed Python, installing packages system-wide is restricted (PEP 668).
> Using a virtual environment as shown above is the recommended approach.

---

### Option B — Build a native `.app` with PyInstaller

This produces a self-contained `minitimer.app` that works without a Python installation.

```bash
source .venv/bin/activate
pip install pyinstaller
pyinstaller minitimer.spec
```

Copy to Applications:

```bash
cp -r dist/minitimer.app /Applications/
```

The app will appear in Launchpad like any other macOS application.

> **Note:** The resulting `.app` bundle is ~80–150 MB because it includes the Python interpreter and PySide6. This is expected for PyInstaller bundles.

---

## Usage

### GUI (recommended)

```bash
python minitimer_gui.py
```

Select a preset (5m / 15m / 25m / 45m), press **Start**, and focus. The ring drains as time passes; an alarm plays and the window shakes when the session ends.

### CLI

Run with the default Pomodoro duration (25 minutes):

```bash
python minitimer.py
```

Or specify a custom duration:

```bash
python minitimer.py 10m   # 10 minutes
python minitimer.py 90s   # 90 seconds
```

---

## Project Structure

```
minitimer/
├── minitimer.py                     # CLI timer (standalone, no GUI dependency)
├── minitimer_gui.py                 # PySide6 desktop application
├── minitimer.spec                   # PyInstaller build spec
├── requirements.txt                 # Python dependencies
├── TODO.md                          # Upcoming work (Phase 2)
├── vinyl-piano_100bpm_C_minor.mp3   # Alarm sound
└── images/
    ├── tomato.png                   # App icon (512×512 PNG)
    ├── minitimer.icns               # App icon (macOS .icns bundle)
    └── minitimer_logo.png           # README logo
```

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 — Core GUI | ✅ Done | Circular ring, presets, alarm, dark theme, pulse animation |
| 2 — Tomato-shaped window | 🔜 Next | Frameless window shaped like a tomato using `QPainterPath` |
| 3 — Polish & packaging | ✅ Done | Shake animation, `.icns` icon, PyInstaller `.app` bundle |

See [TODO.md](TODO.md) for the detailed task list for Phase 2.

---

## The Pomodoro Technique

The [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) is a time management method that uses timed intervals (typically 25 minutes) of focused work separated by short breaks. minitimer implements the core timer so you can follow this rhythm without distractions.

---

## Contributing

Contributions, ideas, and feedback are welcome. Feel free to open an issue or submit a pull request.

The cleanest entry point for contributors is **Phase 2** (tomato-shaped window) — see [TODO.md](TODO.md) for the task breakdown.

---

## Credits

- Alarm sound: [vinyl-piano](https://samplefocus.com/samples/vinyl-piano) from [Sample Focus](https://samplefocus.com), converted to MP3
- Tomato icon: [Freepik](https://www.flaticon.com/authors/freepik) via [flaticon.com](https://www.flaticon.com)

---

## License

[MIT](LICENSE) © Miguel Salvá
