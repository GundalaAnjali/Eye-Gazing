import cv2
import math
import tkinter as tk
from cvzone.FaceMeshModule import FaceMeshDetector
from screeninfo import get_monitors

# 1. Setup Screen Dimensions
monitor = get_monitors()[0]
SCREEN_WIDTH = monitor.width
SCREEN_HEIGHT = monitor.height

# 2. Setup Webcam and Face Tracker
webcam = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

LEFT_PUPIL = 468
LEFT_EYE_LEFT_CORNER = 33
LEFT_EYE_RIGHT_CORNER = 133
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145

# Calibration Variables
h_min, h_max = 999.0, 0.0
v_min, v_max = 999.0, 0.0
calibrated = False

# --- SMOOTHING VARIABLES ---
# This holds the last known screen coordinates to prevent cursor jitter
smoothed_x = SCREEN_WIDTH // 2
smoothed_y = SCREEN_HEIGHT // 2
SMOOTH_FACTOR = 0.15  # Lower number = smoother/slower cursor, Higher number = faster/jumpier cursor

# 3. Setup Interactive Window
root = tk.Tk()
root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.65)  

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='black', highlightthickness=0)
canvas.pack()

def map_value(value, left_min, left_max, right_min, right_max):
    if left_max - left_min == 0: 
        return right_min
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return int(right_min + (value_scaled * right_span))

def update_gaze():
    global h_min, h_max, v_min, v_max, calibrated, smoothed_x, smoothed_y
    
    success, frame = webcam.read()
    if not success:
        root.after(10, update_gaze)
        return

    frame = cv2.flip(frame, 1)
    frame, faces = detector.findFaceMesh(frame, draw=False)
    canvas.delete("all")

    # Define 4 large target boxes spread out across the quadrants of your monitor
    BOX_W, BOX_H = 450, 180
    PAD_X, PAD_Y = 80, 80
    
    t1_x1, t1_y1, t1_x2, t1_y2 = PAD_X, PAD_Y, PAD_X + BOX_W, PAD_Y + BOX_H
    t2_x1, t2_y1, t2_x2, t2_y2 = SCREEN_WIDTH - PAD_X - BOX_W, PAD_Y, SCREEN_WIDTH - PAD_X, PAD_Y + BOX_H
    t3_x1, t3_y1, t3_x2, t3_y2 = PAD_X, SCREEN_HEIGHT - PAD_Y - BOX_H, PAD_X + BOX_W, SCREEN_HEIGHT - PAD_Y
    t4_x1, t4_y1, t4_x2, t4_y2 = SCREEN_WIDTH - PAD_X - BOX_W, SCREEN_HEIGHT - PAD_Y - BOX_H, SCREEN_WIDTH - PAD_X, SCREEN_HEIGHT - PAD_Y

    if faces:
        points = faces[0]
        pupil = points[LEFT_PUPIL]
        e_left = points[LEFT_EYE_LEFT_CORNER]
        e_right = points[LEFT_EYE_RIGHT_CORNER]
        e_top = points[LEFT_EYE_TOP]
        e_bottom = points[LEFT_EYE_BOTTOM]

        h_ratio = math.dist(pupil, e_left) / math.dist(e_left, e_right)
        v_ratio = math.dist(pupil, e_top) / math.dist(e_top, e_bottom)

        if not calibrated:
            # Step-by-step onscreen guide for the user
            canvas.create_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40, 
                               text="CALIBRATION ACTIVE", 
                               fill="yellow", font=("Arial", 28, "bold"))
            canvas.create_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30, 
                               text="Roll your eyes to all 4 edges of your screen slowly.\nLook back at the middle and hit SPACEBAR to lock tracking.", 
                               fill="white", font=("Arial", 18), justify="center")
            
            # Corner calibration reference rings
            for cx, cy in [(20, 20), (SCREEN_WIDTH-20, 20), (20, SCREEN_HEIGHT-20), (SCREEN_WIDTH-20, SCREEN_HEIGHT-20)]:
                canvas.create_oval(cx-15, cy-15, cx+15, cy+15, outline="cyan", width=3)
                canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="cyan")

            if h_ratio < h_min: h_min = h_ratio
            if h_ratio > h_max: h_max = h_ratio
            if v_ratio < v_min: v_min = v_ratio
            if v_ratio > v_max: v_max = v_ratio

        else:
            # Map eyeball math to raw screen positions
            raw_x = map_value(h_ratio, h_min, h_max, 0, SCREEN_WIDTH)
            raw_y = map_value(v_ratio, v_min, v_max, 0, SCREEN_HEIGHT)

            # --- MATH FILTER: EXPONENTIAL SMOOTHING ---
            # Blend current frame with previous frame coordinates to absorb shakes
            smoothed_x = int((SMOOTH_FACTOR * raw_x) + ((1 - SMOOTH_FACTOR) * smoothed_x))
            smoothed_y = int((SMOOTH_FACTOR * raw_y) + ((1 - SMOOTH_FACTOR) * smoothed_y))

            # Snap limits to physical borders
            sx = max(0, min(smoothed_x, SCREEN_WIDTH))
            sy = max(0, min(smoothed_y, SCREEN_HEIGHT))

            # Evaluate bounding boxes using stabilized coordinates
            h_t1 = t1_x1 <= sx <= t1_x2 and t1_y1 <= sy <= t1_y2
            h_t2 = t2_x1 <= sx <= t2_x2 and t2_y1 <= sy <= t2_y2
            h_t3 = t3_x1 <= sx <= t3_x2 and t3_y1 <= sy <= t3_y2
            h_t4 = t4_x1 <= sx <= t4_x2 and t4_y1 <= sy <= t4_y2

            # Render UI elements
            for box, hover, txt in [((t1_x1, t1_y1, t1_x2, t1_y2), h_t1, "Top-Left Content Block"),
                                    ((t2_x1, t2_y1, t2_x2, t2_y2), h_t2, "Top-Right Content Block"),
                                    ((t3_x1, t3_y1, t3_x2, t3_y2), h_t3, "Bottom-Left Content Block"),
                                    ((t4_x1, t4_y1, t4_x2, t4_y2), h_t4, "Bottom-Right Content Block")]:
                bx1, by1, bx2, by2 = box
                bg_color = "#00FF00" if hover else "#1e1e1e"
                text_color = "black" if hover else "white"
                border_color = "lime" if hover else "gray40"
                
                canvas.create_rectangle(bx1, by1, bx2, by2, fill=bg_color, outline=border_color, width=3 if hover else 1)
                canvas.create_text((bx1+bx2)//2, (by1+by2)//2, text=txt, fill=text_color, font=("Arial", 16, "bold"))

            # Display central grid reference lines
            canvas.create_line(SCREEN_WIDTH//2, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT, fill="gray25", dash=(2,4))
            canvas.create_line(0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2, fill="gray25", dash=(2,4))

            # Stabilized cursor sight
            canvas.create_oval(sx-10, sy-10, sx+10, sy+10, outline="lime", width=2)
            canvas.create_oval(sx-2, sy-2, sx+2, sy+2, fill="red")

    def lock_calibration(event):
        global calibrated
        calibrated = True

    root.bind("<space>", lock_calibration)

    cv2.imshow("Webcam Stream (Press ESC to close)", frame)
    if cv2.waitKey(1) == 27:
        root.destroy()
        return

    root.after(15, update_gaze)

root.after(10, update_gaze)
root.mainloop()
webcam.release()
cv2.destroyAllWindows()
