from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QPoint
class TranslationOverlay(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setMinimumWidth(300)
        self.label.setMaximumWidth(600)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 30, 220); /* Dark grey, slightly transparent */
                color: white;
                font-size: 16px;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 100);
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.adjustSize()
    def position_intelligently(self, physical_x, physical_y, physical_width, physical_height):
        ratio = self.devicePixelRatioF()
        selection_x = int(physical_x / ratio)
        selection_y = int(physical_y / ratio)
        selection_width = int(physical_width / ratio)
        selection_height = int(physical_height / ratio)
        if self.layout():
            self.layout().activate()
        self.adjustSize() 
        my_width = self.sizeHint().width()
        my_height = self.sizeHint().height()
        screen = QApplication.screenAt(QPoint(int(selection_x), int(selection_y)))
        if not screen:
            screen = QApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        target_x = selection_x + (selection_width // 2) - (my_width // 2)
        target_y = selection_y + selection_height + 10
        if target_x + my_width > screen_geo.right():
            target_x = screen_geo.right() - my_width - 10
        if target_x < screen_geo.left():
            target_x = screen_geo.left() + 10
        if target_y + my_height > screen_geo.bottom():
            target_y = selection_y - my_height - 10
        if target_y < screen_geo.top():
            target_y = screen_geo.bottom() - my_height - 10
        self.move(target_x, target_y)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()
