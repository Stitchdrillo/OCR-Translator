import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
class HotkeyListener(QObject):
    trigger_signal = pyqtSignal()
    def __init__(self, shortcut):
        super().__init__()
        self.shortcut = shortcut
        self.hook = keyboard.add_hotkey(self.shortcut, self.on_hotkey)
    def on_hotkey(self):
        self.trigger_signal.emit()
    def update_hotkey(self, new_shortcut):
        try:
            keyboard.remove_hotkey(self.hook)
        except Exception:
            pass                                 
        self.shortcut = new_shortcut
        self.hook = keyboard.add_hotkey(self.shortcut, self.on_hotkey)
