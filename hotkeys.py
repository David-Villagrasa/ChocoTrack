import keyboard
import threading
from screen_capture_ocr import capture_and_analyze, reset_chocobo_counter
from window import clear_data, calculate_and_display_winners

def on_capture_hotkey():
    """Run chocobo capture in a separate thread."""
    threading.Thread(target=capture_and_analyze).start()

def on_calculate_hotkey():
    """Trigger the calculation of winning bets."""
    calculate_and_display_winners()

def on_clear_hotkey():
    """Clear data and reset chocobo counter."""
    clear_data()
    reset_chocobo_counter()  # Reset the counter from hotkeys instead of window.py

def setup_hotkeys():
    """Configure global hotkeys for the application."""
    keyboard.add_hotkey("ctrl+alt+t", on_capture_hotkey)  # Capture chocobo data
    keyboard.add_hotkey("ctrl+alt+g", on_clear_hotkey)  # Clear data and reset counter
    keyboard.add_hotkey("ctrl+alt+c", on_calculate_hotkey)  # Simulate clicking "Calculate"
