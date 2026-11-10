from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QKeySequenceEdit
)
from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import pyqtSignal
import pytesseract
from deep_translator import MyMemoryTranslator
from config import load_config, save_config
TESSERACT_NAMES = {
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
    "osd": "OSD (Ignore)"
}
class SettingsWindow(QWidget):
    settings_saved = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translator Settings")
        self.resize(600, 0)
        cfg = load_config()
        layout = QFormLayout()
        self.tesseract_input = QLineEdit(cfg["TESSERACT_PATH"])
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_tesseract)
        tesseract_layout = QHBoxLayout()
        tesseract_layout.addWidget(self.tesseract_input)
        tesseract_layout.addWidget(browse_btn)
        self.ocr_combo = QComboBox()
        self.refresh_ocr_languages()                             
        try:
            translator = MyMemoryTranslator(source = "en-GB", target = "it-IT")
            translation_langs = translator.get_supported_languages(as_dict=True)
            translation_langs = {name.capitalize(): code for name, code in translation_langs.items()}
        except Exception as e:
            print(f"Could not fetch languages: {e}")
            translation_langs = {"English": "en-GB", "Italian": "it-IT"}
        self.source_combo = QComboBox()
        for name, code in translation_langs.items():
            self.source_combo.addItem(name, code)
        src_idx = self.source_combo.findData(cfg["TRANS_SOURCE"])
        if src_idx >= 0: self.source_combo.setCurrentIndex(src_idx)
        self.target_combo = QComboBox()
        for name, code in translation_langs.items():
            if code != "auto":                                 
                self.target_combo.addItem(name, code)
        tgt_idx = self.target_combo.findData(cfg["TRANS_TARGET"])
        if tgt_idx >= 0: self.target_combo.setCurrentIndex(tgt_idx)
        current_sequence = QKeySequence(cfg["HOTKEY"])
        self.hotkey_input = QKeySequenceEdit(current_sequence)
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addRow("Tesseract Path:", tesseract_layout)
        layout.addRow("OCR Language:", self.ocr_combo)
        layout.addRow("Original Text is:", self.source_combo)
        layout.addRow("Translate into:", self.target_combo)
        layout.addRow("Shortcut Recorder:", self.hotkey_input)
        layout.addRow(save_btn)
        self.setLayout(layout)
    def browse_tesseract(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Tesseract Executable",
            self.tesseract_input.text(),
            "Executables (*.exe);;All Files (*)"
        )
        if file_path:
            self.tesseract_input.setText(file_path)
            self.refresh_ocr_languages()
    def refresh_ocr_languages(self):
        path = self.tesseract_input.text()
        pytesseract.pytesseract.tesseract_cmd = path
        current_selection = self.ocr_combo.currentData() or load_config()["OCR_LANG"]
        self.ocr_combo.clear()
        try:
            installed_langs = pytesseract.get_languages()
        except Exception:
            installed_langs = ['eng']
        for code in installed_langs:
            pretty_name = TESSERACT_NAMES.get(code, code)
            self.ocr_combo.addItem(f"{pretty_name} ({code})", code)
        ocr_idx = self.ocr_combo.findData(current_selection)
        if ocr_idx >= 0:
            self.ocr_combo.setCurrentIndex(ocr_idx)
    def save_settings(self):
        raw_sequence = self.hotkey_input.keySequence().toString()
        formatted_hotkey = raw_sequence.lower().replace('meta', 'windows')
        if not formatted_hotkey:
            formatted_hotkey = "ctrl+shift+q"
        cfg = {
            "HOTKEY": formatted_hotkey,
            "TESSERACT_PATH": self.tesseract_input.text(),
            "OCR_LANG": self.ocr_combo.currentData() or "eng",
            "TRANS_SOURCE": self.source_combo.currentData() or "en-GB",
            "TRANS_TARGET": self.target_combo.currentData() or "it-IT",
        }
        save_config(cfg)
        self.settings_saved.emit()
        QMessageBox.information(self, "Saved", "Settings applied successfully!")
        self.close()
