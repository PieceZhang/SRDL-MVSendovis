import cv2
import numpy as np


# https://blog.csdn.net/Python_Matlab/article/details/102887095
def edge_demo(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 0)  # 高斯降噪，适度
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    # 求梯度
    xgrd = cv2.Sobel(gray, cv2.CV_16SC1, 1, 0, ksize=5)
    ygrd = cv2.Sobel(gray, cv2.CV_16SC1, 0, 1, ksize=5)

    egde_output = cv2.Canny(xgrd, ygrd, 50, 150)  # 50低阈值，150高阈值
    # egde_output = cv.Canny(gray,50,150)   #都可使用
    cv2.imshow('canny_edge', egde_output)

    # 输出彩色图
    dst = cv2.bitwise_and(image, image, mask=egde_output)
    cv2.imshow('color edge', dst)


if __name__ == "__main__":
    # filepath = r"D:\B_SRDL\pysot\training_dataset\my_endos\crop511\cam1video_2022-11-12_21-59-11\000000\000000.00.x.jpg"
    filepath = r"D:\B_SRDL\2022-12-29_203546.png"
    img = cv2.imread(filepath)  # blue green red
    cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("input image", img)

    edge_demo(img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
