import cv2
import time
from cvzone.FaceMeshModule import FaceMeshDetector
import pyautogui

# ---------------- SETUP ----------------
webcam = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

# Iris landmarks
LEFT_IRIS = 468
RIGHT_IRIS = 473

# Eye landmarks
L_LEFT = 33
L_RIGHT = 133
L_TOP = 159
L_BOTTOM = 145

# ---------------- SCROLL CONTROL ----------------
last_scroll_time = 0
scroll_delay = 0.25

print("Eye Auto-Scroll Running (ESC to exit)")

# ---------------- LOOP ----------------
while True:

    success, frame = webcam.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:

        pts = faces[0]

        # ---------------- IRIS CENTER ----------------
        left_iris = pts[LEFT_IRIS]
        right_iris = pts[RIGHT_IRIS]

        avg_x = int((left_iris[0] + right_iris[0]) / 2)
        avg_y = int((left_iris[1] + right_iris[1]) / 2)

        # ---------------- EYE BOUNDARIES ----------------
        eye_left = pts[L_LEFT]
        eye_right = pts[L_RIGHT]
        eye_top = pts[L_TOP]
        eye_bottom = pts[L_BOTTOM]

        eye_width = abs(eye_right[0] - eye_left[0])
        eye_height = abs(eye_bottom[1] - eye_top[1])

        if eye_width == 0 or eye_height == 0:
            continue

        # ---------------- NORMALIZED RATIOS ----------------
        norm_x = (avg_x - eye_left[0]) / eye_width
        norm_y = (avg_y - eye_top[1]) / eye_height

        norm_x = max(0, min(1, norm_x))
        norm_y = max(0, min(1, norm_y))

        # ---------------- HORIZONTAL ----------------
        if norm_x < 0.35:
            h_dir = "LEFT"
        elif norm_x > 0.65:
            h_dir = "RIGHT"
        else:
            h_dir = "CENTER"

        # ---------------- VERTICAL ----------------
        if norm_y < 0.35:
            v_dir = "TOP"
        elif norm_y > 0.65:
            v_dir = "BOTTOM"
        else:
            v_dir = "CENTER"

        # ---------------- COMBINE ----------------
        if h_dir == "CENTER" and v_dir == "CENTER":
            gaze = "CENTER"

        elif h_dir == "CENTER":
            gaze = v_dir

        elif v_dir == "CENTER":
            gaze = h_dir

        else:
            gaze = f"{v_dir} {h_dir}"

        # ---------------- AUTO SCROLL ----------------
        now = time.time()

        if now - last_scroll_time > scroll_delay:

            if gaze in ["TOP", "TOP LEFT", "TOP RIGHT"]:
                pyautogui.scroll(25)
                last_scroll_time = now

            elif gaze in ["BOTTOM", "BOTTOM LEFT", "BOTTOM RIGHT"]:
                pyautogui.scroll(-25)
                last_scroll_time = now

        # ---------------- VISUALS ----------------

        cv2.circle(frame, (avg_x, avg_y), 4, (0, 255, 0), -1)

        cv2.circle(frame, eye_left, 3, (255, 0, 0), -1)
        cv2.circle(frame, eye_right, 3, (255, 0, 0), -1)
        cv2.circle(frame, eye_top, 3, (255, 0, 0), -1)
        cv2.circle(frame, eye_bottom, 3, (255, 0, 0), -1)

        cv2.putText(
            frame,
            f"X:{avg_x} Y:{avg_y}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"NormX:{norm_x:.2f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"NormY:{norm_y:.2f}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Gaze: {gaze}",
            (20, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Eye Gaze Direction Tracker", frame)

    if cv2.waitKey(1) == 27:
        break

# ---------------- CLEANUP ----------------
webcam.release()
cv2.destroyAllWindows()
