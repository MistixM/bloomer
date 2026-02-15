# Bloomer

![Cover](https://i.postimg.cc/3NpJgrRH/bloomer-cover.jpg)

Automated clicker for farming resources in the Bloom Telegram mini-game. Detects flower elements on screen via pixel color recognition and clicks them automatically.

## Features

- Automatic pixel detection and clicking for Bloom game flowers
- Configurable hotkey (A-Z) to pause/resume the clicker
- Three accuracy levels: **Easy**, **Medium**, **Extreme**
- Modern dark-themed GUI built with CustomTkinter
- Console version available as a lightweight alternative
- Pre-built Windows executable (no Python required)

## Requirements

- Python 3.8+
- Telegram Desktop with Bloom mini-game open
- Windows OS

## Installation

```bash
git clone https://github.com/your-username/bloomer.git
cd bloomer/pc
pip install pyautogui pygetwindow pynput keyboard customtkinter pillow pyfiglet
```

## Usage

### GUI Version

```bash
python main.py
```

1. Open Bloom in Telegram Desktop
2. Accept the license agreement on first launch
3. Select your preferred hotkey and accuracy level
4. Press the hotkey to start/pause the clicker

### Console Version

```bash
python main_console.py
```

Press `S` to toggle the clicker on/off.

### Pre-built Executable

Download `Bloomer.exe` from the `pc/output/1.0.2/` directory and run it directly — no Python installation needed.

## Accuracy Levels

| Level    | Step Size | Description                  |
|----------|-----------|------------------------------|
| Easy     | 40px      | Fastest scanning, lower precision |
| Medium   | 25px      | Balanced speed and accuracy  |
| Extreme  | 23px      | Slowest scanning, highest precision |

## Project Structure

```
bloom/
├── pc/
│   ├── main.py              # GUI version
│   ├── main_console.py      # Console version
│   ├── data.json             # User preferences
│   ├── images/               # UI assets and icons
│   └── output/               # Pre-built executables
│       ├── 1.0.1/
│       └── 1.0.2/
└── preview.png
```

