import os
import json
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "HOTKEY": "ctrl+shift+q",
    "TESSERACT_PATH": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    "OCR_LANG": "eng",
    "TRANS_SOURCE": "en-GB",
    "TRANS_TARGET": "it-IT"
}
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key, val in DEFAULT_CONFIG.items():
                if key not in data:
                    data[key] = val
            return data
    except Exception:
        return DEFAULT_CONFIG.copy()
def save_config(config_dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=4)                            
