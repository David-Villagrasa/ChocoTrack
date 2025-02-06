import mss
import pytesseract
import cv2
import numpy as np
import re
from window import update_chocobo_entry  

# Tesseract Config
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

MONITOR_ID = 1
chocobo_counter = 0  

def reset_chocobo_counter():
    """Reset the chocobo counter to start from Chocobo 1."""
    global chocobo_counter
    chocobo_counter = 0

def preprocess_image(image):
    """Convert image to grayscale and apply a threshold filter."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return cv2.medianBlur(binary, 3)

def extract_text_from_image(image):
    """Use OCR to extract text from the processed image."""
    return pytesseract.image_to_string(image, lang="eng", config='--psm 6')

def format_extracted_text(text):
    """Format the extracted OCR text into structured chocobo data."""
    lines = text.strip().split("\n")
    numbers = [re.sub(r"\D", "", line) for line in lines if any(c.isdigit() for c in line)]
    name = next((line for line in lines if not any(c.isdigit() for c in line)), "UNKNOWN")

    top_speed = numbers[0] if len(numbers) > 0 else "N/A"
    stamina = numbers[1] if len(numbers) > 1 else "N/A"

    return f"TOP SPEED: {top_speed}\nSTAMINA: {stamina}\nNAME: {name}"

def capture_and_analyze():
    """Capture a screenshot, process it, and extract text data."""
    global chocobo_counter
    if chocobo_counter >= 6:
        return  

    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_ID]
        #TODO set the tracking area in other way
        region = {
            "top": int(monitor["height"] * 0.15),
            "left": int(monitor["width"] * 0.7),
            "width": int(monitor["width"] * 0.125),
            "height": int(monitor["height"] * 0.3)
        }
        screenshot = sct.grab(region)
        preprocessed_img = preprocess_image(np.array(screenshot))
        extracted_text = extract_text_from_image(preprocessed_img)
        formatted_text = format_extracted_text(extracted_text)
        update_chocobo_entry(chocobo_counter, formatted_text)
        chocobo_counter += 1  
