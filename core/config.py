"""Application configuration model and JSON persistence."""

from dataclasses import dataclass
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Resolve config.json at the project root regardless of current working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"


@dataclass(frozen=True)
class AppConfig:
    """Immutable configuration settings for OCR, translation, and hotkeys."""

    hotkey: str = "ctrl+shift+q"
    tesseract_path: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    ocr_lang: str = "eng"
    trans_source: str = "en-GB"
    trans_target: str = "it-IT"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppConfig":
        """Build an AppConfig from a JSON dictionary, filling missing keys with defaults."""
        defaults = cls()
        return cls(
            hotkey=str(data.get("HOTKEY", defaults.hotkey)),
            tesseract_path=str(data.get("TESSERACT_PATH", defaults.tesseract_path)),
            ocr_lang=str(data.get("OCR_LANG", defaults.ocr_lang)),
            trans_source=str(data.get("TRANS_SOURCE", defaults.trans_source)),
            trans_target=str(data.get("TRANS_TARGET", defaults.trans_target)),
        )

    def to_dict(self) -> dict[str, str]:
        """Serialize settings into the standard JSON schema."""
        return {
            "HOTKEY": self.hotkey,
            "TESSERACT_PATH": self.tesseract_path,
            "OCR_LANG": self.ocr_lang,
            "TRANS_SOURCE": self.trans_source,
            "TRANS_TARGET": self.trans_target,
        }


def load_config(path: Path = CONFIG_PATH) -> AppConfig:
    """Load configuration from disk, creating a default file if missing or unreadable."""
    if not path.exists():
        default_config = AppConfig()
        save_config(default_config, path)
        return default_config

    try:
        with path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
        if not isinstance(raw_data, dict):
            raise ValueError("Configuration root must be a JSON object.")
        return AppConfig.from_dict(raw_data)
    except Exception as exc:
        logger.warning("Failed to read %s (%s); falling back to defaults.", path, exc)
        return AppConfig()


def save_config(config: AppConfig, path: Path = CONFIG_PATH) -> None:
    """Persist the given configuration to disk as formatted JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(config.to_dict(), file, indent=4)
