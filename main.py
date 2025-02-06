from window import create_gui
from hotkeys import setup_hotkeys
'''
TODO extended
    - settings window to custom the hotkeys
    - settings to change the monitor and area of tesseract
    - info button with info of how is everything calculated & how are the diferent type of jockeys
    - deal with Readme.md (every calculator info extraxted from https://github.com/ff7man/ff7man.github.io/blob/main/calc.html & https://forums.qhimm.com/index.php?topic=21011.0)
'''
def main():
    root = create_gui()
    setup_hotkeys()
    root.mainloop()

if __name__ == "__main__":
    main()
