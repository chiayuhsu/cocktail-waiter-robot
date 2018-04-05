import numpy as np
import cv2
from imutils.object_detection import non_max_suppression

cap = cv2.VideoCapture(0)

while(True):
    
    # read images
    ret, frame = cap.read()

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # pedestrian detection
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05) 
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
 
    # draw bounding boxes
    for (xA, yA, xB, yB) in pick:
	cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)    

    # show images
    cv2.imshow('after', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
