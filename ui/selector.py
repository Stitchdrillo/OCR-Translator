"""Fullscreen transparent overlay for click-and-drag screen region selection."""

from PyQt6.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QKeyEvent, QMouseEvent, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QWidget

BACKDROP_COLOR = QColor(0, 0, 0, 100)
SELECTION_BORDER_COLOR = QColor(255, 255, 255)
SELECTION_BORDER_WIDTH = 2


class SelectionCanvas(QWidget):
    """Dims the screen and lets the user drag a clear cutout rectangle to capture."""

    area_selected = pyqtSignal(int, int, int, int)  # Physical (x, y, width, height)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.setGeometry(self.screen().geometry())

        self._origin = QPoint()
        self._current = QPoint()
        self._is_selecting = False

    def paintEvent(self, event: QPaintEvent) -> None:
        """Render the dimmed backdrop and transparent selection cutout."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), BACKDROP_COLOR)

        if not self._is_selecting:
            return

        selection = QRect(self._origin, self._current).normalized()

        # Punch a clear hole through the translucent backdrop so the selected area is crisp.
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.fillRect(selection, Qt.GlobalColor.transparent)

        # Restore normal compositing to draw the selection border.
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        pen = QPen(SELECTION_BORDER_COLOR, SELECTION_BORDER_WIDTH, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawRect(selection)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Start dragging on left-click, or cancel immediately on right-click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._origin = event.pos()
            self._current = self._origin
            self._is_selecting = True
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Update the active selection rectangle while dragging."""
        if self._is_selecting:
            self._current = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Finalize selection, convert to physical pixels, emit bounds, and close."""
        if event.button() != Qt.MouseButton.LeftButton or not self._is_selecting:
            return

        self._is_selecting = False
        selection = QRect(self._origin, self._current).normalized()

        # Hide before emitting so the screenshot is guaranteed to be untinted.
        self.hide()

        dpr = self.devicePixelRatioF()
        x = int(selection.x() * dpr)
        y = int(selection.y() * dpr)
        width = int(selection.width() * dpr)
        height = int(selection.height() * dpr)

        if width > 0 and height > 0:
            self.area_selected.emit(x, y, width, height)

        self.close()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Allow Escape to dismiss the selection overlay and return control underneath."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
