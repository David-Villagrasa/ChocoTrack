import mss
import pytesseract
import cv2
import numpy as np
import keyboard
import threading
import re 

# Set the Tesseract installation path (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define which monitor to capture (1 = primary, 2 = secondary, etc.)
MONITOR_ID = 1

def preprocess_image(image):
    """Convert image to grayscale, apply thresholding and median blur."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    blurred = cv2.medianBlur(binary, 3)
    return blurred

def format_extracted_text(text):
    """Format extracted text into structured output."""
    lines = text.strip().split("\n")
    numbers = [re.sub(r"\D", "", line) for line in lines if any(c.isdigit() for c in line)]  # Just numbers
    name = next((line for line in lines if not any(c.isdigit() for c in line)), "UNKNOWN")

    top_speed = numbers[0] if len(numbers) > 0 else "N/A"
    stamina = numbers[1] if len(numbers) > 1 else "N/A"

    formatted_text = f"\n🏁 TOP SPEED: {top_speed}\n💪 STAMINA: {stamina}\n🏇 NAME: {name}"
    return formatted_text

def capture_and_analyze():
    """Capture a screenshot of a specific region and extract text using OCR."""
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_ID]
        screen_width, screen_height = monitor["width"], monitor["height"]

        # Define the region to capture (adjust as needed)
        region = {
            "top": int(screen_height * 0.15),
            "left": int(screen_width * 0.7),
            "width": int(screen_width * 0.125),
            "height": int(screen_height * 0.3)
        }

        # Take a single screenshot
        screenshot = sct.grab(region)

        # Convert to NumPy array and preprocess
        img = np.array(screenshot)
        preprocessed_img = preprocess_image(img)

        # Perform OCR
        extracted_text = pytesseract.image_to_string(preprocessed_img, lang="eng", config='--psm 6')

        # Format and print the extracted text
        print(format_extracted_text(extracted_text))

# Assign the capture function to a hotkey (Ctrl+Alt+T)
keyboard.add_hotkey("ctrl+alt+t", lambda: threading.Thread(target=capture_and_analyze).start())

print("🔴 Press Ctrl+Alt+T to capture and analyze.")
keyboard.wait("esc")  # Keep the script running
