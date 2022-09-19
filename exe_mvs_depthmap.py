# coding:utf-8

from exe_mvs import *

if __name__ == '__main__':
    cv2.namedWindow("depth")
    cv2.namedWindow("depth(normalized)")
    while True:
        ret, camera1_frame = camera1.read()
        ret, camera2_frame = camera2.read()

        camera1_frame = cv2.flip(camera1_frame, -1)
        camera2_frame = cv2.flip(camera2_frame, -1)

        camera1_frame = cv2.cvtColor(camera1_frame, cv2.COLOR_BGR2GRAY)
        camera2_frame = cv2.cvtColor(camera2_frame, cv2.COLOR_BGR2GRAY)

        camera1_frame = cv2.remap(camera1_frame, StereoMap[1][0], StereoMap[1][1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # 立体校正
        camera2_frame = cv2.remap(camera2_frame, StereoMap[2][0], StereoMap[2][1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)  # 立体校正

        cv2.imshow("camera1", cv2.resize(camera1_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))
        cv2.imshow("camera2", cv2.resize(camera2_frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_CUBIC))

        # stereo = cv2.StereoSGBM_create(0, 32, 49)
        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=39)
        disparity = stereo.compute(camera1_frame, camera2_frame)
        cv2.imshow("depth", disparity)
        disparitynorm = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        cv2.imshow("depth(normalized)", disparitynorm)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

camera1.release()
camera2.release()
cv2.destroyWindow("camera1")
cv2.destroyWindow("camera2")
