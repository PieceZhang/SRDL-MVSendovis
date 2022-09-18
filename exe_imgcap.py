# coding:utf-8
# https://blog.csdn.net/qq_22059843/article/details/103400094
import cv2
import time
import os

camera1 = cv2.VideoCapture(1)
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

camera2 = cv2.VideoCapture(2)
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

camera1path = r'./imgcap/cam1'
camera2path = r'./imgcap/cam2'

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

    camera1_frame = cv2.flip(camera1_frame, -1)
    camera2_frame = cv2.flip(camera2_frame, -1)

    cv2.imshow("camera1", cv2.resize(camera1_frame, (640, 360), interpolation=cv2.INTER_CUBIC))
    cv2.imshow("camera2", cv2.resize(camera2_frame, (640, 360), interpolation=cv2.INTER_CUBIC))

    now = time.time()
    if AUTO and now - utc >= INTERVAL:
        shot(1, counter, camera1_frame)
        shot(2, counter, camera2_frame)
        counter += 1
        utc = now

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        shot(1, counter, camera1_frame)
        shot(2, counter, camera2_frame)
        counter += 1

camera1.release()
camera2.release()
cv2.destroyWindow("camera1")
cv2.destroyWindow("camera2")
