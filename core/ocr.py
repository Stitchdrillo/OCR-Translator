"""Optical Character Recognition (OCR) wrapper around Tesseract."""

import logging

from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)

TESSERACT_LANGUAGE_NAMES: dict[str, str] = {
    "eng": "English",
    "por": "Portuguese",
    "chi_sim": "Simplified Chinese",
    "chi_tra": "Traditional Chinese",
    "kor": "Korean",
    "ara": "Arabic",
    "rus": "Russian",
    "hin": "Hindi",
    "jpn": "Japanese",
    "jpn_vert": "Japanese (Vertical)",
    "ita": "Italian",
    "fra": "French",
    "spa": "Spanish",
    "deu": "German",
    "osd": "OSD (Ignore)",
}


def get_installed_languages(tesseract_path: str) -> list[tuple[str, str]]:
    """Return `(code, display_label)` pairs for languages installed in Tesseract."""
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    try:
        codes = pytesseract.get_languages()
    except Exception as exc:
        logger.warning("Could not query Tesseract languages (%s); defaulting to English.", exc)
        codes = ["eng"]

    return [
        (code, f"{TESSERACT_LANGUAGE_NAMES.get(code, code)} ({code})")
        for code in codes
    ]


def extract_text(image: Image.Image, tesseract_path: str, lang: str) -> str:
    """Extract and strip text from an image using the configured Tesseract binary."""
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as exc:
        logger.error("OCR extraction failed: %s", exc)
        return ""
