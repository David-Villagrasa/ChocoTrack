import mss
import pytesseract
import cv2
import numpy as np
import keyboard
import threading

# Set the Tesseract installation path (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define which monitor to capture (1 = primary, 2 = secondary, etc.)
MONITOR_ID = 1

# Variable de control para detener la captura
capture_running = True

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    
    # Apply binary thresholding
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Apply median blur to remove noise
    blurred = cv2.medianBlur(binary, 3)
    
    return blurred

def capture_and_analyze():
    global capture_running
    with mss.mss() as sct:
        monitor = sct.monitors[MONITOR_ID]  # Select the monitor
        screen_width = monitor["width"]
        screen_height = monitor["height"]

        # Define the region for the right half of the screen
        region = {
            "top": int(screen_height*0.15),
            "left": int(screen_width*0.7),  # Start from the middle of the screen
            "width": int(screen_width*0.125),  # Capture the right half
            "height": int(screen_height*0.3)
        }

        while capture_running:
            # Continuously capture the right half of the screen
            screenshot = sct.grab(region)

            # Convert the screenshot to a NumPy array
            img = np.array(screenshot)
            
            # Preprocess the image
            preprocessed_img = preprocess_image(img)
            
            # Perform OCR on the preprocessed image
            extracted_text = pytesseract.image_to_string(preprocessed_img, lang="eng", config='--psm 6')

            # Show the extracted text
            print("\n📜 Extracted Text:")
            print(extracted_text)

            # Optional: Add a small delay to avoid excessive CPU usage
            cv2.waitKey(4)

def stop_capture():
    global capture_running
    print("🛑 Stopping capture...")
    capture_running = False

# Set up a keyboard shortcut to start real-time capture and analysis
keyboard.add_hotkey("ctrl+alt+t", lambda: threading.Thread(target=capture_and_analyze).start())
# Set up a keyboard shortcut to stop the capture (press "Esc")
keyboard.add_hotkey("esc", stop_capture)

print("🔴 Press Ctrl+Alt+T to start real-time capture and analysis.")
print("🛑 Press Esc to stop capture.")

keyboard.wait("esc")  # Keeps the script running indefinitely
