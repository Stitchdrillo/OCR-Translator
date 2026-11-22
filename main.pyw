"""Application entry point for the Screen Translator desktop utility."""

import logging
import sys

from PyQt6.QtWidgets import QApplication

from app import ScreenTranslatorApp


def configure_logging() -> None:
    """Configure application-wide console logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    """Initialize the Qt application and start the background controller."""
    configure_logging()

    qt_app = QApplication(sys.argv)
    qt_app.setQuitOnLastWindowClosed(False)

    controller = ScreenTranslatorApp(qt_app)
    qt_app.aboutToQuit.connect(controller.shutdown)
    controller.start()

    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()
