"""Application controller coordinating hotkeys, UI windows, and background workers."""

import logging

from PyQt6.QtCore import QObject, QThreadPool
from PyQt6.QtWidgets import QApplication

from core.capture import capture_region
from core.config import AppConfig, load_config
from core.hotkey import HotkeyListener
from core.worker import TranslationWorker
from ui.overlay import TranslationOverlay
from ui.selector import SelectionCanvas
from ui.settings import SettingsWindow
from ui.tray import TrayIcon

logger = logging.getLogger(__name__)


class ScreenTranslatorApp(QObject):
    """Orchestrates tray actions, screen capture, background translation, and overlays."""

    def __init__(self, qt_app: QApplication) -> None:
        super().__init__(qt_app)
        self.config: AppConfig = load_config()
        self._thread_pool = QThreadPool.globalInstance()
        self._request_id = 0

        self._canvas: SelectionCanvas | None = None
        self._overlay: TranslationOverlay | None = None
        self._settings_window: SettingsWindow | None = None

        self.tray = TrayIcon(qt_app)
        self.tray.settings_action.triggered.connect(self.open_settings)

        self.listener = HotkeyListener(self.config.hotkey)
        self.listener.triggered.connect(self.open_selection_canvas)

    def start(self) -> None:
        """Display the system tray icon and begin listening in the background."""
        self.tray.show()
        logger.info("Screen Translator running in background (hotkey: %s).", self.config.hotkey)

    def shutdown(self) -> None:
        """Clean up global hooks and active windows before application exit."""
        self.listener.stop()
        self._close_active_overlay()
        self._close_active_canvas()

    def open_selection_canvas(self) -> None:
        """Dismiss any open overlay or canvas and present a fresh region selector."""
        self._close_active_overlay()
        self._close_active_canvas()

        self._canvas = SelectionCanvas()
        self._canvas.area_selected.connect(self._on_area_selected)
        self._canvas.show()

    def open_settings(self) -> None:
        """Open the settings window, replacing any existing instance."""
        if self._settings_window is not None:
            self._settings_window.close()

        self._settings_window = SettingsWindow()
        self._settings_window.settings_saved.connect(self._reload_settings)
        self._settings_window.show()
        self._settings_window.activateWindow()

    def _reload_settings(self) -> None:
        """Reload configuration from disk and update the global shortcut."""
        self.config = load_config()
        self.listener.update_hotkey(self.config.hotkey)
        logger.info("Settings reloaded (hotkey: %s).", self.config.hotkey)

    def _on_area_selected(self, x: int, y: int, width: int, height: int) -> None:
        """Capture the selected region immediately and offload OCR/translation."""
        if width <= 0 or height <= 0:
            return

        image = capture_region(x, y, width, height)
        self._request_id += 1

        worker = TranslationWorker(
            request_id=self._request_id,
            image=image,
            region=(x, y, width, height),
            config=self.config,
        )
        worker.signals.finished.connect(self._on_translation_ready)
        self._thread_pool.start(worker)

    def _on_translation_ready(
        self,
        request_id: int,
        translated_text: str,
        region: tuple[int, int, int, int],
    ) -> None:
        """Display the translated text overlay if the response matches the latest request."""
        if request_id != self._request_id:
            return

        self._close_active_overlay()
        self._overlay = TranslationOverlay(translated_text)
        self._overlay.position_near_selection(*region)
        self._overlay.show()

    def _close_active_overlay(self) -> None:
        """Close and clear the active translation overlay, if present."""
        if self._overlay is not None:
            self._overlay.close()
            self._overlay = None

    def _close_active_canvas(self) -> None:
        """Close and clear the active selection canvas, if present."""
        if self._canvas is not None:
            self._canvas.close()
            self._canvas = None
