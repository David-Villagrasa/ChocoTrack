import mss
import keyboard
import pytesseract
import cv2
import numpy as np  # Necessary for image processing

# Set the Tesseract installation path (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define which monitor to capture (1 = primary, 2 = secondary, etc.)
MONITOR_ID = 2

def capture_text():
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_ID]  # Select the monitor
        screenshot = sct.grab(monitor)  # Capture the screen

        # Convert the screenshot to a NumPy array
        img = np.array(screenshot)  # Convert to NumPy array
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)  # Convert to grayscale

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(img, lang="eng")  # Change "eng" to another language if needed

        # Display the extracted text
        print("\n📜 Extracted Text:")
        print(extracted_text)

# Set up a keyboard shortcut to capture and analyze text
keyboard.add_hotkey("ctrl+alt+t", capture_text)

print("🔴 Press Ctrl+Alt+T to capture and analyze text.")
print("🔴 Press Esc to exit.")
keyboard.wait("esc")  # Keeps the script running until "Esc" is pressed
