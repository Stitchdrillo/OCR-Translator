"""Settings dialog for configuring Tesseract, languages, and the global shortcut."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QKeySequenceEdit,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)

from core.config import AppConfig, load_config, save_config
from core.ocr import get_installed_languages
from core.translator import get_supported_languages


class SettingsWindow(QWidget):
    """Form-based configuration window that persists changes to `config.json`."""

    settings_saved = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Translator Settings")
        self.resize(600, 0)

        self._config = load_config()
        self._setup_ui()
        self._populate_translation_languages()
        self._refresh_ocr_languages(initial_code=self._config.ocr_lang)

    def _setup_ui(self) -> None:
        """Create and arrange all form controls."""
        layout = QFormLayout(self)

        # Tesseract executable path + file browser
        self.tesseract_input = QLineEdit(self._config.tesseract_path)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_tesseract)

        tesseract_row = QHBoxLayout()
        tesseract_row.addWidget(self.tesseract_input)
        tesseract_row.addWidget(browse_btn)

        # Language selectors
        self.ocr_combo = QComboBox()
        self.source_combo = QComboBox()
        self.target_combo = QComboBox()

        # Shortcut recorder
        self.hotkey_input = QKeySequenceEdit(QKeySequence(self._config.hotkey))

        # Save action
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_settings)

        layout.addRow("Tesseract Path:", tesseract_row)
        layout.addRow("OCR Language:", self.ocr_combo)
        layout.addRow("Original Text is:", self.source_combo)
        layout.addRow("Translate into:", self.target_combo)
        layout.addRow("Shortcut Recorder:", self.hotkey_input)
        layout.addRow(save_btn)

    def _populate_translation_languages(self) -> None:
        """Load supported source and target languages into the translation dropdowns."""
        languages = get_supported_languages()

        for name, code in languages.items():
            self.source_combo.addItem(name, code)
            if code != "auto":  # Target language cannot be auto-detected.
                self.target_combo.addItem(name, code)

        self._select_combo_by_data(self.source_combo, self._config.trans_source)
        self._select_combo_by_data(self.target_combo, self._config.trans_target)

    def _refresh_ocr_languages(self, initial_code: str | None = None) -> None:
        """Query the configured Tesseract binary and repopulate available OCR languages."""
        selected_code = initial_code or self.ocr_combo.currentData() or self._config.ocr_lang
        self.ocr_combo.clear()

        for code, label in get_installed_languages(self.tesseract_input.text()):
            self.ocr_combo.addItem(label, code)

        self._select_combo_by_data(self.ocr_combo, selected_code)

    def _browse_tesseract(self) -> None:
        """Open a file picker for selecting the Tesseract executable."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Tesseract Executable",
            self.tesseract_input.text(),
            "Executables (*.exe);;All Files (*)",
        )
        if file_path:
            self.tesseract_input.setText(file_path)
            self._refresh_ocr_languages()

    def _save_settings(self) -> None:
        """Validate form values, save them to disk, and notify the controller."""
        defaults = AppConfig()
        raw_sequence = self.hotkey_input.keySequence().toString()
        normalized_hotkey = raw_sequence.lower().replace("meta", "windows") or defaults.hotkey

        updated_config = AppConfig(
            hotkey=normalized_hotkey,
            tesseract_path=self.tesseract_input.text().strip() or defaults.tesseract_path,
            ocr_lang=self.ocr_combo.currentData() or defaults.ocr_lang,
            trans_source=self.source_combo.currentData() or defaults.trans_source,
            trans_target=self.target_combo.currentData() or defaults.trans_target,
        )

        save_config(updated_config)
        self.settings_saved.emit()

        QMessageBox.information(self, "Saved", "Settings applied successfully!")
        self.close()

    @staticmethod
    def _select_combo_by_data(combo: QComboBox, value: str) -> None:
        """Select the dropdown item matching `value`, if present."""
        index = combo.findData(value)
        if index >= 0:
            combo.setCurrentIndex(index)
