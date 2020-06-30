import cv2
import numpy as np


def detection_line(frame):
    original = frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    min_line_length = 250
    edges = cv2.Canny(frame, 50, 150, apertureSize=3)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # edges = cv2.erode(edges, kernel=kernel, iterations=1)
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=300, lines=np.array([]),
                            minLineLength=min_line_length, maxLineGap=20)

    # for i in range(0, len(lines)):
    x1 = lines[0][0][0]
    y1 = lines[0][0][1]
    x2 = lines[0][0][2]
    y2 = lines[0][0][3]

    # cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow('frame', original)
    # cv2.waitKey(0)

    return x1, y1, x2, y2


def count_people(frame):
    cv2.imshow('circles', frame)


def process_video(path):
    print("aaaaaaa")
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    original_frame = frame
    # frame = frame[75:471, 200:480]
    x1, y1, x2, y2 = detection_line(frame)

    while True:
        ret_val, frame = cap.read()
        original_frame = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = frame[75:471, 117:520]

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        # frame = np.invert(frame)
        frame = cv2.blur(frame, (3, 3))
        frame = cv2.dilate(frame, kernel, iterations=1)
        # frame = cv2.erode(frame, kernel, iterations=1)
        frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)

        count_people(frame)
        if not ret_val:
            break
        cv2.line(original_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('video', original_frame)
        cv2.waitKey(5)


process_video('.\\Data\\video10.mp4')
