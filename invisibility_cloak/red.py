
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)  # 0 = default webcam

# Give the camera time to warm up
time.sleep(3)

# Capture the background (you should move away during this time)
print("Capturing background... Please step out of the frame.")
for i in range(60):
    ret, background = cap.read()

background = np.flip(background, axis=1)  # flip background

print("Background captured. Move into the frame with your red cloak!")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame
    frame = np.flip(frame, axis=1)

    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV (two ranges because red wraps around HSV)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Clean the mask (remove noise)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8))

    # Invert mask (everything that is not red)
    mask_inv = cv2.bitwise_not(mask)

    # Segment out non-red parts from the frame
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Segment out red parts from the background
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combine the two to create the effect
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Invisibility Cloak", final_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
