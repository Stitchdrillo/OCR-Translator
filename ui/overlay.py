"""Frameless floating overlay card for displaying translated text."""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

OVERLAY_MIN_WIDTH = 300
OVERLAY_MAX_WIDTH = 600
SCREEN_EDGE_MARGIN = 10
SELECTION_GAP = 10

OVERLAY_STYLESHEET = """
    QLabel {
        background-color: rgba(30, 30, 30, 220);
        color: white;
        font-size: 16px;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 100);
    }
"""


class TranslationOverlay(QWidget):
    """Displays translated text near the captured region; closes on left-click."""

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setMinimumWidth(OVERLAY_MIN_WIDTH)
        self.label.setMaximumWidth(OVERLAY_MAX_WIDTH)
        self.label.setStyleSheet(OVERLAY_STYLESHEET)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.adjustSize()

    def position_near_selection(
        self,
        physical_x: int,
        physical_y: int,
        physical_width: int,
        physical_height: int,
    ) -> None:
        """Position the card below (or above) the captured region within screen bounds."""
        dpr = self.devicePixelRatioF()
        sel_x = int(physical_x / dpr)
        sel_y = int(physical_y / dpr)
        sel_w = int(physical_width / dpr)
        sel_h = int(physical_height / dpr)

        if self.layout() is not None:
            self.layout().activate()
        self.adjustSize()

        card_w = self.sizeHint().width()
        card_h = self.sizeHint().height()

        screen = QApplication.screenAt(QPoint(sel_x, sel_y)) or QApplication.primaryScreen()
        bounds = screen.availableGeometry()

        # Center horizontally under the selection by default.
        target_x = sel_x + (sel_w // 2) - (card_w // 2)
        target_y = sel_y + sel_h + SELECTION_GAP

        # Clamp horizontally inside the screen's usable area.
        target_x = max(
            bounds.left() + SCREEN_EDGE_MARGIN,
            min(target_x, bounds.right() - card_w - SCREEN_EDGE_MARGIN),
        )

        # Flip above the selection if placing below would overflow the bottom edge.
        if target_y + card_h > bounds.bottom():
            target_y = sel_y - card_h - SELECTION_GAP

        if target_y < bounds.top():
            target_y = bounds.bottom() - card_h - SCREEN_EDGE_MARGIN

        self.move(target_x, target_y)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Dismiss the overlay when left-clicked."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()
