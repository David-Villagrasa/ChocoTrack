from window import create_gui
from screen_capture_ocr import setup_hotkeys

# Create GUI
root = create_gui()

# Configure keyboard shortcuts
setup_hotkeys()

# Run the interface
root.mainloop()
