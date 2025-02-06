import mss
import pytesseract
import cv2
import numpy as np
import re
import threading
import keyboard
from window import update_chocobo_entry  # Correctly import the update function

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Global variables
MONITOR_ID = 1
chocobo_counter = 0  # Keeps track of captured chocobos

def preprocess_image(image):
    """Convert image to grayscale and apply filter."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    blurred = cv2.medianBlur(binary, 3)
    return blurred

def format_extracted_text(text):
    """Format the extracted text from the image."""
    lines = text.strip().split("\n")
    numbers = [re.sub(r"\D", "", line) for line in lines if any(c.isdigit() for c in line)]
    name = next((line for line in lines if not any(c.isdigit() for c in line)), "UNKNOWN")

    top_speed = numbers[0] if len(numbers) > 0 else "N/A"
    stamina = numbers[1] if len(numbers) > 1 else "N/A"

    return f"TOP SPEED: {top_speed}\nSTAMINA: {stamina}\nNAME: {name}"

def capture_and_analyze():
    """Capture an image, process it, and extract data."""
    global chocobo_counter
    if chocobo_counter >= 6:
        return  # Do not capture more than 6 chocobos

    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_ID]
        screen_width, screen_height = monitor["width"], monitor["height"]

        # Define the capture region
        region = {
            "top": int(screen_height * 0.15),
            "left": int(screen_width * 0.7),
            "width": int(screen_width * 0.125),
            "height": int(screen_height * 0.3)
        }

        # Capture image
        screenshot = sct.grab(region)

        # Convert image and preprocess it
        img = np.array(screenshot)
        preprocessed_img = preprocess_image(img)

        # Extract text
        extracted_text = pytesseract.image_to_string(preprocessed_img, lang="eng", config='--psm 6')

        # Format and update GUI
        formatted_text = format_extracted_text(extracted_text)
        update_chocobo_entry(chocobo_counter, formatted_text)
        chocobo_counter += 1  # Move to the next chocobo

def setup_hotkeys():
    """Configure keyboard shortcuts."""
    keyboard.add_hotkey("ctrl+alt+t", lambda: threading.Thread(target=capture_and_analyze).start())
