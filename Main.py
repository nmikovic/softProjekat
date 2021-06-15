import cv2
from euc_tracker import Tracker


tracker = Tracker()
valid_ids = []
rezultati = []
ispravno = [4, 24, 17, 23, 17, 27, 29, 22, 10, 23]

def detect_objects(old_frame, new_frame):

    #cv2.rectangle(old_frame, (244, 112), (435, 452), (0, 255, 0), 2)

    #razlika
    diff = cv2.absdiff(old_frame, new_frame)
    ##cv2.imshow('diff', diff)

    #siva
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ##cv2.imshow('gray', gray)

    #adaptivni treshold
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 7)
    ##cv2.imshow('adaptiveTresh', adaptive_threshold)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(adaptive_threshold, kernel, iterations=2)
    #cv2.imshow('dilated', dilated)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for contour in contours:
        area = cv2.contourArea(contour)
        #print(area)
        if area > 150:
            x, y, w, h = cv2.boundingRect(contour)
            cx = (x + x + w) / 2
            cy = (y + y + h) / 2

            detections.append([cx, cy])
            #cv2.circle(new_frame, (int(cx), int(cy)), 1, (0,255,0), 3)
            #cv2.rectangle(new_frame, (x,y), (x+w, y+h), (0,255,0), 2)

    boxes_ids = tracker.update(detections)
    #print('ovo cu prikazati', boxes_ids)

    for boxes_id in boxes_ids:

        cx, cy, id = boxes_id
        cv2.putText(new_frame, str(id), (int(cx), int(cy) + 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.circle(new_frame, (int(cx), int(cy)), 1, (0, 255, 0), 3)

        if(244 < cx < 435) and (112 < cy < 452) and id not in valid_ids:
            #print("dodao sam ", id)
            valid_ids.append(id)

    cv2.imshow('new_frame', new_frame) #prikaz rezultata detekcije

def load_video(path):

    cap = cv2.VideoCapture(path)
    ret, frame = cap.read() #citam prvi

    old_frame = frame.copy()
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        new_frame = frame.copy()

        detect_objects(new_frame, old_frame)

        old_frame = new_frame

        ##cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
            cap.release()
    cv2.destroyAllWindows()
    #print(len(valid_ids))


for i in range(1, 11):
    valid_ids = []
    pravi_rez = []
    tracker = Tracker()
    a = 1

    load_video('.\\Predefinisani projekat 3\\video' + i.__str__() + '.mp4')


    #filter objekata
    for id in valid_ids:
        if tracker.points[id][2] > 10: #broj uspesnih detektovanja tacke u zeljenoj regiji
            pravi_rez.append(id)

    #print(valid_ids)
    #rezultati.append(len(valid_ids))
    rezultati.append(len(pravi_rez))
    #print(tracker.points)
    #print("nakon filtera" , pravi_rez)
    print("Rezultat za video " + i.__str__() + ": " + len(pravi_rez).__str__())

sum = 0
for i in range(0, 10):
    sum += abs(rezultati[i] - ispravno[i])

print("MAE:", sum/10)
