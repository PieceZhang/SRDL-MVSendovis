# coding:utf-8
# https://blog.csdn.net/qq_22059843/article/details/103400094
import cv2
import time
import os

camID = {1: 0, 2: 2, 3: 3, 4: 4}
cam1num = 1
cam2num = 2

camera1 = cv2.VideoCapture(camID[cam1num])
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

camera2 = cv2.VideoCapture(camID[cam2num])
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

AUTO = False  # True自动拍照，False则手动按s键拍照
INTERVAL = 0.0000005  # 调整自动拍照间隔

cv2.namedWindow("camera1")
cv2.namedWindow("camera2")
cv2.moveWindow("camera1", 0, 0)
cv2.moveWindow("camera2", 700, 0)

counter = 0
utc = time.time()

camera1path = r'./imgcap/cam{}'.format(cam1num)
camera2path = r'./imgcap/cam{}'.format(cam2num)

if not os.path.exists(camera1path):
    os.mkdir(camera1path)
if not os.path.exists(camera2path):
    os.mkdir(camera2path)


def shot(camnum, imgnum, frame):
    path = './imgcap/cam{}/{}_cam{}.jpg'.format(camnum, imgnum, camnum)
    cv2.imwrite(path, frame)
    print("snapshot saved into: " + path)


while True:
    ret, camera1_frame = camera1.read()
    ret, camera2_frame = camera2.read()

    # camera1_frame = cv2.flip(camera1_frame, -1)  # 180 degree
    # camera2_frame = cv2.flip(camera2_frame, -1)  # 180 degree
    # camera1_frame = cv2.transpose(cv2.flip(camera1_frame, 1))  # 90 degree
    # camera2_frame = cv2.transpose(cv2.flip(camera2_frame, 1))  # 90 degree

    # camera1_frame = cv2.line(camera1_frame, (0, 360), (1280, 360), (0, 0, 255), 5)  # 绘制极线
    # camera2_frame = cv2.line(camera2_frame, (0, 360), (1280, 360), (0, 0, 255), 5)  # 绘制极线

    cv2.imshow("camera1", cv2.resize(camera1_frame, (640, 360), interpolation=cv2.INTER_CUBIC))
    cv2.imshow("camera2", cv2.resize(camera2_frame, (640, 360), interpolation=cv2.INTER_CUBIC))

    # cv2.imshow("camera1", camera1_frame)
    # cv2.imshow("camera2", camera2_frame)

    now = time.time()
    if AUTO and now - utc >= INTERVAL:
        shot(cam1num, counter, camera1_frame)
        shot(cam2num, counter, camera2_frame)
        counter += 1
        utc = now

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        shot(cam1num, counter, camera1_frame)
        shot(cam2num, counter, camera2_frame)
        counter += 1

camera1.release()
camera2.release()
