# import cv2
# import csv
# import os
# from cvzone.FaceMeshModule import FaceMeshDetector

# # ---------------- CAMERA ----------------
# cap = cv2.VideoCapture(0)
# detector = FaceMeshDetector(maxFaces=1)

# # ---------------- LANDMARKS ----------------
# LEFT_IRIS = 468
# RIGHT_IRIS = 473

# LEFT_EYE_LEFT = 33
# LEFT_EYE_RIGHT = 133
# LEFT_EYE_TOP = 159
# LEFT_EYE_BOTTOM = 145

# # ---------------- SAVE FILE ----------------
# save_path = os.path.join(os.getcwd(), "eye_data.csv")
# file = open(save_path, "a", newline="", buffering=1)
# writer = csv.writer(file)

# # Write header only if file is empty
# if os.path.getsize(save_path) == 0:
#     writer.writerow([
#         "Left_Iris_X", "Left_Iris_Y",
#         "Right_Iris_X", "Right_Iris_Y",

#         "Eye_Left_X", "Eye_Left_Y",
#         "Eye_Right_X", "Eye_Right_Y",
#         "Eye_Top_X", "Eye_Top_Y",
#         "Eye_Bottom_X", "Eye_Bottom_Y",

#         "Norm_X", "Norm_Y",
#         "Gaze_Direction"
#     ])

# print("Dataset collecting...")
# print("SPACE = Save sample")
# print("ESC = Exit")

# # ---------------- LOOP ----------------
# while True:
#     success, frame = cap.read()
#     if not success:
#         break

#     frame = cv2.flip(frame, 1)
#     frame, faces = detector.findFaceMesh(frame, draw=False)

#     gaze = "NO_FACE"

#     if faces:
#         pts = faces[0]

#         # ---------------- IRIS COORDINATES ----------------
#         lx, ly = pts[LEFT_IRIS]
#         rx, ry = pts[RIGHT_IRIS]

#         # ---------------- EYE LANDMARKS ----------------
#         eye_left_x, eye_left_y = pts[LEFT_EYE_LEFT]
#         eye_right_x, eye_right_y = pts[LEFT_EYE_RIGHT]
#         eye_top_x, eye_top_y = pts[LEFT_EYE_TOP]
#         eye_bottom_x, eye_bottom_y = pts[LEFT_EYE_BOTTOM]

#         # ---------------- EYE SIZE ----------------
#         eye_width = max(1, eye_right_x - eye_left_x)
#         eye_height = max(1, eye_bottom_y - eye_top_y)

#         # ---------------- NORMALIZATION ----------------
#         norm_x = (lx - eye_left_x) / eye_width

#         avg_y = (ly + ry) / 2
#         norm_y = (avg_y - eye_top_y) / eye_height

#         norm_x = max(0, min(1, norm_x))
#         norm_y = max(0, min(1, norm_y))

#         # ---------------- GAZE CLASSIFICATION ----------------
#         if norm_x < 0.30:
#             h = "LEFT"
#         elif norm_x > 0.70:
#             h = "RIGHT"
#         else:
#             h = "CENTER"

#         if norm_y < 0.30:
#             v = "TOP"
#         elif norm_y > 0.70:
#             v = "BOTTOM"
#         else:
#             v = "CENTER"

#         if h == "CENTER" and v == "CENTER":
#             gaze = "CENTER"
#         elif h == "LEFT" and v == "CENTER":
#             gaze = "LEFT"
#         elif h == "RIGHT" and v == "CENTER":
#             gaze = "RIGHT"
#         elif h == "CENTER" and v == "TOP":
#             gaze = "TOP"
#         elif h == "CENTER" and v == "BOTTOM":
#             gaze = "BOTTOM"
#         elif h == "LEFT" and v == "TOP":
#             gaze = "TOP_LEFT"
#         elif h == "RIGHT" and v == "TOP":
#             gaze = "TOP_RIGHT"
#         elif h == "LEFT" and v == "BOTTOM":
#             gaze = "BOTTOM_LEFT"
#         elif h == "RIGHT" and v == "BOTTOM":
#             gaze = "BOTTOM_RIGHT"

#         # ---------------- DRAW LANDMARKS ----------------
#         # Iris
#         cv2.circle(frame, (lx, ly), 4, (0, 255, 0), -1)
#         cv2.circle(frame, (rx, ry), 4, (0, 255, 0), -1)

#         # Eye landmarks
#         cv2.circle(frame, (eye_left_x, eye_left_y), 4, (255, 0, 0), -1)
#         cv2.circle(frame, (eye_right_x, eye_right_y), 4, (255, 0, 0), -1)
#         cv2.circle(frame, (eye_top_x, eye_top_y), 4, (0, 255, 255), -1)
#         cv2.circle(frame, (eye_bottom_x, eye_bottom_y), 4, (0, 255, 255), -1)

#         # Coordinate labels
#         cv2.putText(frame, f"L:{eye_left_x},{eye_left_y}",
#                     (eye_left_x - 40, eye_left_y - 10),
#                     cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

#         cv2.putText(frame, f"R:{eye_right_x},{eye_right_y}",
#                     (eye_right_x - 40, eye_right_y - 10),
#                     cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

#         cv2.putText(frame, f"T:{eye_top_x},{eye_top_y}",
#                     (eye_top_x - 30, eye_top_y - 10),
#                     cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

#         cv2.putText(frame, f"B:{eye_bottom_x},{eye_bottom_y}",
#                     (eye_bottom_x - 30, eye_bottom_y + 20),
#                     cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

