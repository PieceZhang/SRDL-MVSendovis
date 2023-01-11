# coding:utf-8

import cv2
import os
import time
import argparse

parser = argparse.ArgumentParser(description='multi cams video capture')
parser.add_argument('--num', default=2, type=int, help='number of cam')
parser.add_argument('--nolist', default=[0, 1], type=list, help='cam no. list')
args = parser.parse_args()
assert args.num == len(args.nolist)

FRAME_WIDTH = int(1280 * 1)  # 1280
FRAME_HEIGHT = int(720 * 1)  # 720
WINDOW_WIDTH = int(FRAME_WIDTH * 0.5)
WINDOW_HEIGHT = int(FRAME_HEIGHT * 0.5)

camlist = []
pathlist = []
for i in range(args.num):
    cam = cv2.VideoCapture(args.nolist[i])
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cv2.namedWindow("camera{}".format(i + 1))
    camlist.append(cam)
    path = r'./videocap/cam{}'.format(i + 1)
    if not os.path.exists(path):
        os.mkdir(path)
    pathlist.append(path)

codec = cv2.VideoWriter_fourcc(*'XVID')
fps = 30

startcap = False

while True:
    framelist = []
    for i in range(args.num):
        ret, frame = camlist[i].read()
        assert ret
        framelist.append(frame)
        cv2.imshow("camera{}".format(i + 1), cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))

    if startcap:
        for i in range(args.num):
            writerlist[i].write(framelist[i])

    key = cv2.waitKey(1)
    if key == ord("q"):
        if startcap:
            startcap = False
            for i in range(args.num):
                writerlist[i].release()
            print("[INFO] Stop capture, filename: {}".format(timestamp))
        break
    elif key == ord("s"):
        if not startcap:
            startcap = True
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            writerlist = []
            for i in range(args.num):
                writerlist.append(cv2.VideoWriter(pathlist[i] + '/cam{}video_{}.avi'.format(i + 1, timestamp),
                                                  codec, fps, (FRAME_WIDTH, FRAME_HEIGHT)))
            print("[INFO] Start capture, filename: {}".format(timestamp))
        elif startcap:
            startcap = False
            for i in range(args.num):
                writerlist[i].release()
            writerlist = []
            print("[INFO] Stop capture, filename: {}".format(timestamp))

for cam in camlist:
    cam.release()
