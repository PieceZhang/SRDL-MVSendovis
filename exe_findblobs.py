# https://blog.csdn.net/See_Star/article/details/103044722
import cv2
import numpy as np
from pickle import dump, load
from utils_kalman import KalmanFilter

try:
    f = open('color_dist.pickle', 'rb')
    color_dist = load(f)
except FileNotFoundError:
    color_dist = {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])}

cap = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)

KFx = KalmanFilter()
KFy = KalmanFilter()

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        if frame is not None:
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯模糊
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
            erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
            inRange_hsv = cv2.inRange(erode_hsv, color_dist['Lower'], color_dist['Upper'])
            cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            try:
                c = max(cnts, key=cv2.contourArea)
            except ValueError:
                pass
            else:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)

                # draw contours
                # cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)

                # center coordinates
                centercoor = (np.mean(box[:, 0]), np.mean(box[:, 1]))
                # draw center
                cv2.circle(frame, centercoor, 10, (255, 0, 0), 0)

                # kalman
                centerx = KFx.predict(centercoor[0])
                centery = KFy.predict(centercoor[1])
                centercoor = (int(centerx), int(centery))
                # draw center (kalman)
                cv2.circle(frame, centercoor, 10, (0, 0, 255), 0)

            cv2.imshow('camera', frame)
            cv2.waitKey(1)
        else:
            print("无画面")
    else:
        print("无法读取摄像头！")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
