"""System tray icon and context menu for background control."""

from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):
    """System tray indicator providing access to Settings and Quit actions."""

    def __init__(self, app: QApplication, icon_path: Path | None = None) -> None:
        super().__init__(app)

        if icon_path and icon_path.exists():
            icon = QIcon(str(icon_path))
        else:
            icon = app.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)

        self.setIcon(icon)
        self.setToolTip("Screen Translator")

        self.menu = QMenu()
        self.settings_action = self.menu.addAction("Settings")
        self.menu.addSeparator()
        self.quit_action = self.menu.addAction("Quit")
        self.quit_action.triggered.connect(QApplication.quit)

        self.setContextMenu(self.menu)