#         # Iris coordinates
#         cv2.putText(frame, f"Iris L:({lx},{ly})",
#                     (20, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

#         cv2.putText(frame, f"Iris R:({rx},{ry})",
#                     (20, 100),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

#         # Normalized coordinates
#         cv2.putText(frame,
#                     f"NormX={norm_x:.2f}  NormY={norm_y:.2f}",
#                     (20, 130),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.6,
#                     (255, 255, 0),
#                     2)

#         # Gaze
#         cv2.putText(frame,
#                     f"Gaze: {gaze}",
#                     (20, 40),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (0, 255, 255),
#                     2)

#     # ---------------- SHOW WINDOW ----------------
#     cv2.imshow("Eye Dataset Collection", frame)

#     key = cv2.waitKey(1) & 0xFF

#     # ---------------- SAVE SAMPLE ----------------
#     if key == 32 and faces:
#         writer.writerow([
#             lx, ly,
#             rx, ry,

#             eye_left_x, eye_left_y,
#             eye_right_x, eye_right_y,
#             eye_top_x, eye_top_y,
#             eye_bottom_x, eye_bottom_y,

#             norm_x,
#             norm_y,
#             gaze
#         ])

#         file.flush()
#         print("Saved:", gaze)

#     # ---------------- EXIT ----------------
#     if key == 27:
#         break

# file.close()
# cap.release()
# cv2.destroyAllWindows()


import cv2
import csv
import os
from cvzone.FaceMeshModule import FaceMeshDetector

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

# ---------------- LANDMARKS ----------------
LEFT_IRIS = 468
RIGHT_IRIS = 473

LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145

# ---------------- SAVE FILE ----------------
save_path = os.path.join(os.getcwd(), "eye_data.csv")
file = open(save_path, "a", newline="", buffering=1)
writer = csv.writer(file)

# Write header if file is empty
if os.path.getsize(save_path) == 0:
    writer.writerow([
        "Left_Iris_X",
        "Left_Iris_Y",
        "Right_Iris_X",
        "Right_Iris_Y",
        "Norm_X",
        "Norm_Y",
        "Gaze_Direction"
    ])

print("Dataset collecting...")
print("SPACE = Save sample")
print("ESC = Exit")

# ---------------- LOOP ----------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame, faces = detector.findFaceMesh(frame, draw=False)

    gaze = "NO_FACE"

    if faces:
        pts = faces[0]

        # ---------------- IRIS COORDINATES ----------------
        lx, ly = pts[LEFT_IRIS]
        rx, ry = pts[RIGHT_IRIS]

        # ---------------- EYE LANDMARKS (used only for normalization) ----------------
        eye_left = pts[LEFT_EYE_LEFT]
        eye_right = pts[LEFT_EYE_RIGHT]
        eye_top = pts[LEFT_EYE_TOP]
        eye_bottom = pts[LEFT_EYE_BOTTOM]

        eye_width = max(1, eye_right[0] - eye_left[0])
        eye_height = max(1, eye_bottom[1] - eye_top[1])

        # ---------------- NORMALIZATION ----------------
        norm_x = (lx - eye_left[0]) / eye_width

        avg_y = (ly + ry) / 2
        norm_y = (avg_y - eye_top[1]) / eye_height

        norm_x = max(0, min(1, norm_x))
        norm_y = max(0, min(1, norm_y))

        # ---------------- GAZE CLASSIFICATION ----------------
        if norm_x < 0.30:
            h = "LEFT"
        elif norm_x > 0.70:
            h = "RIGHT"
        else:
            h = "CENTER"

        if norm_y < 0.30:
            v = "TOP"
        elif norm_y > 0.70:
            v = "BOTTOM"
        else:
            v = "CENTER"

        if h == "CENTER" and v == "CENTER":
            gaze = "CENTER"
        elif h == "LEFT" and v == "CENTER":
            gaze = "LEFT"
        elif h == "RIGHT" and v == "CENTER":
            gaze = "RIGHT"
        elif h == "CENTER" and v == "TOP":
            gaze = "TOP"
        elif h == "CENTER" and v == "BOTTOM":
            gaze = "BOTTOM"
        elif h == "LEFT" and v == "TOP":
            gaze = "TOP_LEFT"
        elif h == "RIGHT" and v == "TOP":
            gaze = "TOP_RIGHT"
        elif h == "LEFT" and v == "BOTTOM":
            gaze = "BOTTOM_LEFT"
        elif h == "RIGHT" and v == "BOTTOM":
            gaze = "BOTTOM_RIGHT"

        # ---------------- DISPLAY ----------------
        cv2.circle(frame, (lx, ly), 4, (0, 255, 0), -1)
        cv2.circle(frame, (rx, ry), 4, (0, 255, 0), -1)

        cv2.putText(frame, f"Gaze: {gaze}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2)

        cv2.putText(frame,
                    f"NormX={norm_x:.2f}  NormY={norm_y:.2f}",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2)

    cv2.imshow("Eye Dataset Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    # ---------------- SAVE SAMPLE ----------------
    if key == 32 and faces:
        writer.writerow([
            lx,
            ly,
            rx,
            ry,
            norm_x,
            norm_y,
            gaze
        ])

        file.flush()
        print("Saved:", gaze)

    # ---------------- EXIT ----------------
    if key == 27:
        break

file.close()
cap.release()
cv2.destroyAllWindows()
