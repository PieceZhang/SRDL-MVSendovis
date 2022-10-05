# coding:utf-8

import cv2
import os
import time

FRAME_WIDTH = int(1280 * 1)  # 1280
FRAME_HEIGHT = int(720 * 1)  # 720
WINDOW_WIDTH = int(FRAME_WIDTH * 0.5)
WINDOW_HEIGHT = int(FRAME_HEIGHT * 0.5)

camera1 = cv2.VideoCapture(2)
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

camera2 = cv2.VideoCapture(0)
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

cv2.namedWindow("camera1")
cv2.namedWindow("camera2")
cv2.moveWindow("camera1", 0, 0)
cv2.moveWindow("camera2", 700, 0)

camera1path = r'./videocap/cam1'
camera2path = r'./videocap/cam2'

if not os.path.exists(camera1path):
    os.mkdir(camera1path)
if not os.path.exists(camera2path):
    os.mkdir(camera2path)

codec = cv2.VideoWriter_fourcc(*'XVID')
fps = 25

startcap = False

while True:
    ret, camera1_frame = camera1.read()
    ret, camera2_frame = camera2.read()

    # camera1_frame = cv2.flip(camera1_frame, -1)
    # camera2_frame = cv2.flip(camera2_frame, -1)

    cv2.imshow("camera1", cv2.resize(camera1_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))
    cv2.imshow("camera2", cv2.resize(camera2_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))

    if startcap:
        output1.write(camera1_frame)
        output2.write(camera2_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        if startcap:
            startcap = False
            output1.release()
            output2.release()
            print("[INFO] Stop capture, filename: {}".format(timestamp))
        break
    elif key == ord("s"):
        if not startcap:
            startcap = True
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            camera1name = camera1path + '/cam1video_{}.avi'.format(timestamp)
            camera2name = camera2path + '/cam2video_{}.avi'.format(timestamp)
            output1 = cv2.VideoWriter(camera1name, codec, fps, (FRAME_WIDTH, FRAME_HEIGHT))
            output2 = cv2.VideoWriter(camera2name, codec, fps, (FRAME_WIDTH, FRAME_HEIGHT))
            print("[INFO] Start capture, filename: {}".format(timestamp))
        elif startcap:
            startcap = False
            output1.release()
            output2.release()
            print("[INFO] Stop capture, filename: {}".format(timestamp))

camera1.release()
camera2.release()
cv2.destroyWindow("camera1")
cv2.destroyWindow("camera2")
