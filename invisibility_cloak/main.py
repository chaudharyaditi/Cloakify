import cv2
import numpy as np
import json

# Default cloak color
selected_color = "red"

# Define HSV ranges for colors
color_ranges = {
    "red": [
        (np.array([0, 120, 70]), np.array([10, 255, 255])),
        (np.array([170, 120, 70]), np.array([180, 255, 255]))
    ],
    "blue": [
        (np.array([94, 80, 2]), np.array([126, 255, 255]))
    ],
    "green": [
        (np.array([40, 40, 40]), np.array([70, 255, 255]))
    ]
}

def get_selected_color():
    """Read the currently selected cloak color from color.json."""
    try:
        with open("color.json") as f:
            color = json.load(f).get("color", "red")
            print("[INFO] Current color:", color)
    except FileNotFoundError:
        color = "red"
    return color

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera")
        return

    # Capture background for initial frames
    print("[INFO] Capturing background, please step out of the frame...")
    for i in range(60):
        ret, background = cap.read()
    background = np.flip(background, axis=1)  # Flip horizontally

    print("[INFO] Starting cloak detection. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Update cloak color from Flask selection
        selected_color = get_selected_color()

        # Create mask for selected color
        mask = None
        for lower, upper in color_ranges[selected_color]:
            new_mask = cv2.inRange(hsv, lower, upper)
            mask = new_mask if mask is None else mask | new_mask

        # Refine mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))

        # Invert mask
        mask_inv = cv2.bitwise_not(mask)

        # Segment out cloak and background
        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        # Show the output
        cv2.imshow("Invisibility Cloak", final_output)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
