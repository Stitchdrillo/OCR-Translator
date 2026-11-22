# Screen Translator

A lightweight desktop utility for instant on-screen text translation. Press a global hotkey, drag a box over any text on your screen—images, games, PDFs, or locked UIs—and get a floating translation right next to your selection.

## Features

- **Global Hotkey Trigger:** Summon the selection overlay from anywhere (defaults to `Ctrl+Shift+Q`).
- **Crisp Region Selection:** Dims the screen with a clear cutout so you can see exactly what you're capturing. Press `Esc` or right-click anytime to cancel.
- **Non-Blocking Background Processing:** OCR and translation run in a background thread pool so your UI never freezes.
- **Smart, DPI-Aware Overlay:** Automatically scales on high-DPI displays and positions itself near your selection without spilling off-screen. Left-click the card to dismiss it.
- **System Tray & Settings UI:** Lives quietly in your system tray with a built-in preferences dialog to change languages, update your Tesseract path, or record a new shortcut.

## Prerequisites

1. **Python 3.10+**
2. **Tesseract-OCR:** `pytesseract` is only a Python wrapper, so you need the Tesseract engine installed on your system:
   - **Windows:** Download and install from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). During setup, be sure to check any extra language packs you want to recognize.
   - **Linux / macOS:** Install via your package manager (`sudo apt install tesseract-ocr` or `brew install tesseract`).

## Installation

**Clone the repository:**
   ```bash
   git clone https://github.com/Stitchdrillo/OCR-Translator.git
   cd OCR-Translator
   ```

**Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the application:

```bash
python main.pyw
```

*(On Windows, you can also double-click `main.pyw` directly to launch it without a terminal window.)*

Look for the **Screen Translator** icon in your system tray.
Press **`Ctrl+Shift+Q`** (or your custom shortcut) to freeze and dim the screen.
**Click and drag** across the text you want to translate.
Wait a moment for the translated card to appear, then **left-click** the card to close it.
Right-click the tray icon and choose **Settings** to configure your languages, Tesseract path, or shortcut.

> **Note for Linux/macOS users:** The `keyboard` library requires root or accessibility permissions to listen for global hotkeys outside the active window.

## Configuration

Settings are managed automatically through the Settings window and saved to `config.json` in the project root.

If `config.json` is missing or corrupted, the app will safely recreate it with default values on startup.

