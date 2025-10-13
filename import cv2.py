import cv2
import numpy as np
import pyautogui
import time

# --- Configuration ---
SWIPE_THRESHOLD = 20  # Horizontal distance to trigger a swipe
COOLDOWN_SECONDS = 1.5 # Time to wait after a swipe is detected

# --- Initialization ---
cap = cv2.VideoCapture(0)

# --- State Variables for Gesture Logic ---
initial_x = None
last_swipe_time = 0

print("🚀 Starting Gesture Control (OpenCV method).")
print("Place your hand in the green box and make a clear gesture.")
print("Press 'q' to quit.")

# --- Main Loop ---
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    # --- Region of Interest (ROI) ---
    # We will only process a specific part of the screen for hand detection
    roi = frame[100:350, 400:650]
    cv2.rectangle(frame, (400, 100), (650, 350), (0, 255, 0), 2)

    # --- Hand Detection using Contours ---
    # Convert ROI to HSV color space (better for color detection)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Define a range for skin color in HSV
    # This might need adjustment for your skin tone and lighting
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a mask to isolate skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply some image processing to clean up the mask
    mask = cv2.GaussianBlur(mask, (5, 5), 100)
    
    # Find the contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    current_time = time.time()

    # --- Gesture Logic ---
    if len(contours) > 0 and (current_time - last_swipe_time > COOLDOWN_SECONDS):
        # Find the largest contour, which we assume is the hand
        hand_contour = max(contours, key=cv2.contourArea)
        
        # Check if the contour is reasonably large (to avoid noise)
        if cv2.contourArea(hand_contour) > 5000:
            # Calculate the center of the contour
            M = cv2.moments(hand_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Draw the contour and its center
                cv2.drawContours(roi, [hand_contour], -1, (0, 255, 0), 3)
                cv2.circle(roi, (cx, cy), 7, (0, 0, 255), -1)

                if initial_x is None:
                    initial_x = cx
                
                delta_x = cx - initial_x

                # Check for Right Swipe
                if delta_x > SWIPE_THRESHOLD:
                    print("➡️  Right Swipe Detected! Switching to next tab.")
                    pyautogui.hotkey('ctrl', 'tab')
                    initial_x = None 
                    last_swipe_time = current_time

                # Check for Left Swipe
                elif delta_x < -SWIPE_THRESHOLD:
                    print("⬅️  Left Swipe Detected! Switching to previous tab.")
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    initial_x = None
                    last_swipe_time = current_time
    else:
        # Reset if no hand is detected
        initial_x = None

    cv2.imshow("Hand Gesture Control - OpenCV Method", frame)
    # cv2.imshow("Mask", mask) # Uncomment to see the skin detection mask

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()