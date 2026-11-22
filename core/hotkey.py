"""Global keyboard shortcut listener bridged to Qt signals."""

import logging
from typing import Any

import keyboard
from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class HotkeyListener(QObject):
    """Registers a system-wide hotkey and emits a thread-safe Qt signal when pressed."""

    triggered = pyqtSignal()

    def __init__(self, shortcut: str, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.shortcut = shortcut
        self._hook: Any = None
        self._register(shortcut)

    def update_hotkey(self, new_shortcut: str) -> None:
        """Replace the active global shortcut with a new key combination."""
        self.stop()
        self.shortcut = new_shortcut
        self._register(new_shortcut)

    def stop(self) -> None:
        """Unregister the active global hotkey hook if one is bound."""
        if self._hook is None:
            return
        try:
            keyboard.remove_hotkey(self._hook)
        except Exception as exc:
            logger.debug("Failed to remove hotkey hook cleanly: %s", exc)
        finally:
            self._hook = None

    def _register(self, shortcut: str) -> None:
        """Bind a keyboard hook that forwards presses to `triggered`."""
        try:
            self._hook = keyboard.add_hotkey(shortcut, self.triggered.emit)
        except Exception as exc:
            logger.error("Failed to register hotkey '%s': %s", shortcut, exc)
            self._hook = None
