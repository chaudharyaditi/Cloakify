import cv2
import numpy as np
import json
import base64

selected_color = "red"

# HSV ranges for colors
color_ranges = {
    "red": [(np.array([0,120,70]), np.array([10,255,255])),
            (np.array([170,120,70]), np.array([180,255,255]))],
    "blue": [(np.array([94,80,2]), np.array([126,255,255]))],
    "green": [(np.array([40,40,40]), np.array([70,255,255]))]
}

def set_cloak_color(color):
    global selected_color
    if color in color_ranges:
        selected_color = color
        print(f"[INFO] Cloak color set to {color}")

def process_frame(frame):
    """Apply invisibility cloak effect on a single frame (BGR)."""
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask for selected color
    mask = None
    for lower, upper in color_ranges[selected_color]:
        new_mask = cv2.inRange(hsv, lower, upper)
        mask = new_mask if mask is None else mask | new_mask

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8))
    mask_inv = cv2.bitwise_not(mask)

    background = np.zeros_like(frame)  # black background for simplicity
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    return final_output

def frame_to_base64(frame):
    """Encode frame as JPEG base64 string."""
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')
