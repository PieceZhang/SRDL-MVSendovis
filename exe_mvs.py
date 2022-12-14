# coding:utf-8
"""
单目相机畸变矫正: https://blog.csdn.net/qq_41170600/article/details/103037028
立体校正: https://blog.csdn.net/weixin_43788282/article/details/124434611

"""
import cv2
import numpy as np

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
WINDOW_WIDTH = int(FRAME_WIDTH * 0.5)
WINDOW_HEIGHT = int(FRAME_HEIGHT * 0.5)

# Intrinsic Matrix
inmat1 = np.array([
    [729.805504098369, 0, 648.974913106474],
    [0, 730.860418019541, 418.936872740850],
    [0, 0, 1]
])
inmat2 = np.array([
    [731.797077430788, 0, 632.311698457381],
    [0, 731.384427290877, 368.705044840897],
    [0, 0, 1]
])
IntrinsicMatrix = {1: inmat1, 2: inmat2}
del inmat1
del inmat2

# Distortion Matrix (先立体矫正，再畸变矫正)
d1 = np.array([0.0676319395832053, -0.0718284677630564, 0, 0, 0])  # k1, k2, p1, p2, k3
d2 = np.array([0.0690562232934869, -0.0669207185079367, 0, 0, 0])  # k1, k2, p1, p2, k3
DistortionMatrix = {1: d1, 2: d2}
del d1
del d2

# Distortion Map  # cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
mapx1, mapy1 = cv2.initUndistortRectifyMap(IntrinsicMatrix[1], DistortionMatrix[1], None, IntrinsicMatrix[1], (FRAME_WIDTH, FRAME_HEIGHT), 5)
mapx2, mapy2 = cv2.initUndistortRectifyMap(IntrinsicMatrix[2], DistortionMatrix[2], None, IntrinsicMatrix[2], (FRAME_WIDTH, FRAME_HEIGHT), 5)
DistortionMap = {1: [mapx1, mapy1], 2: [mapx2, mapy2]}
del mapx1
del mapx2
del mapy1
del mapy2

# Stereo Rectify
R = np.array([
    [0.998634412480918, -0.0384450280065628, 0.0353735781405737],
    [0.0370254061436707, 0.998515526343090, 0.0399482534246386],
    [-0.0368568787173969, -0.0385839794909432, 0.998575408778853]
])  # MATLAB标定得到的R (Rotation of camera 2 relative to camera 1, specified as a 3-by-3 matrix.)
R = np.transpose(R)  # 转置的R
T = np.array([-34.3888358134576, 3.98282280687758, -0.250840913890431])
RL, RR, PL, PR, Q, roiL, roiR = cv2.stereoRectify(IntrinsicMatrix[1], DistortionMatrix[1], IntrinsicMatrix[2], DistortionMatrix[2],
                                                  (FRAME_WIDTH, FRAME_HEIGHT), R, T, 1, (0, 0))
camera1map = cv2.initUndistortRectifyMap(IntrinsicMatrix[1], DistortionMatrix[1], RL, PL, (FRAME_WIDTH, FRAME_HEIGHT), cv2.CV_16SC2)
camera2map = cv2.initUndistortRectifyMap(IntrinsicMatrix[2], DistortionMatrix[2], RR, PR, (FRAME_WIDTH, FRAME_HEIGHT), cv2.CV_16SC2)
StereoMap = {1: camera1map, 2: camera2map}
del camera1map
del camera2map

camera1 = cv2.VideoCapture(2)
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
camera2 = cv2.VideoCapture(1)
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
cv2.namedWindow("camera1")
cv2.namedWindow("camera2")
cv2.moveWindow("camera1", 0, 0)
cv2.moveWindow("camera2", WINDOW_WIDTH, 0)  # 并排显示

if __name__ == '__main__':
    while True:
        ret, camera1_frame = camera1.read()
        ret, camera2_frame = camera2.read()

        camera1_frame = cv2.flip(camera1_frame, -1)
        camera2_frame = cv2.flip(camera2_frame, -1)

        camera1_frame = cv2.remap(camera1_frame, StereoMap[1][0], StereoMap[1][1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # 立体校正
        camera2_frame = cv2.remap(camera2_frame, StereoMap[2][0], StereoMap[2][1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # 立体校正

        # camera1_frame = cv2.remap(camera1_frame, DistortionMap[1][0], DistortionMap[1][1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # 畸变校正
        # camera2_frame = cv2.remap(camera2_frame, DistortionMap[2][0], DistortionMap[2][1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # 畸变校正

        camera1_frame = cv2.line(camera1_frame, (0, 360), (1280, 360), (0, 0, 255), 5)  # 绘制极线
        camera2_frame = cv2.line(camera2_frame, (0, 360), (1280, 360), (0, 0, 255), 5)  # 绘制极线

        cv2.imshow("camera1", cv2.resize(camera1_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))
        cv2.imshow("camera2", cv2.resize(camera2_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    camera1.release()
    camera2.release()
    cv2.destroyWindow("camera1")
    cv2.destroyWindow("camera2")
