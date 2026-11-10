import pytesseract
from config import load_config
def extract_text(image):
    cfg = load_config()
    pytesseract.pytesseract.tesseract_cmd = cfg["TESSERACT_PATH"]
    try:
        text = pytesseract.image_to_string(image, lang=cfg["OCR_LANG"])
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
