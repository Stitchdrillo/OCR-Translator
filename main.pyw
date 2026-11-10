import sys
from PyQt6.QtWidgets import QApplication
from ui.selector import SelectionCanvas
from ui.overlay import TranslationOverlay
from ui.settings import SettingsWindow
from ui.tray import TrayIcon
from core.capture import capture_region
from core.ocr import extract_text
from core.translator import translate_text
from core.hotkey import HotkeyListener
from config import load_config

# Momento python (garbage collector)
current_canvas = None
current_overlay = None
settings_window = None
listener = None

def show_canvas():
    global current_canvas, current_overlay
    
    # Se c'è già qualcosa lo chiude, molto comodo
    if current_overlay:
        current_overlay.close()
        current_overlay = None

    current_canvas = SelectionCanvas()
    current_canvas.on_area_selected.connect(handle_selection)
    current_canvas.show()

def reload_app_settings():
    global listener
    cfg = load_config()
    # In realtà tutto legge le impostazioni in real time tranne il listener per la hot key
    if listener:
        listener.update_hotkey(cfg["HOTKEY"])
    
def show_settings():
    global settings_window
    # Questa serve, me ne ero dimenticato ed è un casino
    if settings_window:
        settings_window.close()
    settings_window = SettingsWindow()
    settings_window.settings_saved.connect(reload_app_settings)
    
    settings_window.show()
    settings_window.activateWindow()

def handle_selection(x, y, width, height):
    global current_overlay
    
    # Se si cliccava senza trascinare crashava... già
    if width > 0 and height > 0:
        print("Capturing image...")
        image = capture_region(x, y, width, height)
        
        print("Extracting text...")
        text = extract_text(image)
        
        if text:
            print(f"Original: {text}")
            print("Translating...")
            
            # Ho scoperto che è molto bello programmare separando la roba
            # invece che avere un gigantesco file unico
            translated = translate_text(text) 
            current_overlay = TranslationOverlay(translated)
            
            # Il metodo preferito di tutti, ero fuso e non l'ho chiamato smart_positioning
            # ma non ho assolutamente voglia di cambiarlo
            current_overlay.position_intelligently(x, y, width, height)
            
            current_overlay.show()
        else:
            print("No text found in that area.") # Prima o poi dovrei fare ordine nella shell

def main():
    global listener
    
    app = QApplication(sys.argv)
    
    # Senza questo l'app si chiudeva misteriosamente dopo la selezione
    app.setQuitOnLastWindowClosed(False)
    
    cfg = load_config()
    
    # Questo fa l'icona nella roba in basso a destra
    tray = TrayIcon(app)
    
    tray.settings_action.triggered.connect(show_settings)
    tray.show()
    
    # Questo sta in background e aspetta l'hotkey
    listener = HotkeyListener(cfg["HOTKEY"])

    listener.trigger_signal.connect(show_canvas)
    
    print(f"App is running in the background.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
