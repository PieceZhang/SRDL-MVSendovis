# coding:utf-8

import cv2
import os

FRAME_WIDTH = int(1280 * 1)  # 1280
FRAME_HEIGHT = int(720 * 1)  # 720
WINDOW_WIDTH = int(FRAME_WIDTH * 0.5)
WINDOW_HEIGHT = int(FRAME_HEIGHT * 0.5)

cv2.namedWindow("camera1")
cv2.namedWindow("camera2")
cv2.moveWindow("camera1", 0, 0)
cv2.moveWindow("camera2", 700, 0)

camera1path = r'./videocap/cam1'
camera2path = r'./videocap/cam2'

camera1name = camera1path + '/cam1video.avi'
camera2name = camera2path + '/cam2video.avi'

camera1 = cv2.VideoCapture(camera1name)
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

camera2 = cv2.VideoCapture(camera2name)
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

while True:
    ret1, camera1_frame = camera1.read()
    ret2, camera2_frame = camera2.read()

    # camera1_frame = cv2.flip(camera1_frame, -1)
    # camera2_frame = cv2.flip(camera2_frame, -1)

    if ret1 and ret2:
        cv2.imshow("camera1", cv2.resize(camera1_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))
        cv2.imshow("camera2", cv2.resize(camera2_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))

        key = cv2.waitKey(40)  # 25 fps
        if key == ord("q"):
            break
    else:
        break

camera1.release()
camera2.release()
cv2.destroyWindow("camera1")
cv2.destroyWindow("camera2")
