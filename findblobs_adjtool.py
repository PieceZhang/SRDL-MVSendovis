import cv2
import numpy as np
from pickle import dump, load


def process(image, color_dist):
    gs_frame = cv2.GaussianBlur(image, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, color_dist['Lower'], color_dist['Upper'])
    return inRange_hsv


def callback(a):
    _Hlow = cv2.getTrackbarPos(tHlow, windowName)
    _Hhigh = cv2.getTrackbarPos(tHhigh, windowName)
    _Slow = cv2.getTrackbarPos(tSlow, windowName)
    _Shigh = cv2.getTrackbarPos(tShigh, windowName)
    _Vlow = cv2.getTrackbarPos(tVlow, windowName)
    _Vhigh = cv2.getTrackbarPos(tVhigh, windowName)
    color_dist = {'Lower': np.array([_Hlow, _Slow, _Vlow]), 'Upper': np.array([_Hhigh, _Shigh, _Vhigh])}
    dst = process(img, color_dist)
    cv2.imshow(windowName, dst)


if __name__ == '__main__':
    Hlow = 0
    Hhigh = 255
    Slow = 0
    Shigh = 255
    Vlow = 0
    Vhigh = 255

    try:
        f = open('color_dist.pickle', 'rb')
        color_dist_init = load(f)
    except FileNotFoundError:
        color_dist_init = {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])}
    except EOFError:
        color_dist_init = {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])}


    # img = cv2.imread("test.jpg")
    # img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
    # dst = process(img, color_dist_init)
    windowName = 'adjtool'  # 窗体名
    cv2.namedWindow(windowName)
    # cv2.imshow(windowName, dst)

    tHlow = 'Hlow '
    tHhigh = 'Hhigh'
    tSlow = 'Slow'
    tShigh = 'Shigh'
    tVlow = 'Vlow'
    tVhigh = 'Vhigh'
    cv2.createTrackbar(tHlow, windowName, color_dist_init['Lower'][0], 255, callback)
    cv2.createTrackbar(tHhigh, windowName, color_dist_init['Upper'][0], 255, callback)
    cv2.createTrackbar(tSlow, windowName, color_dist_init['Lower'][1], 255, callback)
    cv2.createTrackbar(tShigh, windowName, color_dist_init['Upper'][1], 255, callback)
    cv2.createTrackbar(tVlow, windowName, color_dist_init['Lower'][2], 255, callback)
    cv2.createTrackbar(tVhigh, windowName, color_dist_init['Upper'][2], 255, callback)

    cap = cv2.VideoCapture(0)
    while 1:
        ret, img = cap.read()
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow(windowName, img)
        key = cv2.waitKey(5)
        if key == ord('s'):  # 采集一帧图像
            dst = process(img, color_dist_init)
            cv2.imshow(windowName, dst)
            break

    while 1:
        key = cv2.waitKey(5)
        if key == ord('q'):
            break

    with open('color_dist.pickle', 'wb') as f:
        Hlow = cv2.getTrackbarPos(tHlow, windowName)
        Hhigh = cv2.getTrackbarPos(tHhigh, windowName)
        Slow = cv2.getTrackbarPos(tSlow, windowName)
        Shigh = cv2.getTrackbarPos(tShigh, windowName)
        Vlow = cv2.getTrackbarPos(tVlow, windowName)
        Vhigh = cv2.getTrackbarPos(tVhigh, windowName)
        color_dist = {'Lower': np.array([Hlow, Slow, Vlow]), 'Upper': np.array([Hhigh, Shigh, Vhigh])}
        dump(color_dist, f)

    cv2.destroyAllWindows()
