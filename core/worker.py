"""Background worker task for running OCR and translation off the UI thread."""

import logging

from PIL import Image
from PyQt6.QtCore import QObject, QRunnable, pyqtSignal

from core.config import AppConfig
from core.ocr import extract_text
from core.translator import translate_text

logger = logging.getLogger(__name__)


class WorkerSignals(QObject):
    """Qt signals emitted by `TranslationWorker` upon completion."""

    finished = pyqtSignal(int, str, tuple)  # (request_id, translated_text, region)
    no_text = pyqtSignal(int)  # (request_id,)


class TranslationWorker(QRunnable):
    """Executes OCR and translation in a thread pool to keep the UI responsive."""

    def __init__(
        self,
        request_id: int,
        image: Image.Image,
        region: tuple[int, int, int, int],
        config: AppConfig,
    ) -> None:
        super().__init__()
        self.request_id = request_id
        self.image = image
        self.region = region
        self.config = config
        self.signals = WorkerSignals()

    def run(self) -> None:
        """Extract text from the captured image and translate it."""
        logger.info("Extracting text (request #%d)...", self.request_id)
        extracted = extract_text(
            image=self.image,
            tesseract_path=self.config.tesseract_path,
            lang=self.config.ocr_lang,
        )

        if not extracted:
            logger.info("No text detected in selected region (request #%d).", self.request_id)
            self.signals.no_text.emit(self.request_id)
            return

        logger.info("Translating extracted text: %r", extracted)
        translated = translate_text(
            text=extracted,
            source_lang=self.config.trans_source,
            target_lang=self.config.trans_target,
        )
        self.signals.finished.emit(self.request_id, translated, self.region)
