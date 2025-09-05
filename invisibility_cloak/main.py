import cv2
import numpy as np
import json

# Default cloak color
selected_color = "red"

# Define HSV ranges
color_ranges = {
    "red": [
        (np.array([0, 120, 70]), np.array([10, 255, 255])),
        (np.array([170, 120, 70]), np.array([180, 255, 255]))
    ],
    "blue": [(np.array([94, 80, 2]), np.array([126, 255, 255]))],
    "green": [(np.array([40, 40, 40]), np.array([70, 255, 255]))]
}

def set_cloak_color(color: str):
    global selected_color
    if color in color_ranges:
        selected_color = color
        print(f"[INFO] Cloak color set to {color}")
    else:
        print(f"[WARNING] Unsupported color: {color}")

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot access webcam")
        return

    # Capture background
    for i in range(60):
        ret, background = cap.read()
    background = np.flip(background, axis=1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Use latest selected color
        try:
            with open("color.json") as f:
                color = json.load(f).get("color", "red")
        except FileNotFoundError:
            color = selected_color

        # Create mask
        mask = None
        for lower, upper in color_ranges[color]:
            new_mask = cv2.inRange(hsv, lower, upper)
            mask = new_mask if mask is None else mask | new_mask

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
        mask_inv = cv2.bitwise_not(mask)

        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Encode as JPEG for Flask
        ret, buffer = cv2.imencode('.jpg', final_output)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
