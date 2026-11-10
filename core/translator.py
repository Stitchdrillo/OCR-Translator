from deep_translator import MyMemoryTranslator
from config import load_config
def translate_text(text):
    if not text.strip():
        return ""
    cfg = load_config()
    try:
        translator = MyMemoryTranslator(
            source = cfg["TRANS_SOURCE"],
            target = cfg["TRANS_TARGET"]
        )
        translated = translator.translate(text)
        return translated
    except Exception as e:
        print(f"Translation Error: {e}")
        return f"Error: {e}"
