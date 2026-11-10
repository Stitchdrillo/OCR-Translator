from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle
class TrayIcon(QSystemTrayIcon):
    def __init__(self, app_context):
        super().__init__()
        icon = app_context.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)
        self.setIcon(icon)
        self.setToolTip("Screen Translator")
        self.menu = QMenu()
        self.settings_action = self.menu.addAction("Settings")
        self.menu.addSeparator()                                  
        self.quit_action = self.menu.addAction("Quit")
        self.quit_action.triggered.connect(QApplication.quit)
        self.setContextMenu(self.menu)
