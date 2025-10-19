Gesture-Based Tab Switcher 👆
This Python script allows you to switch between browser or application tabs using simple hand swipe gestures captured by your webcam.

Requirements
OpenCV

NumPy

PyAutoGUI

Installation
Install the required packages using pip:

Bash

pip install opencv-python numpy pyautogui
Usage
Run the script from your terminal:

Bash

python "import cv2.py"
(Note: You may want to rename the file to something more descriptive, like app.py or tab_switcher.py)

A window will appear showing your webcam feed with a green box (the Region of Interest).

Place your hand inside the green box and make a clear horizontal swipe motion.

Swipe Right: Switches to the next tab (Ctrl + Tab).

Swipe Left: Switches to the previous tab (Ctrl + Shift + Tab).

Press 'q' to quit the application.
