import cv2
import numpy as np

globalCnt = 0


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


def rect_people(old_frame, new_frame, line):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))
    diff = cv2.absdiff(old_frame, new_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    frame = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 5)

    # cv2.imshow('gray', frame)

    dilated = cv2.dilate(frame, kernel, iterations=3)
    cv2.imshow('th', dilated)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if h > 15:  # potrebno je namsestiti
            # cv2.rectangle(old_frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

            if line[1] < y + int(h/2) < line[1] + 400:
                cv2.circle(old_frame, (x + int(w / 2), y + int(h / 2)), 1, (0, 255, 0), 3)
            else:
                cv2.circle(old_frame, (x + int(w / 2), y + int(h / 2)), 1, (0, 0, 255), 3)
    cv2.rectangle(old_frame, (line[0] - 100, line[1]), (line[0] + 500, line[1] + 400), (0, 255, 0), 4)
    cv2.imshow('new', old_frame)


def process_video(path):
    print("aaaaaaa")
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    old_frame = frame.copy
    # frame = frame[75:471, 200:480]
    x1, y1, x2, y2 = detection_line(frame)
    aca = [x1, y1, x2, y2]
    print(aca)
    while True:
        old_frame = frame.copy()
        ret_val, frame = cap.read()
        new_frame = frame.copy()

        original_frame = frame.copy()
        # frame = frame[75:471, 117:520]

        # count_people(frame)
        rect_people(old_frame, new_frame, aca)
        if not ret_val:
            break
        cv2.line(original_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('video', original_frame)
        cv2.waitKey(15)


process_video('.\\Data\\video1.mp4')
