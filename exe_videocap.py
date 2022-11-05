# coding:utf-8

import cv2
import os
import time

FRAME_WIDTH = int(1280 * 1)  # 1280
FRAME_HEIGHT = int(720 * 1)  # 720
WINDOW_WIDTH = int(FRAME_WIDTH * 0.5)
WINDOW_HEIGHT = int(FRAME_HEIGHT * 0.5)

camID = {1: 0, 2: 3, 3: 4, 4: 2}
cam1num = 3
cam2num = 4

camera1 = cv2.VideoCapture(camID[cam1num])
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

camera2 = cv2.VideoCapture(camID[cam2num])
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

cv2.namedWindow("camera{}".format(cam1num))
cv2.namedWindow("camera{}".format(cam2num))
cv2.moveWindow("camera{}".format(cam1num), 0, 0)
cv2.moveWindow("camera{}".format(cam2num), 700, 0)

camera1path = r'./videocap/cam{}'.format(cam1num)
camera2path = r'./videocap/cam{}'.format(cam2num)

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

    # camera1_frame = cv2.flip(camera1_frame, -1)  # 180 degree
    # camera2_frame = cv2.flip(camera2_frame, -1)  # 180 degree
    # camera1_frame = cv2.transpose(cv2.flip(camera1_frame, 1))  # 90 degree
    # camera2_frame = cv2.transpose(cv2.flip(camera2_frame, 1))  # 90 degree

    cv2.imshow("camera{}".format(cam1num), cv2.resize(camera1_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))
    cv2.imshow("camera{}".format(cam2num), cv2.resize(camera2_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))

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
            camera1name = camera1path + '/cam{}video_{}.avi'.format(cam1num, timestamp)
            camera2name = camera2path + '/cam{}video_{}.avi'.format(cam2num, timestamp)
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
