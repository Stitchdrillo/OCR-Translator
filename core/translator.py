"""Machine translation wrapper and supported language discovery."""

import logging

from deep_translator import MyMemoryTranslator

logger = logging.getLogger(__name__)

FALLBACK_LANGUAGES: dict[str, str] = {
    "English": "en-GB",
    "Italian": "it-IT",
}


def get_supported_languages() -> dict[str, str]:
    """Fetch `{Display Name: language_code}` pairs supported by MyMemory."""
    try:
        translator = MyMemoryTranslator(source="en-GB", target="it-IT")
        raw_languages = translator.get_supported_languages(as_dict=True)
        return {name.capitalize(): code for name, code in raw_languages.items()}
    except Exception as exc:
        logger.warning("Could not fetch translation languages (%s); using fallback list.", exc)
        return FALLBACK_LANGUAGES.copy()


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text between two language codes, returning an error string on failure."""
    if not text.strip():
        return ""

    try:
        translator = MyMemoryTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as exc:
        logger.error("Translation failed: %s", exc)
        return f"Error: {exc}"
